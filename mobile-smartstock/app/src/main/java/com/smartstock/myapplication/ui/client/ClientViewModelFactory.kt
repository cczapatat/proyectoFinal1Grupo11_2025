package com.smartstock.myapplication.ui.client

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.smartstock.myapplication.network.NetworkServiceAdapter

class ClientViewModelFactory (
    private val serviceAdapter: NetworkServiceAdapter,
    private val sellerId: String
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return ClientViewModel(serviceAdapter, sellerId) as T
    }
}