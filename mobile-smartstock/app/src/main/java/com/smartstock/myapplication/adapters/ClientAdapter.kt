package com.smartstock.myapplication.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.paging.PagingDataAdapter
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.databinding.ClientItemBinding
import com.smartstock.myapplication.models.Client

class ClientAdapter (
    private val onSelectClick: (Client) -> Unit
) : PagingDataAdapter<Client, ClientAdapter.ClientViewHolder>(ClientComparator) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ClientViewHolder {
        val binding = ClientItemBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ClientViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ClientViewHolder, position: Int) {
        getItem(position)?.let { holder.bind(it) }
    }

    inner class ClientViewHolder(private val binding: ClientItemBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(client: Client) {
            binding.client = client
            binding.onSelectClick = onSelectClick
            binding.executePendingBindings()
        }
    }

    object ClientComparator : DiffUtil.ItemCallback<Client>() {
        override fun areItemsTheSame(oldItem: Client, newItem: Client) = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: Client, newItem: Client) = oldItem == newItem
    }
}