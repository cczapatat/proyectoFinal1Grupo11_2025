package com.smartstock.myapplication.ui

import android.app.DatePickerDialog
import android.content.Context
import android.os.Bundle
import android.text.TextUtils
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.smartstock.myapplication.R
import com.smartstock.myapplication.adapters.ProductAdapterOrder
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.databinding.FragmentCreateOrderBinding
import com.smartstock.myapplication.models.Order
import com.smartstock.myapplication.models.Product
import com.smartstock.myapplication.models.ProductOrder
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.UserSessionRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Calendar

class CreateOrderFragment: Fragment() {

    private var _binding: FragmentCreateOrderBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!
    private lateinit var adapter: NetworkServiceAdapter
    private lateinit var dateEdt: EditText
    private var selectedClientId: String? = ""
    private var productsArray: ArrayList<Product> = arrayListOf()
    private var productsOrdersArray: ArrayList<ProductOrder> = arrayListOf()

    private lateinit var paymentMap: Map<String, String>
    private lateinit var userSessionRepository: UserSessionRepository
    private lateinit var productAdapterOrder: ProductAdapterOrder

    private var isSubmitting = false
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentCreateOrderBinding.inflate(inflater, container, false)

        paymentMap = mapOf(
            getString(R.string.tipo_pago_ondelivery) to "PAYMENT_ON_DELIVERY",
            getString(R.string.tipo_pago_creditcard) to "CREDIT_CARD",
            getString(R.string.tipo_pago_debitcard) to "DEBIT_CARD"
        )
        adapter = NetworkServiceAdapter.getInstance(requireContext())
        val userTokenDao = AppDatabase.getDatabase(requireContext()).userTokenDao()
        userSessionRepository = UserSessionRepository(requireActivity().application, userTokenDao)


        // Set User:
        val sharedPreferences = requireContext().getSharedPreferences("CLL_APP", Context.MODE_PRIVATE)
        val type = sharedPreferences.getString("type", "")
        val id = sharedPreferences.getString("id", "")
        val name = sharedPreferences.getString("name", "")
        val clientDropdown = binding.autoCompleteTextViewCreate1
        if (type == "CLIENT"){
            clientDropdown.setText(name, false)
            clientDropdown.isEnabled = true
            clientDropdown.isFocusable = false
            clientDropdown.isClickable = false
        } else {
            // Logic to fetch seller clients
            clientDropdown.setText("", false)
            clientDropdown.isEnabled = false
            clientDropdown.isFocusable = false
            clientDropdown.isClickable = false
            lifecycleScope.launch {
                try {
                    val clients = adapter.fetchPaginatedClientsBySellerId(
                        sellerId = id!!, // `id` is the sellerId
                        page = 1,
                        perPage = 100 // Fetch enough clients for dropdown
                    )
                    val clientNames = clients.map { it.name }
                    clientDropdown.isEnabled = true
                    clientDropdown.isFocusable = true
                    clientDropdown.isClickable = true
                    // Bind names to dropdown
                    val dropdownAdapter = ArrayAdapter(
                        requireContext(),
                        R.layout.list_item, // Use the same list_item layout
                        clientNames
                    )
                    clientDropdown.setAdapter(dropdownAdapter)

                    // Handle client selection
                    clientDropdown.setOnItemClickListener { parent, _, position, _ ->
                        val selectedClient = clients[position]
                        selectedClientId = selectedClient.id.toString()
                    }

                } catch (e: Exception) {
                    e.printStackTrace()
                    showMessage("Failed to load clients", requireContext())
                }
            }
        }

        selectedClientId = id
        // Set Calendar
        val c = Calendar.getInstance()
        val df = SimpleDateFormat("dd-MM-yyyy")
        val formattedDate: String = df.format(c.time)
        dateEdt = binding.datePickerCreate
        dateEdt.setText(formattedDate)
        dateEdt.showSoftInputOnFocus = false
        dateEdt.setOnClickListener {

            val c = Calendar.getInstance()
            val year = c.get(Calendar.YEAR)
            val month = c.get(Calendar.MONTH)
            val day = c.get(Calendar.DAY_OF_MONTH)

            val datePickerDialog = DatePickerDialog(
                binding.root.context,
                { _, year, monthOfYear, dayOfMonth ->
                    val dat = String.format("%02d-%02d-%04d", dayOfMonth, monthOfYear + 1, year)
                    dateEdt.setText(dat)
                },
                year,
                month,
                day
            )
            // Prevent past date selection
            datePickerDialog.datePicker.minDate = System.currentTimeMillis() - 1000
            datePickerDialog.show()
        }


        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        requireActivity().findViewById<View>(R.id.bottom_navigation)?.visibility = View.GONE
        binding.buttonCancelCreate.setOnClickListener {
            navigateToClients()
        }
        binding.buttonAcceptCreate.setOnClickListener {
            if (!isSubmitting) {
                isSubmitting = true
                binding.buttonAcceptCreate.isEnabled = false
                addOrder()
            }


        }
        setupDropdowns()

