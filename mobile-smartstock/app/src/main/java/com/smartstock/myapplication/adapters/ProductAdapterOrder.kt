package com.smartstock.myapplication.adapters

import android.util.Log
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.R
import com.smartstock.myapplication.databinding.ProductItemBinding
import com.smartstock.myapplication.models.Product

class ProductAdapterOrder(
    private val productList: List<Product>,
    private val onDeleteClick: (Product) -> Unit
) : RecyclerView.Adapter<ProductAdapterOrder.ProductViewHolder>() {

    inner class ProductViewHolder(private val binding: ProductItemBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(product: Product) {
            binding.product = product
            binding.onDeleteClick = onDeleteClick
            binding.executePendingBindings() // Optional: ensure bindings update immediately

            val context = binding.root.context
            val contentDescription = buildString {
                append(context.getString(R.string.desc_nombre_producto, product.name))
                append(". ")
                append(context.getString(R.string.desc_precio_unitario, product.currency_price, product.unit_price))
                append(". ")
                append(context.getString(R.string.desc_precio_promocional, product.currency_price, product.discount_price))
                append(". ")
                append(context.getString(R.string.desc_cantidad_disponible, product.quantity))
                if (product.description?.isNotEmpty() == true) {
                    append(". ")
                    append(context.getString(R.string.desc_producto, product.description))
                }
            }

            binding.root.contentDescription = contentDescription
            binding.deleteSelectedProductIcon?.let { deleteIcon ->
                deleteIcon.contentDescription = context.getString(
                    R.string.desc_boton_eliminar_producto,
                    product.name
                )
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        val binding = ProductItemBinding.inflate(inflater, parent, false)
        return ProductViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        holder.bind(productList[position])
    }

    override fun getItemCount(): Int = productList.size
}
