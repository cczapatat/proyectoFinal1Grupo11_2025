package com.smartstock.myapplication.network

import android.util.Log
import androidx.paging.PagingSource
import androidx.paging.PagingState
import com.smartstock.myapplication.models.SimpleProductName

class SimpleProductNamePagingSource (
    private val networkServiceAdapter: NetworkServiceAdapter
) : PagingSource<Int, SimpleProductName>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, SimpleProductName> {
        val page = params.key ?: 1
        val perPage = 10
        Log.d("Paging", "Loading page 0...")
        return try {
            Log.d("Paging", "Loading page 1...")
            val simpleProductNameList = networkServiceAdapter.fetchPaginatedSimpleProductName(page, perPage)
            LoadResult.Page(
                data = simpleProductNameList,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (simpleProductNameList.isEmpty()) null else page + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, SimpleProductName>): Int? {
        return state.anchorPosition?.let {
            state.closestPageToPosition(it)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(it)?.nextKey?.minus(1)
        }
    }
}