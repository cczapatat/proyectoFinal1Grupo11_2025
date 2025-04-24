package com.smartstock.myapplication.adapters

import android.graphics.Color
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.paging.PagingDataAdapter
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.R
import com.smartstock.myapplication.databinding.ProductItemSelectBinding
import com.smartstock.myapplication.models.Product

class ProductAdapter (
    private val onProductClick: (Product) -> Unit
) : PagingDataAdapter<Product, ProductAdapter.ProductViewHolder>(DiffCallback) {

    private var selectedProductId: String? = null

    object DiffCallback : DiffUtil.ItemCallback<Product>() {
        override fun areItemsTheSame(oldItem: Product, newItem: Product): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: Product, newItem: Product): Boolean {
            return oldItem == newItem
        }
    }

    inner class ProductViewHolder(private val binding: ProductItemSelectBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(product: Product) {
            binding.productNameSelect.text = "${product.name} (${product.unit_price} x UND)"

            // Highlight the selected product
            val isSelected = product.id == selectedProductId
            val bgColor = if (isSelected) {
                ContextCompat.getColor(binding.root.context, R.color.purple_500) // or any color you want
            } else {
                Color.TRANSPARENT
            }
            binding.root.setBackgroundColor(bgColor)
            // Load image using Glide or Coil if needed
            // Click listener for selecting product
            binding.root.setOnClickListener {
                selectedProductId = product.id
                notifyDataSetChanged() // refresh to highlight the new selection
                onProductClick(product)
            }
            // Optional: load image if needed
            // Glide.with(binding.productImage.context).load(product.imageUrl).into(binding.productImage)
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val binding = ProductItemSelectBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ProductViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        val product = getItem(position)
        if (product != null) {
            holder.bind(product) // Use bind method to set up data
        }
    }
}