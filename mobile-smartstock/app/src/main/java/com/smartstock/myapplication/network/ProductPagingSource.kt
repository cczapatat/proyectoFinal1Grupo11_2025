package com.smartstock.myapplication.network

import android.util.Log
import androidx.paging.PagingSource
import androidx.paging.PagingState
import com.smartstock.myapplication.models.Product

class ProductPagingSource (
    private val networkServiceAdapter: NetworkServiceAdapter
) : PagingSource<Int, Product>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Product> {
        val page = params.key ?: 1
        val perPage = 10
        Log.d("Paging", "Loading page 0...")
        return try {
            Log.d("Paging", "Loading page 1...")
            val productList = networkServiceAdapter.fetchPaginatedProducts(page, perPage)
            LoadResult.Page(
                data = productList,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (productList.isEmpty()) null else page + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, Product>): Int? {
        return state.anchorPosition?.let {
            state.closestPageToPosition(it)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(it)?.nextKey?.minus(1)
        }
    }
}