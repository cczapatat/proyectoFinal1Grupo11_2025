package com.smartstock.myapplication.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.paging.PagingDataAdapter
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.databinding.VisitItemBinding
import com.smartstock.myapplication.models.ClientVisit

class ClientVisitAdapter (
    private val onSelectClick: (ClientVisit) -> Unit
) : PagingDataAdapter<ClientVisit, ClientVisitAdapter.ClientViewHolder>(ClientComparator) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ClientViewHolder {
        val binding = VisitItemBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ClientViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ClientViewHolder, position: Int) {
        getItem(position)?.let { holder.bind(it) }
    }

    inner class ClientViewHolder(private val binding: VisitItemBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(visit: ClientVisit) {
            binding.visit = visit
            binding.onSelectClick = onSelectClick
            binding.executePendingBindings()
        }
    }

    object ClientComparator : DiffUtil.ItemCallback<ClientVisit>() {
        override fun areItemsTheSame(oldItem: ClientVisit, newItem: ClientVisit) = oldItem.id == newItem.id
        override fun areContentsTheSame(oldItem: ClientVisit, newItem: ClientVisit) = oldItem == newItem
    }
}