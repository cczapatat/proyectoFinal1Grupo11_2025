package com.smartstock.myapplication.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.R
import com.smartstock.myapplication.models.SimpleProductName

/**
 * A RecyclerView.Adapter for showing a list of selected SimpleProductName items.
 * Each item has a delete icon; tapping it invokes [onRemove].
 */
class SelectedProductAdapter(
    private val items: MutableList<SimpleProductName>,
    private val onRemove: (SimpleProductName) -> Unit
) : RecyclerView.Adapter<SelectedProductAdapter.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.simple_product_name_item, parent, false)
        return ViewHolder(view)
    }

    override fun getItemCount(): Int = items.size

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(items[position])
    }

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val nameText: TextView = itemView.findViewById(R.id.productListName)
        private val deleteIcon: ImageView = itemView.findViewById(R.id.deleteSelectedProductIcon)

        fun bind(item: SimpleProductName) {
            nameText.text = item.name
            deleteIcon.setOnClickListener {
                onRemove(item)
            }
        }
    }
}
