package com.smartstock.myapplication.database.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.smartstock.myapplication.models.Client

@Dao
interface ClientDao {
    @Query("SELECT * FROM clients")
    suspend fun getAll(): List<Client>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(client: Client)

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertManyRaw(albums: List<Client>): List<Long>


    @Query("DELETE FROM clients")
    suspend fun deleteAll()
}