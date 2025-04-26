package com.smartstock.myapplication.network

import android.content.Context
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.Response
import com.android.volley.VolleyError
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.smartstock.myapplication.R
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.models.Client
import com.smartstock.myapplication.models.CreatedOrder
import com.smartstock.myapplication.models.Order
import com.smartstock.myapplication.models.Product
import com.smartstock.myapplication.models.Stock
import com.smartstock.myapplication.models.User
import com.smartstock.myapplication.models.UserToken
import com.smartstock.myapplication.models.UserVerify
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject
import java.util.UUID
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException
import kotlin.coroutines.suspendCoroutine

class NetworkServiceAdapter constructor(context: Context){

    companion object {
        const val INTERNAL_TOKEN = "internal_token"
        const val BASE_URL_USER_SESSIONS = "http://130.211.32.9/"
        const val BASE_URL_CLIENTS = "http://130.211.32.9/"
        const val BASE_URL_PRODUCTS = "http://130.211.32.9/"
        //const val BASE_URL_PRODUCTS = "http://130.211.32.9/"
        const val BASE_URL_ORDER = "http://130.211.32.9/"
        //const val BASE_URL_ORDER = "http://130.211.32.9/"
        const val LOGIN_PATH = "user_sessions/login"
        const val CREATE_CLIENT_PATH = "user_sessions/create"
        const val GET_PRODUCT_PATH = "stocks-api/stocks/all"
        const val CREATE_ORDER_PATH = "orders/create"
        const val VERIFY_PATH = "user_sessions/auth"
        const val GET_CLIENTS_SELLER_PATH = "user_sessions/clients/seller/"
        const val UNKNOWN = "unknown"
        const val COVER_UNKNOWN =
            "https://www.alleganyco.gov/wp-content/uploads/unknown-person-icon-Image-from.png"
        private var instance: NetworkServiceAdapter? = null
        fun getInstance(context: Context) = instance ?: synchronized(this) {
            instance ?: NetworkServiceAdapter(context).also {
                instance = it
            }
        }
    }

    private val requestQueue: RequestQueue by lazy {
        Volley.newRequestQueue(context.applicationContext)
    }

    suspend fun login(user: User, context: Context) = suspendCoroutine { cont ->
        val jsonPayload = JSONObject()
        jsonPayload.put("email", user.email).put("password", user.password)

        requestQueue.add(
            postRequestNoToken(BASE_URL_USER_SESSIONS, LOGIN_PATH, jsonPayload, { response ->
                val userLoggedIn = User(
                    id = response.optString("id"),
                    user_id = response.optString("user_id"),
                    token = response.optString("token"),
                    name = response.optString("name"),
                    type = response.optString("type"),
                    phone = response.optString("phone"),
                    email = response.optString("email"),
                    zone = response.optString("zone"),
                )
                // Save token to database
                CoroutineScope(Dispatchers.IO).launch {
                    val db = AppDatabase.getDatabase(context)
                    db.userTokenDao().clearToken()
                    db.userTokenDao().insertToken(UserToken(userLoggedIn.user_id,
                        userLoggedIn.token, userLoggedIn.type))
                }

                cont.resume(userLoggedIn)
            }, {
                cont.resumeWithException(it)
            })
        )
    }

    suspend fun addClient(client: Client, context: Context, token: String?) = suspendCoroutine { cont ->

        val jsonPayload = JSONObject()
        jsonPayload.put("name", client.name)
            .put("phone", client.phone)
            .put("email", client.email)
            .put("password", "1234567")
            .put("type", "CLIENT")
            .put("seller_id", client.sellerId)
            .put("address", client.address)
            .put("client_type", client.clientType)
            .put("zone", client.zone)

        requestQueue.add(
            postRequestWithToken(BASE_URL_CLIENTS,CREATE_CLIENT_PATH,jsonPayload,context,token, { response ->
                try{
                    val clientCreated = Client(
                        id = UUID.fromString(response.optString("id")),
                        name = response.optString("name"),
                        phone = response.optString("phone"),
                        zone = response.optString("zone"),
                        email = response.optString("email"),
                        clientType = response.optString("client_type"),
                        address = response.optString("address"),
                        sellerId = client.sellerId,
                        userId = UUID.fromString(response.optString("user_id")),
                    )
                    cont.resume(clientCreated)
                } catch (e: Exception) {
                    //showToast(context.getString(R.string.error_database_integrity), context)
                    cont.resumeWithException(e)
                }

            }) { error ->
                val networkResponse = error.networkResponse
                val errorMessage = extractVolleyErrorMessage(networkResponse, context)
                showToast(errorMessage, context)
                cont.resumeWithException(error)
            }
        )
    }

