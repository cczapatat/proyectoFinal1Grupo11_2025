package com.smartstock.myapplication.ui.clientVisit


import androidx.lifecycle.ViewModel

import androidx.lifecycle.viewModelScope
import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.cachedIn
import com.smartstock.myapplication.network.ClientVisitPagingSource

import com.smartstock.myapplication.network.NetworkServiceAdapter

class ClientVisitViewModel(private val networkServiceAdapter: NetworkServiceAdapter, private val token : String?) : ViewModel() {

    val clientsVisits = Pager(PagingConfig(pageSize = 10)) {
        ClientVisitPagingSource(networkServiceAdapter, token)
    }.flow.cachedIn(viewModelScope)
}