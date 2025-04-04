package com.smartstock.myapplication.models

data class Reminders(
    val id: Int,
    val date: String,
    val hour: String,
    val description: String,
    val tone: String,
)
