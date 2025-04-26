package com.smartstock.myapplication.repositories

import androidx.paging.Pager
import androidx.paging.PagingConfig
import androidx.paging.PagingData
import com.smartstock.myapplication.models.Product
import com.smartstock.myapplication.models.Stock
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.network.ProductPagingSource
import kotlinx.coroutines.flow.Flow

class ProductRepository (private val networkServiceAdapter: NetworkServiceAdapter) {
    fun getPaginatedProducts(): Flow<PagingData<Stock>> {
        return Pager(
            config = PagingConfig(pageSize = 10),
            pagingSourceFactory = {
                ProductPagingSource(networkServiceAdapter)
            }
        ).flow
    }
}