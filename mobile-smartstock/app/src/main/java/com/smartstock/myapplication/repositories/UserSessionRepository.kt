package com.smartstock.myapplication.repositories

import android.app.Application
import com.smartstock.myapplication.database.dao.UserTokenDao


class UserSessionRepository(
    private val application: Application,
    private val userTokenDao: UserTokenDao
) {

    suspend fun getSavedToken(): String? {
        return this.userTokenDao.getToken()?.token

    }
    suspend fun getSavedUserId(): String? {
        return this.userTokenDao.getToken()?.userId

    }

    suspend fun deleteSavedToken() {
        this.userTokenDao.clearToken()
    }

}