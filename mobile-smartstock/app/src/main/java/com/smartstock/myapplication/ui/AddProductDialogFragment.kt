package com.smartstock.myapplication.ui

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.widget.Toast
import androidx.core.widget.addTextChangedListener
import androidx.fragment.app.DialogFragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.TextInputEditText
import com.smartstock.myapplication.R
import com.smartstock.myapplication.adapters.StockAdapter
import com.smartstock.myapplication.models.Product
import com.smartstock.myapplication.models.Stock
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.ProductRepository
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class AddProductDialogFragment(
    private val onProductAdded: (Product, Int, String) -> Unit
) : DialogFragment() {

    private var selectedStock: Stock? = null
    private lateinit var stockAdapter: StockAdapter
    private var quantityTextWatcher: android.text.TextWatcher? = null
    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val view = LayoutInflater.from(context).inflate(R.layout.dialog_add_product, null)

        val recyclerView = view.findViewById<RecyclerView>(R.id.productRecyclerView)
        val quantityInput = view.findViewById<TextInputEditText>(R.id.quantityInput)

        val repository = ProductRepository(NetworkServiceAdapter.getInstance(requireContext()))

        stockAdapter = StockAdapter { stock ->
            selectedStock = stock
            quantityInput.setText("")
            Toast.makeText(context, "${getString(R.string.producto_seleccionado)} ${stock.product.name}", Toast.LENGTH_SHORT).show()

            quantityTextWatcher?.let { quantityInput.removeTextChangedListener(it) }
            val maxQuantity = stock.quantity_in_stock
            quantityTextWatcher = object : android.text.TextWatcher {
                override fun beforeTextChanged(
                    s: CharSequence?,
                    start: Int,
                    count: Int,
                    after: Int
                ) {
                }

                override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}

                override fun afterTextChanged(s: android.text.Editable?) {
                    val enteredText = s.toString()
                    if (enteredText.isNotEmpty()) {
                        val enteredValue = enteredText.toIntOrNull() ?: 0
                        if (enteredValue > maxQuantity) {
                            quantityInput.setText(maxQuantity.toString())
                            quantityInput.setSelection(quantityInput.text?.length ?: 0)
                            Toast.makeText(
                                requireContext(),
                                "${getString(R.string.max_stock_available)} $maxQuantity",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }
                }
            }
            quantityInput.addTextChangedListener(quantityTextWatcher)

        }


        recyclerView.apply {
            adapter = stockAdapter
            layoutManager = LinearLayoutManager(context)
        }

        return AlertDialog.Builder(requireContext())
            .setView(view)
            .setPositiveButton(getString(R.string.agregar)) { _, _ ->
                val quantity = quantityInput.text.toString().toIntOrNull() ?: 0
                Log.d("quantity", quantity.toString())

                    selectedStock?.let {
                        onProductAdded(it.product, quantity, it.id)
                    } ?: Toast.makeText(context, getString(R.string.favor_seleccionar_producto), Toast.LENGTH_SHORT).show()
            }
            .setNegativeButton(getString(R.string.cancelar), null)
            .setNegativeButton(getString(R.string.cancelar), null)
            .create()
    }

    override fun onResume() {
        super.onResume()

        lifecycleScope.launch {
            val repository = ProductRepository(NetworkServiceAdapter.getInstance(requireContext()))
            repository.getPaginatedProducts().collectLatest {
                stockAdapter.submitData(it)
            }
        }
    }
}