    suspend fun addOrder(order: Order, context: Context, token: String?) = suspendCoroutine { cont ->

        val jsonPayload = JSONObject()
        jsonPayload.put("client_id", order.client_id)
            .put("delivery_date", order.delivery_date)
            .put("payment_method", order.payment_method)
            .put("products", JSONArray(order.products.map {
                JSONObject().apply {
                    put("product_id", it.product_id)
                    put("units", it.units)
                }
            }))

        requestQueue.add(
            postRequestWithToken(BASE_URL_ORDER,CREATE_ORDER_PATH,jsonPayload,context, token, { response ->
                try{
                    val orderCreated = CreatedOrder(
                        id = UUID.fromString(response.optString("id")),
                        clientId = response.optString("client_id"),
                        sellerId = response.optString("seller_id"),
                    )
                    cont.resume(orderCreated)
                } catch (e: Exception) {
                    //showToast(context.getString(R.string.error_database_integrity), context)
                    cont.resumeWithException(e)
                }
            }) { error ->
                val networkResponse = error.networkResponse
                val errorMessage = extractVolleyErrorMessage(networkResponse, context)
                showToast(errorMessage, context)
                cont.resumeWithException(error)
            }
        )
    }

    suspend fun fetchPaginatedProducts(page: Int, perPage: Int): List<Stock> = suspendCoroutine { cont ->
        //val url = "$BASE_URL_PRODUCTS$GET_PRODUCT_PATH?page=$page&per_page=$perPage&sort_order=asc"
        val url = "$BASE_URL_PRODUCTS"
        val path = "$GET_PRODUCT_PATH?page=$page&per_page=$perPage&sort_order=asc"

        requestQueue.add(
            getRequest(url, path, { response ->
                try{
                    val jsonArray = response.getJSONArray("stocks")
                    val stocks = mutableListOf<Stock>()
                    for (i in 0 until jsonArray.length()) {
                        val stockItem = jsonArray.getJSONObject(i)
                        val productJson = stockItem.getJSONObject("product")
                        val product = Product(
                            id = productJson.optString("id"),
                            manufacturer_id = productJson.optString("manufacturer_id"),
                            name = productJson.optString("name"),
                            description = productJson.optString("description"),
                            category = productJson.optString("category"),
                            unit_price = productJson.optDouble("unit_price"),
                            currency_price = productJson.optString("currency_price"),
                            is_promotion = productJson.optBoolean("is_promotion"),
                            discount_price = productJson.optDouble("discount_price"),
                            expired_at = productJson.optString("expired_at"),
                            url_photo = productJson.optString("url_photo"),
                            store_conditions = productJson.optString("store_conditions")
                        )
                        val stock = Stock(
                            id = stockItem.optString("id"),
                            quantity_in_stock = stockItem.optInt("quantity_in_stock"),
                            product = product
                        )
                        stocks.add(
                            stock
                        )
                    }
                    cont.resume(stocks)
                } catch (e: Exception) {
                    //showToast(context.getString(R.string.error_database_integrity), context)
                    cont.resumeWithException(e)
                }

            }, {
                cont.resumeWithException(it)
            })
        )
    }

    suspend fun fetchPaginatedClientsBySellerId(
        sellerId: String,
        page: Int,
        perPage: Int,
        sortBy: String = "name",
        sortOrder: String = "asc"
    ): List<Client> = suspendCoroutine { cont ->

        val url = "$BASE_URL_USER_SESSIONS"
        val path = "$GET_CLIENTS_SELLER_PATH$sellerId?page=$page&per_page=$perPage&sort_by=$sortBy&sort_order=$sortOrder"

        requestQueue.add(
            getRequest(url, path, { response ->
                try{
                    val jsonArray = response.getJSONArray("data")
                    val clients = mutableListOf<Client>()
                    for (i in 0 until jsonArray.length()) {
                        val item = jsonArray.getJSONObject(i)
                        val sellerId = if (item.has("seller_id") && !item.isNull("seller_id")) {
                            UUID.fromString(item.getString("seller_id"))
                        } else {
                            null // or -1 or 0 if your Client class expects a non-null Int
                        }
                        clients.add(
                            Client(
                                id = UUID.fromString(item.getString("id")),
                                name = item.getString("name"),
                                phone = item.getString("phone"),
                                email = item.getString("email"),
                                userId = UUID.fromString(item.getString("user_id")),
                                sellerId = sellerId,
                                address = item.getString("address"),
                                clientType = item.getString("client_type"),
                                zone = item.getString("zone")
                            )
                        )
                    }
                    cont.resume(clients)
                } catch (e: Exception) {
                    //showToast(context.getString(R.string.error_database_integrity), context)
                    cont.resumeWithException(e)
                }

            }, {
                cont.resumeWithException(it)
            })
        )
    }

