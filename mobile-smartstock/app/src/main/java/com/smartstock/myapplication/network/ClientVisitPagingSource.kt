package com.smartstock.myapplication.network

import androidx.paging.PagingSource
import androidx.paging.PagingState
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.models.ClientVisit

class ClientVisitPagingSource (private val serviceAdapter: NetworkServiceAdapter, private val token: String?
) : PagingSource<Int, ClientVisit>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, ClientVisit> {
        return try {
            val page = params.key ?: 1
            val clientVisits = serviceAdapter.fetchPaginatedClientVisits(page, params.loadSize, token)
            LoadResult.Page(
                data = clientVisits,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (clientVisits.isEmpty()) null else page + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, ClientVisit>): Int? {
        return state.anchorPosition?.let { state.closestPageToPosition(it)?.prevKey?.plus(1)
            ?: state.closestPageToPosition(it)?.nextKey?.minus(1) }
    }
}