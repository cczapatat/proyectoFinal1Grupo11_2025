package com.smartstock.myapplication.database.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.smartstock.myapplication.models.UserToken

@Dao
interface UserTokenDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertToken(userToken: UserToken)

    @Query("SELECT * FROM user_token LIMIT 1")
    fun getToken(): UserToken?

    @Query("DELETE FROM user_token")
    suspend fun clearToken()
}
