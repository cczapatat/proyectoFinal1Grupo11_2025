package com.smartstock.myapplication.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.databinding.ListItemNotificationBinding
import com.smartstock.myapplication.models.NewsAlert

class NotificationListAdapter : ListAdapter<NewsAlert, NotificationListAdapter.NotificationViewHolder>(NewsAlertDiffCallback()) {

    // Called when RecyclerView needs a new ViewHolder of the given type to represent an item.
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): NotificationViewHolder {
        // Inflate the layout for each list item using ViewBinding
        val binding = ListItemNotificationBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return NotificationViewHolder(binding)
    }

    // Called by RecyclerView to display the data at the specified position.
    override fun onBindViewHolder(holder: NotificationViewHolder, position: Int) {
        val newsAlertItem = getItem(position) // Get the NewsAlert object for this position
        holder.bind(newsAlertItem)
    }

    // ViewHolder class that holds the views for each list item.
    class NotificationViewHolder(private val binding: ListItemNotificationBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(newsAlert: NewsAlert) {
            // Set the notification text
            binding.textViewNotificationNotes.text = newsAlert.notes
            binding.root.setOnClickListener {
              // Handle item click
             }
        }
    }

    // DiffUtil.ItemCallback for calculating the differences between two non-null items in a list.
    // This helps RecyclerView efficiently update only the items that have changed.
    class NewsAlertDiffCallback : DiffUtil.ItemCallback<NewsAlert>() {
        // Called to check whether two objects represent the same item.
        // Use a stable, unique ID for this. alarm_id is perfect.
        override fun areItemsTheSame(oldItem: NewsAlert, newItem: NewsAlert): Boolean {
            return oldItem.alarm_id == newItem.alarm_id
        }

        // Called to check whether two items have the same data.
        // This is used to detect if the contents of an item have changed.
        // Since NewsAlert is a data class, its generated equals() method will compare all properties.
        override fun areContentsTheSame(oldItem: NewsAlert, newItem: NewsAlert): Boolean {
            return oldItem == newItem
        }
    }
}