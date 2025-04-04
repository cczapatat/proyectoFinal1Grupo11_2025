package com.smartstock.myapplication.models

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "user_token")
data class UserToken(
    @PrimaryKey(autoGenerate = false) val userId: String,
    val token: String,
    val type: String,
)