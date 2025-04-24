package com.smartstock.myapplication.models

import java.util.UUID

data class CreatedOrder(
    val id: UUID,
    val clientId: String,
    val sellerId: String
)
