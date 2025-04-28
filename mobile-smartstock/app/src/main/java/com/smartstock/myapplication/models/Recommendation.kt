package com.smartstock.myapplication.models

import java.util.UUID

data class Recommendation(
    val id: String?,
    val document_id: String?,
    val file_path: String?,
    val store_id: String?,
    val tags:  String?,
    val enabled: Boolean,
    val update_date: String?,
    val creation_date: String?
)
