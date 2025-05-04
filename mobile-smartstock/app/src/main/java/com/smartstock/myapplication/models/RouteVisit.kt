package com.smartstock.myapplication.models

import com.google.type.DateTime

data class RouteVisit(
    val client_id: String,
    val description: String,
    val visit_date: String,
    val products: ArrayList<SimpleProductName>
)
