package com.smartstock.myapplication.util

import android.widget.TextView
import androidx.databinding.BindingAdapter

object BindingAdapters {
    @JvmStatic
    @BindingAdapter("android:text")
    fun setTranslatedClientType(view: TextView, type: String?) {
        view.text = type ?: ""
    }
}

