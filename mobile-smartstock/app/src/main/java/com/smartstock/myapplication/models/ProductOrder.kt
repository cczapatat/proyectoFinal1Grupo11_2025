package com.smartstock.myapplication.models

data class ProductOrder(
    val product_id: String,
    val units: Int? = 0
)