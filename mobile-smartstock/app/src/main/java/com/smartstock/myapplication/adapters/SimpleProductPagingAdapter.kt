package com.smartstock.myapplication.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.paging.PagingDataAdapter
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.R
import com.smartstock.myapplication.models.SimpleProductName

/**
 * A PagingDataAdapter for displaying SimpleProductName items.
 * Touching an item invokes [onClick].
 */
class SimpleProductPagingAdapter(
    private val onClick: (SimpleProductName) -> Unit
) : PagingDataAdapter<SimpleProductName, SimpleProductPagingAdapter.ViewHolder>(DIFF_CALLBACK) {

    companion object {
        private val DIFF_CALLBACK = object : DiffUtil.ItemCallback<SimpleProductName>() {
            override fun areItemsTheSame(oldItem: SimpleProductName, newItem: SimpleProductName): Boolean =
                oldItem.id == newItem.id

            override fun areContentsTheSame(oldItem: SimpleProductName, newItem: SimpleProductName): Boolean =
                oldItem == newItem
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.simple_product_name_item, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = getItem(position) ?: return
        holder.bind(item)
    }

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val nameText: TextView = itemView.findViewById(R.id.productListName)

        fun bind(item: SimpleProductName) {
            nameText.text = item.name
            itemView.setOnClickListener { onClick(item) }
        }
    }
}