        productAdapterOrder  = ProductAdapterOrder(productsArray) { productToDelete ->
            productsArray.remove(productToDelete)
            binding.productsOrderRv.adapter?.notifyDataSetChanged()
        }
        binding.productsOrderRv.adapter = productAdapterOrder
        binding.productsOrderRv.layoutManager = LinearLayoutManager(requireContext())
        // binding add product
        binding.buttonAddProduct.setOnClickListener {
            val dialog = AddProductDialogFragment { product, quantity, idStock ->
                // Handle added product and quantity
                product.id = idStock
                product.quantity = quantity
                productsArray.add(product)
                //productAdapterOrder.updateData(productsArray)
                productAdapterOrder.notifyDataSetChanged()
                updateTotalOrderValue()
                productAdapterOrder.notifyItemInserted(productsArray.size - 1)
            }
            dialog.show(parentFragmentManager, "AddProductDialog")
        }

    }

    private fun setupDropdowns() {
        val adapterZone = ArrayAdapter(requireContext(), R.layout.list_item, paymentMap.keys.toList())

        binding.autoCompleteTextViewCreate2.setAdapter(adapterZone)
    }

    private fun addOrder() {

        //val seller_id = UUID.randomUUID()
        val releaseDateOld = binding.datePickerCreate.text.toString()
        val arr = releaseDateOld.split("-")
        val orderDate = "${arr[2]}-${arr[1]}-${arr[0]} 23:59:30"

        val selectedPayment = binding.autoCompleteTextViewCreate2.text.toString()

        // Convert user-friendly dropdown values to request values
        val mappedPayment = paymentMap[selectedPayment] ?: ""


        val argsArray: ArrayList<String?> = arrayListOf(selectedClientId, orderDate, mappedPayment)
        if (this.formIsValid(argsArray, productsArray)) {

            for(prod in productsArray){
                productsOrdersArray.add(ProductOrder(prod.id, prod.quantity))
            }

            lifecycleScope.launch {
                val token = withContext(Dispatchers.IO) {
                    userSessionRepository.getSavedToken()
                }
                val order = Order(
                    client_id = selectedClientId,
                    delivery_date = orderDate,
                    payment_method = mappedPayment,
                    products = productsOrdersArray
                )

                try {
                    val createdOrder = adapter.addOrder(order, requireContext(), token)
                    Toast.makeText(requireContext(), getString(R.string.success_orden), Toast.LENGTH_LONG).show()
                    clearForm()
                    navigateToClients()
                } catch (e: Exception) {
                    e.printStackTrace()
                } finally {
                    isSubmitting = false
                    binding.buttonAcceptCreate.isEnabled = true
                }
            }


        } else {
            showMessage(getString(R.string.error_add_client_fields), this.requireContext())
            binding.buttonAcceptCreate.isEnabled = true
            isSubmitting = false
        }
    }

    private fun clearForm() {
        binding.autoCompleteTextViewCreate1.setText("")
        binding.datePickerCreate.setText("")
        binding.autoCompleteTextViewCreate2.setText("")
        productsArray.clear()
        binding.productsOrderRv.adapter?.notifyDataSetChanged()
    }

    private fun formIsValid(array: ArrayList<String?>, productsArray: ArrayList<Product>): Boolean {
        for (elem in array) {
            if (TextUtils.isEmpty(elem)) {
                return false
            }
        }
        if (productsArray.isEmpty()) {
            return false
        }
        return true
    }

    private fun showMessage(s: String, context: Context) {
        requireActivity().runOnUiThread{
            Toast.makeText(context, s, Toast.LENGTH_LONG).show()
        }
    }

    private fun navigateToClients() {

        binding.root.findNavController().navigate(
            CreateOrderFragmentDirections.actionCreateOrderFragmentToClientFragment()
        )
    }

    private fun updateTotalOrderValue() {
        val total = productsArray.sumOf { it.unit_price * it.quantity!! }
        binding.totalValueOrder.text = getString(R.string.total) + " $%,.0f".format(total)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}