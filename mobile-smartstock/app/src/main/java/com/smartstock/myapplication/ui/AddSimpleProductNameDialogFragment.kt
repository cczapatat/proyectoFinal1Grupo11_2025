package com.smartstock.myapplication.ui

import android.app.Dialog
import android.os.Bundle
import android.view.LayoutInflater
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.fragment.app.DialogFragment
import androidx.lifecycle.lifecycleScope
import androidx.paging.cachedIn
import androidx.paging.filter
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.R
import com.smartstock.myapplication.adapters.SimpleProductPagingAdapter
import com.smartstock.myapplication.models.SimpleProductName
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.SimpleProductNameRepository
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch

/**
 * Dialog that shows a paginated list of products.
 * Each tap:
 *  • notifies the parent via onProductAdded,
 *  • excludes that product from future pages,
 *  • and refreshes the list in-place.
 */
class AddSimpleProductNameDialogFragment(
    private val onProductAdded: (SimpleProductName) -> Unit
) : DialogFragment() {

    // Track which IDs have already been picked
    private val excludedIds = mutableSetOf<String>()

    // The paging adapter must be a property so we can call .refresh() on it
    private lateinit var pagingAdapter: SimpleProductPagingAdapter

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        // Inflate your dialog layout
        val view = LayoutInflater.from(requireContext())
            .inflate(R.layout.dialog_add_simple_product_name, null)

        // Find RecyclerView and wire up the paging adapter
        val recycler = view.findViewById<RecyclerView>(R.id.simpleProductRecyclerView)
        pagingAdapter = SimpleProductPagingAdapter { product ->
            // 1) send back to parent
            onProductAdded(product)
            // 2) mark as excluded so it's removed from the list
            excludedIds.add(product.id)
            // 3) re-load pages (this removes the tapped item)
            pagingAdapter.refresh()
            // 4) optional feedback
            Toast.makeText(
                requireContext(),
                getString(R.string.producto_seleccionado),
                Toast.LENGTH_SHORT
            ).show()
        }
        recycler.layoutManager = LinearLayoutManager(requireContext())
        recycler.adapter = pagingAdapter

        // Build AlertDialog
        val dialog = AlertDialog.Builder(requireContext())
            .setView(view)
            .setPositiveButton(R.string.aceptar, null)
            .setNegativeButton(R.string.cancelar, null)
            .create()

        // Once it’s shown, start collecting pages (excluding tapped IDs)
        dialog.setOnShowListener {
            lifecycleScope.launch {
                SimpleProductNameRepository(
                    NetworkServiceAdapter.getInstance(requireContext())
                )
                    .getPaginatedSimpleProducts()
                    .map { pagingData ->
                        // Filter out any IDs the user has already picked
                        pagingData.filter { it.id !in excludedIds }
                    }
                    .cachedIn(lifecycleScope)
                    .collectLatest { pagingData ->
                        pagingAdapter.submitData(lifecycle, pagingData)
                    }
            }
        }

        return dialog
    }
}