    suspend fun verifyUser(token:String) = suspendCoroutine { cont ->

        requestQueue.add(
            getRequest(BASE_URL_USER_SESSIONS, VERIFY_PATH, { response ->
                val verifiedUser = UserVerify(
                    user_session_id = response.optString("user_session_id"),
                    user_id = response.optString("user_id"),
                    user_type = response.optString("user_type")
                )
                cont.resume(verifiedUser)
            }, {
                cont.resumeWithException(it)
            })
        )
    }

    private fun getRequest(
        base: String,
        path: String,
        responseListener: Response.Listener<JSONObject>,
        errorListener: Response.ErrorListener
    ): JsonObjectRequest {
        return object : JsonObjectRequest(Method.GET, base + path,null, responseListener, errorListener) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
                //headers["Authorization"] = "Bearer $token"
                headers["content-type"] = "application/json"
                headers["x-token"] = INTERNAL_TOKEN
                return headers
            }

        }
    }

    private fun postRequestNoToken(
        base: String,
        path: String,
        body: JSONObject,
        responseListener: Response.Listener<JSONObject>,
        errorListener: Response.ErrorListener
    ): JsonObjectRequest {
        return object : JsonObjectRequest(
            Request.Method.POST, base + path, body, responseListener, errorListener
        ) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
                headers["content-type"] = "application/json"
                headers["x-token"] = INTERNAL_TOKEN
                return headers
            }
            override fun parseNetworkResponse(response: com.android.volley.NetworkResponse?): Response<JSONObject> {
                return if (response?.statusCode == 401) {
                    Response.error(VolleyError("Unauthorized - 401"))
                } else {
                    super.parseNetworkResponse(response)
                }
            }
        }
    }

    private fun postRequestWithToken(
        base: String,
        path: String,
        body: JSONObject,
        context: Context,
        token: String?,
        responseListener: Response.Listener<JSONObject>,
        errorListener: Response.ErrorListener
    ): JsonObjectRequest {
        //


        println("POST URL*******************: $base$path")
        println("POST Headers******************: Authorization=Bearer $token")
        println("POST Body**********************: $body")

        return object : JsonObjectRequest(Method.POST, base + path, body, responseListener, errorListener) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
                headers["Authorization"] = "Bearer $token"
                headers["Content-Type"] = "application/json"
                headers["x-token"] = INTERNAL_TOKEN
                return headers
            }
            override fun parseNetworkResponse(response: com.android.volley.NetworkResponse?): Response<JSONObject> {

                return if (response?.statusCode == 401) {
                    Response.error(VolleyError("Unauthorized - 401"))
                } else if (response?.statusCode == 400){
                    val errorMessage = extractVolleyErrorMessage(response, context)
                    Response.error(VolleyError(errorMessage))
                }
                else if (response?.statusCode == 409){
                    Response.error(VolleyError("Conflict in DB - 409"))
                }
                else if (response?.statusCode == 500){
                    Response.error(VolleyError("Error in system - 500"))
                }
                else {
                    super.parseNetworkResponse(response)
                }
            }
        }
    }

    private fun showToast(message: String, context: Context) {
        Toast.makeText(context, message, Toast.LENGTH_LONG).show()
    }

    private fun extractVolleyErrorMessage(response: com.android.volley.NetworkResponse?, context: Context): String {
        return try {
            val responseData = response?.data
            val errorString = responseData?.let { String(it) } ?: "{}"
            val jsonObject = JSONObject(errorString)
            val apiMessage = jsonObject.optString("message", "Unknown error")

            // Map API message to localized string
            when (apiMessage) {
                "user_id is required" -> context.getString(R.string.error_user_id_required)
                "seller_id is required" -> context.getString(R.string.error_seller_id_required)
                "name is required" -> context.getString(R.string.error_name_required)
                "phone is required" -> context.getString(R.string.error_phone_required)
                "email is required" -> context.getString(R.string.error_email_required)
                "address is required" -> context.getString(R.string.error_address_required)
                "client_type is required" -> context.getString(R.string.error_client_type_required)
                "zone is required" -> context.getString(R.string.error_zone_required)
                "Email already exists"-> context.getString(R.string.error_email_exists)
                "Phone already exists"-> context.getString(R.string.error_phone_exists)
                "Client already exists"-> context.getString(R.string.error_client_exists)
                "Email format is not valid"-> context.getString(R.string.error_email_format)
                "Phone format is not valid"-> context.getString(R.string.error_phone_format)
                else -> context.getString(R.string.error_unknown)
            }
        } catch (e: Exception) {
            context.getString(R.string.error_database_integrity)
        }
    }
}