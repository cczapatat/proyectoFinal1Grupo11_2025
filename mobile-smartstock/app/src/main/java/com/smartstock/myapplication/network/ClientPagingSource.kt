package com.smartstock.myapplication.network

import androidx.paging.PagingSource
import androidx.paging.PagingState
import com.smartstock.myapplication.models.Client

class ClientPagingSource (
    private val sellerId: String,
    private val serviceAdapter: NetworkServiceAdapter
) : PagingSource<Int, Client>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Client> {
        return try {
            val page = params.key ?: 1
            val clients = serviceAdapter.fetchPaginatedClientsBySellerId(sellerId, page, params.loadSize)

            LoadResult.Page(
                data = clients,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (clients.isEmpty()) null else page + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, Client>): Int? {
        return state.anchorPosition?.let { state.closestPageToPosition(it)?.prevKey?.plus(1)
            ?: state.closestPageToPosition(it)?.nextKey?.minus(1) }
    }
}