package com.smartstock.myapplication.models

data class Order(
    val client_id: String?,
    val delivery_date: String,
    val payment_method: String,
    val products: ArrayList<ProductOrder>
)

