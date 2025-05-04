package com.smartstock.myapplication.repositories

import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.PagingData
import com.smartstock.myapplication.models.SimpleProductName
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.network.SimpleProductNamePagingSource
import kotlinx.coroutines.flow.Flow

class SimpleProductNameRepository (private val networkServiceAdapter: NetworkServiceAdapter) {
    fun getPaginatedSimpleProducts(): Flow<PagingData<SimpleProductName>> {
        return Pager(
            config = PagingConfig(pageSize = 10),
            pagingSourceFactory = {
                SimpleProductNamePagingSource(networkServiceAdapter)
            }
        ).flow
    }
}