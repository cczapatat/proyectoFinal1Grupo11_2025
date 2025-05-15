package com.smartstock.myapplication.adapters

import android.graphics.Color
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.Toast
import androidx.core.content.ContextCompat
import androidx.paging.PagingDataAdapter
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.R
import com.smartstock.myapplication.databinding.ProductItemSelectBinding
import com.smartstock.myapplication.models.Product
import com.smartstock.myapplication.models.Stock

class StockAdapter (
    private val onProductClick: (Stock) -> Unit
) : PagingDataAdapter<Stock, StockAdapter.StockViewHolder>(DiffCallback) {

    private var selectedStockId: String? = null

    object DiffCallback : DiffUtil.ItemCallback<Stock>() {
        override fun areItemsTheSame(oldItem: Stock, newItem: Stock): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: Stock, newItem: Stock): Boolean {
            return oldItem == newItem
        }
    }

    inner class StockViewHolder(private val binding: ProductItemSelectBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(stock: Stock) {
            val product = stock.product
            binding.productNameSelect.text = "${product.name} (${product.unit_price} x UND) (${stock.quantity_in_stock})"
            binding.productNameSelect.contentDescription = "${product.name} (${product.unit_price} x UND) (${stock.quantity_in_stock})"
            val isOutOfStock = stock.quantity_in_stock <= 0
            val isSelected = stock.id == selectedStockId

            val context = binding.root.context
            val bgColor = when {
                isOutOfStock -> Color.LTGRAY
                isSelected -> ContextCompat.getColor(context, R.color.purple_500)
                else -> Color.TRANSPARENT
            }

            binding.root.setBackgroundColor(bgColor)
            binding.root.alpha = if (isOutOfStock) 0.5f else 1.0f
            // Load image using Glide or Coil if needed
            // Click listener for selecting product
            binding.root.setOnClickListener {
                if (!isOutOfStock) {
                    selectedStockId = stock.id
                    notifyDataSetChanged()
                    onProductClick(stock)
                } else {
                    Toast.makeText(context, context.getString(R.string.no_stock_available), Toast.LENGTH_SHORT).show()
                }
            }
            // Optional: load image if needed
            // Glide.with(binding.productImage.context).load(product.imageUrl).into(binding.productImage)
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): StockViewHolder {
        val binding = ProductItemSelectBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return StockViewHolder (binding)
    }

    override fun onBindViewHolder(holder: StockViewHolder, position: Int) {
        getItem(position)?.let { holder.bind(it) }
        //val product = getItem(position)
        //if (product != null) {
        //    holder.bind(product) // Use bind method to set up data
        //}
    }
}