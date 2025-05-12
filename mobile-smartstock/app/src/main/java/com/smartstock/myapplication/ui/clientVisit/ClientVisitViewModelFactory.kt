package com.smartstock.myapplication.ui.clientVisit

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.smartstock.myapplication.network.NetworkServiceAdapter

class ClientVisitViewModelFactory (
    private val serviceAdapter: NetworkServiceAdapter,
    private val token: String?
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return ClientVisitViewModel(serviceAdapter, token) as T
    }
}