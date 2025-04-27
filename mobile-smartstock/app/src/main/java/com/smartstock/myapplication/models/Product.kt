package com.smartstock.myapplication.models



data class Product(
    var id: String,
    val manufacturer_id: String,
    val name: String,
    val description: String,
    val category: String,
    val unit_price: Double,
    val currency_price: String,
    val is_promotion: Boolean,
    val discount_price: Double,
    val expired_at: String,
    val url_photo: String,
    val store_conditions: String,
    var quantity: Int? = null
)