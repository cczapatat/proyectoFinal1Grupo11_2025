package com.smartstock.myapplication.models

import java.util.UUID

data class CreatedUpload(
    val id: String,
    val file_name: String,
    val path_source: String,
    val user_id: String,
    val created_at: String,
    val updated_at: String
    )
