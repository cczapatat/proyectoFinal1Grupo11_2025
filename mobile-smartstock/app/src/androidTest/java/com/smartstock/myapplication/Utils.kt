package com.smartstock.myapplication

import android.content.res.Resources

object Utils {

    fun getLocalizedText(key: String): String {
        val locale = Resources.getSystem().configuration.locales.get(0)
        return when (key) {
            "Menu Create Client" -> if (locale.language == "es") "Crear Cliente" else "Create client"
            "Menu List client" -> if (locale.language == "es") "Mis Clientes" else "My Clients"
            "Create" -> if (locale.language == "es") "Crear" else "Create"
            "client_type_supermarket" -> if (locale.language == "es") "Supermercado" else "Supermarket"
            "zone_south" -> if (locale.language == "es") "Sur" else "South"
            "registrar_cliente_seleccionar_zona" -> if (locale.language == "es") "Seleccionar zona" else "Select a zone"
            "registrar_cliente_seleccionar_tipo" -> if (locale.language == "es") "Seleccionar tipo" else "Select a type"
            "lista_de_clientes" -> if (locale.language == "es") "Lista de Clientes" else "Clients"
            "registrar_cliente" -> if (locale.language == "es") "Registrar Cliente" else "Register client"
            "create_order" -> if (locale.language == "es") "Crear Pedido" else "Create Order"
            "tipo_pago_ondelivery" -> if (locale.language == "es") "Pago contra entrega" else "On delivery payment"
            "add" -> if (locale.language == "es") "Agregar" else "Add"
            "clients" -> if (locale.language == "es") "Agregar" else "Clients"
            else -> key
        }
    }
}