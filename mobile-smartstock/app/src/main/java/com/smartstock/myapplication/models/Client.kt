package com.smartstock.myapplication.models

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.TypeConverters
import java.util.UUID

@Entity(tableName = "clients")
@TypeConverters(UUIDConverter::class)
data class Client(
    @PrimaryKey val id: UUID = UUID.randomUUID(),
    val name: String,
    val phone: String,
    val email: String,
    val userId: UUID,
    val sellerId: UUID,
    val address: String,
    val clientType: String,
    val zone: String
)