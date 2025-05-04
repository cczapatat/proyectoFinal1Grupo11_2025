package com.smartstock.myapplication.models

import java.util.UUID


data class ProductVisit(
    val createdAt: String,
    val id: UUID,
    val productId: UUID,
    val updatedAt: String,
    val visitId: UUID,
)