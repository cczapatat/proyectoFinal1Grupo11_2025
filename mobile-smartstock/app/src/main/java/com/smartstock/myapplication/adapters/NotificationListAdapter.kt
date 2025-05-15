package com.smartstock.myapplication.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.databinding.ListItemNotificationBinding
import com.smartstock.myapplication.models.NewsAlert

class NotificationListAdapter : ListAdapter<NewsAlert, NotificationListAdapter.NotificationViewHolder>(NewsAlertDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): NotificationViewHolder {

        val binding = ListItemNotificationBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return NotificationViewHolder(binding)
    }


    override fun onBindViewHolder(holder: NotificationViewHolder, position: Int) {
        val newsAlertItem = getItem(position)
        holder.bind(newsAlertItem)
    }

    class NotificationViewHolder(private val binding: ListItemNotificationBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(newsAlert: NewsAlert) {
            // Set the notification text
            binding.textViewNotificationNotes.text = newsAlert.notes
            binding.root.setOnClickListener {

             }
        }
    }


    class NewsAlertDiffCallback : DiffUtil.ItemCallback<NewsAlert>() {

        override fun areItemsTheSame(oldItem: NewsAlert, newItem: NewsAlert): Boolean {
            return oldItem.alarm_id == newItem.alarm_id
        }
        override fun areContentsTheSame(oldItem: NewsAlert, newItem: NewsAlert): Boolean {
            return oldItem == newItem
        }
    }
}