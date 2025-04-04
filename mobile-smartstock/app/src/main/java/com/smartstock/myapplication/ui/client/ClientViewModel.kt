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
    private val _clientRepository = ClientRepository(
        application,
        AppDatabase.getDatabase(application.applicationContext).clientDao()
    )
    private val currentApp = application

    val clientAdded = SingleLiveEvent<Boolean>()

    var client: LiveData<Client>
        get() = _client


    private var _eventNetworkError = MutableLiveData(false)

    val eventNetworkError: LiveData<Boolean>
        get() = _eventNetworkError

    private var _isNetworkErrorShown = MutableLiveData(false)

    val isNetworkErrorShown: LiveData<Boolean>
        get() = _isNetworkErrorShown

    init {
        client = MutableLiveData()
    }

    fun onNetworkErrorShown() {
        _isNetworkErrorShown.value = true
    }

    fun addNewClient(newClient: Client, onResult: (Boolean) -> Unit) {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                _clientRepository.addClient(newClient, currentApp.applicationContext)
                _eventNetworkError.postValue(false)
                _isNetworkErrorShown.postValue(false)
                onResult(true)  // Call the callback with success
            } catch (e: Exception) {
                println(e)
                e.printStackTrace() // Log the full stack trace

                _eventNetworkError.postValue(true)
                _isNetworkErrorShown.postValue(true)
                onResult(false)  // Call the callback with failure
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