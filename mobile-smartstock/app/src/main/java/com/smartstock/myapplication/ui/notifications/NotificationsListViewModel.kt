package com.smartstock.myapplication.ui.notifications

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.smartstock.myapplication.models.NewsAlert
import com.smartstock.myapplication.network.FirebaseNotificationService
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class NotificationsListViewModel(application: Application) : AndroidViewModel(application) {

    private val firebaseNotificationService = FirebaseNotificationService() // Instantiate your service

    // LiveData to hold the list of news alerts
    private val _newsAlerts = MutableLiveData<List<NewsAlert>>()
    val newsAlerts: LiveData<List<NewsAlert>> get() = _newsAlerts

    // LiveData to hold loading state
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> get() = _isLoading

    // LiveData for error messages
    private val _errorMessage = MutableLiveData<String?>()
    val errorMessage: LiveData<String?> get() = _errorMessage

    companion object {
        private const val TAG = "NotificationsListVM"
    }

    init {
        fetchAllNewsAlerts() // Fetch alerts when the ViewModel is created
    }

    fun fetchAllNewsAlerts() {
        viewModelScope.launch {
            _isLoading.value = true
            _errorMessage.value = null // Clear previous errors
            firebaseNotificationService.getAllNewsAlerts()
                .catch { exception ->
                    Log.e(TAG, "Error fetching all news alerts", exception)
                    _errorMessage.value = "Failed to load notifications: ${exception.localizedMessage}"
                    _isLoading.value = false
                }
                .collectLatest { alerts ->
                    _newsAlerts.value = alerts
                    _isLoading.value = false
                }
        }
    }

    /**
     * Call this to clear any displayed error message.
     */
    fun onErrorShown() {
        _errorMessage.value = null
    }
}