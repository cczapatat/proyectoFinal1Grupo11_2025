package com.smartstock.myapplication.ui.client


import androidx.lifecycle.ViewModel

import androidx.lifecycle.viewModelScope
import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.cachedIn
import com.smartstock.myapplication.network.ClientPagingSource

import com.smartstock.myapplication.network.NetworkServiceAdapter

class ClientViewModel(private val networkServiceAdapter: NetworkServiceAdapter, private val sellerId: String) : ViewModel() {

    val clients = Pager(PagingConfig(pageSize = 10)) {
        ClientPagingSource(sellerId, networkServiceAdapter)
    }.flow.cachedIn(viewModelScope)
}