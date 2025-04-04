package com.smartstock.myapplication.ui.client
import android.view.View
class ThrottleClickListener (
    private val interval: Long = 1000L, // Default 1-second interval
    private val onClick: (View) -> Unit
) : View.OnClickListener {

    private var lastClickTime: Long = 0

    override fun onClick(v: View) {
        val currentTime = System.currentTimeMillis()
        if (currentTime - lastClickTime >= interval) {
            lastClickTime = currentTime
            onClick(v)
        }
    }
}

// Extension function for easy usage
fun View.setOnThrottleClickListener(interval: Long = 1000L, onClick: (View) -> Unit) {
    val listener = ThrottleClickListener(interval, onClick)
    setOnClickListener(listener)
}
