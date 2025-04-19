package com.smartstock.myapplication.ui.client

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.models.Client
import com.smartstock.myapplication.repositories.ClientRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ClientViewModel(application: Application) : AndroidViewModel(application) {
    private val _client = MutableLiveData<Client>()
    private val _isSubmitting = MutableLiveData(false)
    val isSubmitting: LiveData<Boolean> get() = _isSubmitting

    private val _clientRepository = ClientRepository(
        application,
        AppDatabase.getDatabase(application.applicationContext).clientDao()
    )
    private val currentApp = application





    fun addNewClient(newClient: Client,token:String, onResult: (Boolean) -> Unit) {
        if (_isSubmitting.value == true) return // 🚫 Prevent duplicate requests

        _isSubmitting.value = true

        viewModelScope.launch(Dispatchers.IO) {
            try {
                _clientRepository.addClient(newClient, currentApp.applicationContext, token)

                onResult(true)  // Call the callback with success
            } catch (e: Exception) {
                println(e)
                e.printStackTrace() // Log the full stack trace


                onResult(false)  // Call the callback with failure
            }
            finally {
                _isSubmitting.postValue(false) // Reset flag after request
            }
        }
    }


    class Factory(val app: Application) : ViewModelProvider.Factory {
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            if (modelClass.isAssignableFrom(ClientViewModel::class.java)) {
                @Suppress("UNCHECKED_CAST")
                return ClientViewModel(app) as T
            }
            throw IllegalArgumentException("Unable to construct the view model")
        }
    }
}