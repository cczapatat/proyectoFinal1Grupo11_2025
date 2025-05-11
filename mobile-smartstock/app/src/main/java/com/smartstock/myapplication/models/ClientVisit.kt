package com.smartstock.myapplication.models


data class ClientVisit(
    val id: String,
    val sellerId: String,
    val userId: String,
    val visitDate: String,
    val description : String,
    val client: ClientSimple
)