package com.smartstock.myapplication.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.accessibility.AccessibilityNodeInfo
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.R
import com.smartstock.myapplication.databinding.StockItemBinding
import com.smartstock.myapplication.models.Product

class StockSearchAdapter(
    private var productList: List<Product>
) : RecyclerView.Adapter<StockSearchAdapter.ProductViewHolder>() {

    fun setData(newList: List<Product>) {
        productList = newList
        notifyDataSetChanged()
    }

    inner class ProductViewHolder(private val binding: StockItemBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(product: Product) {
            binding.product = product
            binding.executePendingBindings()

            itemView.contentDescription = buildItemDescription(product)
            itemView.isFocusable = true
            itemView.isFocusableInTouchMode = true
        }
        private fun buildItemDescription(product: Product): String {
            val context = binding.root.context
            return "${product.name}. " +
                    "${context.getString(R.string.desc_precio_unitario, product.currency_price, product.unit_price)}. " +
                    "${context.getString(R.string.desc_precio_promocional, product.currency_price, product.discount_price)}." +
                    "${context.getString(R.string.desc_producto, product.description)}. " +
                    "${context.getString(R.string.desc_cantidad_disponible, product.quantity)}."
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        val binding = StockItemBinding.inflate(layoutInflater, parent, false)
        return ProductViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        holder.bind(productList[position])

        holder.itemView.setAccessibilityDelegate(object : View.AccessibilityDelegate() {
            override fun onInitializeAccessibilityNodeInfo(
                host: View,
                info: AccessibilityNodeInfo
            ) {
                super.onInitializeAccessibilityNodeInfo(host, info)
                info.collectionItemInfo = AccessibilityNodeInfo.CollectionItemInfo.obtain(
                    0,
                    1,
                    holder.adapterPosition,
                    1,
                    false
                )
            }
        })
    }

    override fun getItemCount(): Int = productList.size
}