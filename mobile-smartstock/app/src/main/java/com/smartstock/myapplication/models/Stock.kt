package com.smartstock.myapplication.models

data class Stock(
    val id: String,
    val quantity_in_stock: Int,
    val product: Product,
    var quantity: Int? = null
)
