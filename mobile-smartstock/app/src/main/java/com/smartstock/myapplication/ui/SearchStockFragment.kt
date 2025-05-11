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
import com.smartstock.myapplication.adapters.StockSearchAdapter
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.databinding.FragmentCreateOrderBinding
import com.smartstock.myapplication.databinding.FragmentSearchStockBinding
import com.smartstock.myapplication.models.Order
import com.smartstock.myapplication.models.Product
import com.smartstock.myapplication.models.ProductOrder
import com.smartstock.myapplication.models.Stock
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.UserSessionRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Calendar

class SearchStockFragment: Fragment() {

    private var _binding: FragmentSearchStockBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!
    private lateinit var adapter: NetworkServiceAdapter
    private lateinit var stockSearchAdapter: StockSearchAdapter

    private var selectedStoreId: String? = null
    private var selectedProductId: String? = null

    private var productsArray: ArrayList<Product> = arrayListOf()
    private var productsOrdersArray: ArrayList<ProductOrder> = arrayListOf()

    private var isSubmitting = false
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentSearchStockBinding.inflate(inflater, container, false)
        adapter = NetworkServiceAdapter.getInstance(requireContext())
        stockSearchAdapter = StockSearchAdapter(emptyList())
        binding.stocksResultRv.layoutManager = LinearLayoutManager(requireContext())
        binding.stocksResultRv.adapter = stockSearchAdapter
        // Set User:
        val sharedPreferences = requireContext().getSharedPreferences("CLL_APP", Context.MODE_PRIVATE)
        val type = sharedPreferences.getString("type", "")
        val id = sharedPreferences.getString("id", "")
        val name = sharedPreferences.getString("name", "")

        setupDropdowns()

        return binding.root

    }
    private fun setupDropdowns() {
        val storeDropdown = binding.autoCompleteTextViewCreate1
        val productDropdown = binding.autoCompleteTextViewCreate2

        lifecycleScope.launch {
            try {
                val stores = adapter.fetchPaginatedStores(
                    page = 1,
                    perPage = 100
                )
                println("************************Stores")
                println(stores)
                val storesNames = stores.map { it.name }
                storeDropdown.isEnabled = true
                storeDropdown.isFocusable = true
                storeDropdown.isClickable = true

                val dropdownAdapterStore = ArrayAdapter(
                    requireContext(),
                    R.layout.list_item,
                    storesNames
                )
                storeDropdown.setAdapter(dropdownAdapterStore)
                storeDropdown.setOnItemClickListener{parent, _, position, _ ->
                    val selectedStore = stores[position]
                    selectedStoreId = selectedStore.id
                }

                val products = adapter.fetchPaginatedSimpleProductName(
                    page = 1,
                    perPage = 100
                )
                println("************************Products")
                println(products)
                val productNames = products.map { it.name }
                productDropdown.isEnabled = true
                productDropdown.isFocusable = true
                productDropdown.isClickable = true

                val dropdownAdapterProduct = ArrayAdapter(
                    requireContext(),
                    R.layout.list_item,
                    productNames
                )
                productDropdown.setAdapter(dropdownAdapterProduct)
                productDropdown.setOnItemClickListener{parent, _, position, _ ->
                    val selectedProduct = products[position]
                    selectedProductId = selectedProduct.id
                }

            } catch (e: Exception) {
                e.printStackTrace()
                showMessage("Failed to fetch stores and clients", requireContext())
            }
        }
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        requireActivity().findViewById<View>(R.id.bottom_navigation)?.visibility = View.GONE
        binding.buttonCancelCreate.setOnClickListener {
            navigateToClients()
        }
        binding.buttonSearchProduct.setOnClickListener {
            if (!isSubmitting) {
                isSubmitting = true
                binding.buttonSearchProduct.isEnabled = false
                searchStock()
            }
        }

    }

    private fun searchStock() {
        println("selected store*******************: $selectedStoreId")
        println("selected product*******************: $selectedProductId")
        val argsArray: ArrayList<String?> = arrayListOf(selectedStoreId, selectedProductId)
        if (this.formIsValid(argsArray)) {

            lifecycleScope.launch {

                try {
                    val stock = adapter.fetchStockByProductIdAndStoreId(selectedProductId, selectedStoreId,requireContext())
                    Toast.makeText(requireContext(), getString(R.string.success_stock), Toast.LENGTH_LONG).show()
                    if (stock == null){
                        stockSearchAdapter.setData(emptyList())
                    } else{
                        val product = stock.product
                        product.quantity = stock.quantity_in_stock
                        stockSearchAdapter.setData(listOf(product))
                    }
                } catch (e: Exception) {
                    stockSearchAdapter.setData(emptyList())
                    e.printStackTrace()
                } finally {
                    isSubmitting = false
                    binding.buttonSearchProduct.isEnabled = true
                }
            }


        } else {
            showMessage(getString(R.string.error_add_client_fields), this.requireContext())
            binding.buttonSearchProduct.isEnabled = true
            isSubmitting = false
        }
    }

    private fun formIsValid(array: ArrayList<String?>): Boolean {
        for (elem in array) {
            if (TextUtils.isEmpty(elem)) {
                return false
            }
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
            SearchStockFragmentDirections.actionSearchStockFragmentToClientFragment()
        )
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}