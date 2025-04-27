package com.smartstock.myapplication.ui.utils

import android.widget.TextView
import androidx.databinding.BindingAdapter
import com.smartstock.myapplication.R

@BindingAdapter("translatedClientType")
fun TextView.setTranslatedClientType(type: String?) {
    text = when (type) {
        "SUPERMARKET" -> context.getString(R.string.client_type_supermarket)
        "CORNER_STORE" -> context.getString(R.string.client_type_corner_store)
        else -> type ?: ""
    }
}