package com.smartstock.myapplication.ui

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.DialogFragment
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.TextInputEditText
import com.smartstock.myapplication.R
import com.smartstock.myapplication.adapters.ProductAdapter
import com.smartstock.myapplication.models.Product
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.ProductRepository
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class AddProductDialogFragment(
    private val onProductAdded: (Product, Int) -> Unit
) : DialogFragment() {

    private var selectedProduct: Product? = null
    private lateinit var productAdapter: ProductAdapter

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val view = LayoutInflater.from(context).inflate(R.layout.dialog_add_product, null)

        val recyclerView = view.findViewById<RecyclerView>(R.id.productRecyclerView)
        val quantityInput = view.findViewById<TextInputEditText>(R.id.quantityInput)

        val repository = ProductRepository(NetworkServiceAdapter.getInstance(requireContext()))

        productAdapter = ProductAdapter { product ->
            selectedProduct = product
            Toast.makeText(context, "${getString(R.string.producto_seleccionado)} ${product.name}", Toast.LENGTH_SHORT).show()
        }

        recyclerView.apply {
            adapter = productAdapter
            layoutManager = LinearLayoutManager(context)
        }

        return AlertDialog.Builder(requireContext())
            .setView(view)
            .setPositiveButton(getString(R.string.agregar)) { _, _ ->
                val quantity = quantityInput.text.toString().toIntOrNull() ?: 0
                Log.d("quantity", quantity.toString())

                    selectedProduct?.let {
                        onProductAdded(it, quantity)
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
                productAdapter.submitData(it)
            }
        }
    }
}