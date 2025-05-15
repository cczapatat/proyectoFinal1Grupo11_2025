package com.smartstock.myapplication.models

import com.google.firebase.database.Exclude
import com.google.firebase.database.IgnoreExtraProperties

@IgnoreExtraProperties
data class NewsAlert(
    @get:Exclude var firebaseKey: String = "",

    val alarm_id: String = "",
    val maximum_value: Long? = null,
    val minimum_value: Long? = null,
    val new_stock_unit: Long? = null,
    val notes: String = "",
    val product_id: String = "",
    val stock_id: String = "",
    val trigger_id: String = ""

) {

    constructor() : this(
        firebaseKey = "",
        alarm_id = "",
        maximum_value = null,
        minimum_value = null,
        new_stock_unit = null,
        notes = "",
        product_id = "",
        stock_id = "",
        trigger_id = ""
    )
}