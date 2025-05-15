package com.smartstock.myapplication.ui.notifications

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.view.isVisible
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import com.smartstock.myapplication.adapters.NotificationListAdapter
import com.smartstock.myapplication.databinding.FragmentNotificationsListBinding // Generated from fragment_notifications_list.xml

/**
 * Fragment for displaying a list of notifications.
 */
class NotificationsListFragment : Fragment() {

    // ViewBinding property for accessing views in the layout
    private var _binding: FragmentNotificationsListBinding? = null
    private val binding get() = _binding!!

    // ViewModel for managing UI-related data
    private val viewModel: NotificationsListViewModel by viewModels()

    // Adapter for the RecyclerView
    private lateinit var notificationListAdapter: NotificationListAdapter

    /**
     * Inflates the layout for this fragment and initializes ViewBinding.
     */
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentNotificationsListBinding.inflate(inflater, container, false)
        return binding.root
    }

    /**
     * Called after the view has been created. Sets up the RecyclerView and observes ViewModel data.
     */
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        setupRecyclerView()
        observeViewModel()
    }

    /**
     * Configures the RecyclerView with a LinearLayoutManager and sets the adapter.
     */
    private fun setupRecyclerView() {
        notificationListAdapter = NotificationListAdapter()
        binding.recyclerViewNotifications.apply {
            layoutManager = LinearLayoutManager(context) // Sets a vertical list layout
            adapter = notificationListAdapter // Attaches the adapter
        }
    }

    /**
     * Observes LiveData from the ViewModel to update the UI based on data changes.
     */
    private fun observeViewModel() {

        // Observes the loading state and updates the visibility of the progress bar and RecyclerView
        viewModel.isLoading.observe(viewLifecycleOwner) { isLoading ->
            binding.progressBarNotifications.isVisible = isLoading
            binding.recyclerViewNotifications.isVisible = !isLoading && binding.textViewNotificationsError.isVisible.not()
        }

        // Observes error messages and displays them if present
        viewModel.errorMessage.observe(viewLifecycleOwner) { errorMessage ->
            binding.textViewNotificationsError.isVisible = errorMessage != null
            binding.textViewNotificationsError.text = errorMessage
            if (errorMessage != null) {
                binding.recyclerViewNotifications.isVisible = false
            }
        }

        // Observes the list of news alerts and updates the RecyclerView or error message accordingly
        viewModel.newsAlerts.observe(viewLifecycleOwner) { alerts ->
            if (alerts.isNullOrEmpty() && viewModel.isLoading.value == false && viewModel.errorMessage.value == null) {
                binding.textViewNotificationsError.text = "No se encontraron notificaciones." // Displays a default message if no alerts are found
                binding.textViewNotificationsError.isVisible = true
                binding.recyclerViewNotifications.isVisible = false
            } else if (!alerts.isNullOrEmpty()) {
                binding.textViewNotificationsError.isVisible = false
                binding.recyclerViewNotifications.isVisible = true
            }
            notificationListAdapter.submitList(alerts) // Updates the adapter with the new list
        }
    }

    /**
     * Cleans up resources when the view is destroyed.
     */
    override fun onDestroyView() {
        super.onDestroyView()
        binding.recyclerViewNotifications.adapter = null // Detaches the adapter to prevent memory leaks
        _binding = null // Clears the binding reference
    }
}