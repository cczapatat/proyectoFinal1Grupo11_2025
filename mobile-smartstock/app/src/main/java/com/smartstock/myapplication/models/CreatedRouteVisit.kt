package com.smartstock.myapplication.models

import java.util.UUID


data class CreatedRouteVisit(
    val clientId: UUID,
    val createdAt: String,
    val description: String,
    val id: UUID,
    val products: List<ProductVisit>,
    val updatedAt: String,
    val sellerId: String,
    val userId: UUID,
    val visitDate: String,
)
