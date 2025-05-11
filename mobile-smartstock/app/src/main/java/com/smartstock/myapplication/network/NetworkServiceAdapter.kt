package com.smartstock.myapplication.network

import android.content.Context
import android.net.Uri
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
import com.smartstock.myapplication.models.ClientSimple
import com.smartstock.myapplication.models.ClientVisit
import com.smartstock.myapplication.models.CreatedOrder
import com.smartstock.myapplication.models.CreatedRecommendation
import com.smartstock.myapplication.models.CreatedRouteVisit
import com.smartstock.myapplication.models.CreatedUpload
import com.smartstock.myapplication.models.Manufacturer
import com.smartstock.myapplication.models.Order
import com.smartstock.myapplication.models.Product
import com.smartstock.myapplication.models.ProductVisit
import com.smartstock.myapplication.models.Recommendation
import com.smartstock.myapplication.models.RouteVisit
import com.smartstock.myapplication.models.SimpleProductName
import com.smartstock.myapplication.models.Stock
import com.smartstock.myapplication.models.Store
import com.smartstock.myapplication.models.User
import com.smartstock.myapplication.models.UserToken
import com.smartstock.myapplication.models.UserVerify
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.UUID
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException
import kotlin.coroutines.suspendCoroutine

open class NetworkServiceAdapter constructor(context: Context){

    companion object {
        const val INTERNAL_TOKEN = "internal_token"
        const val BASE_URL_USER_SESSIONS = "http://130.211.32.9/"
        const val BASE_URL_CLIENTS = "http://130.211.32.9/"
        const val BASE_URL_PRODUCTS_STOCK = "http://130.211.32.9/"
        //const val BASE_URL_PRODUCTS_STOCK ="https://3a07-186-29-181-170.ngrok-free.app/"
        const val BASE_URL_PRODUCTS = "http://130.211.32.9/"
        const val BASE_ROUTES = "http://130.211.32.9/"
        const val BASE_URL_MANUFACTURER = "http://130.211.32.9/manufacture-api/"
        const val BASE_URL_STORE = "http://130.211.32.9/stores/"
        const val BASE_URL_ORDER = "http://130.211.32.9/"
        const val BASE_URL_VIDEO = "http://130.211.32.9/"
        const val BASE_URL_DOCUMENT_MANAGER = "http://130.211.32.9/document-manager/"
        const val LOGIN_PATH = "user_sessions/login"
        const val CREATE_CLIENT_PATH = "user_sessions/create"
        const val GET_PRODUCT_STOCKS = "stocks-api/stocks/all"
        const val GET_ALL_PRODUCTS = "/products/paginated_full"
        const val CREATE_ORDER_PATH = "orders/create"
        const val VERIFY_PATH = "user_sessions/auth"
        const val GET_CLIENTS_SELLER_PATH = "user_sessions/clients/seller/"
        const val VIDEO_CREATE = "video/create"
        const val DOCUMENT_UPLOAD = "document/create"
        const val ROUTE_CREATE_VISIT = "routes/visits/create"
        const val GET_MANUFACTURERS_PAGINATED = "manufacturers/list"
        const val GET_STORES_PAGINATED = "paginated_full"
        const val GET_PRODUCTS_BY_CATEGORY_BY_MANUFACTURER = "products/category_manufacturer_paginated"
        const val GET_PRODUCTS_BY_ID_BY_STORE = "stocks-api/stocks/product_and_store"
        const val BASE_VISITS = "http://130.211.32.9/"
        const val GET_PAGINATED_VISITS = "visits/by-visit-date-paginated/"
        const val UNKNOWN = "unknown"
        val DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd")
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

    suspend fun addRouteVisit(routeVisit: RouteVisit, context: Context, token: String?) = suspendCoroutine { cont ->

        val jsonPayload = JSONObject()
        jsonPayload.put("client_id", routeVisit.client_id)
            .put("visit_date", routeVisit.visit_date)
            .put("description", routeVisit.description)
            .put("products", JSONArray(routeVisit.products.map {
                JSONObject().apply {
                    put("product_id", it.id)
                }
            }))
        requestQueue.add(
            postRequestWithToken(BASE_ROUTES,
                ROUTE_CREATE_VISIT,jsonPayload,context, token, { response ->
                    try{

                        val routeVisitCreated = CreatedRouteVisit(
                            clientId = UUID.fromString(response.optString("client_id")),
                            createdAt = response.optString("created_at"),
                            description = response.optString("description"),
                            id = UUID.fromString(response.optString("id")),
                            products = response.getJSONArray("products").let { jsonArray ->
                                List(jsonArray.length()) { index ->
                                    val productJson = jsonArray.getJSONObject(index)
                                    ProductVisit(
                                        id = UUID.fromString(productJson.optString("id")),
                                        productId = UUID.fromString(productJson.optString("product_id")),
                                        visitId = UUID.fromString(productJson.optString("visit_id")),
                                        createdAt = productJson.optString("created_at"),
                                        updatedAt = productJson.optString("updated_at")
                                    )
                                }
                            },
                            updatedAt = response.optString("updated_at"),
                            userId = UUID.fromString(response.optString("user_id")),
                            visitDate = response.optString("visit_date"),
                            sellerId = response.optString("seller_id"),
                        )
                        cont.resume(routeVisitCreated)
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
    suspend fun addRecomendation(recomendation: Recommendation, context: Context, token: String?) = suspendCoroutine { cont ->

        val jsonPayload = JSONObject()
        jsonPayload.put("document_id", recomendation.document_id)
            .put("file_path", recomendation.file_path)
            .put("store_id", recomendation.store_id)
            .put("tags", recomendation.tags)
            .put("enabled", recomendation.enabled)
            .put("update_date", recomendation.update_date)
            .put("creation_date", recomendation.creation_date)

        requestQueue.add(
            postRequestWithToken(BASE_URL_VIDEO,
                VIDEO_CREATE,jsonPayload,context, token, { response ->
                    try{
                        val videoCreated = CreatedRecommendation(
                            mensaje = response.optString("mensaje"),
                            resultado = Recommendation(
                                id = response.optString("id"),
                                document_id = response.optString("document_id"),
                                file_path = response.optString("file_path"),
                                tags = response.optString("file_path"),
                                store_id = null,
                                enabled = response.optBoolean("enabled"),
                                update_date = response.optString("update_date"),
                                creation_date = response.optString("creation_date"),
                            )
                        )
                        cont.resume(videoCreated)
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

    suspend fun fetchPaginatedProductsStocks(page: Int, perPage: Int): List<Stock> = suspendCoroutine { cont ->
        //val url = "$BASE_URL_PRODUCTS$GET_PRODUCT_PATH?page=$page&per_page=$perPage&sort_order=asc"
        val url = "$BASE_URL_PRODUCTS_STOCK"
        val path = "$GET_PRODUCT_STOCKS?page=$page&per_page=$perPage&sort_order=asc"

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

    suspend fun fetchPaginatedSimpleProductName(page: Int, perPage: Int) : List<SimpleProductName> = suspendCoroutine { cont ->

        val url = "$BASE_URL_PRODUCTS$GET_ALL_PRODUCTS"
        val path = "?page=$page&per_page=$perPage&sort_order=asc"

        requestQueue.add(
            getRequest(url, path, { response ->
                try{
                    val jsonArray = response.getJSONArray("data")
                    val products = mutableListOf<SimpleProductName>()
                    for (i in 0 until jsonArray.length()) {
                        val item = jsonArray.getJSONObject(i)
                        products.add(
                            SimpleProductName(
                                id = item.getString("id"),
                                name = item.getString("name")
                            )
                        )
                    }
                    cont.resume(products)
                } catch (e: Exception) {
                    //showToast(context.getString(R.string.error_database_integrity), context)
                    print(e.message)
                    cont.resumeWithException(e)
                }

            }, {
                cont.resumeWithException(it)
            })
        )
    }
    suspend fun fetchPaginatedStores(page: Int, perPage: Int) : List<Store> = suspendCoroutine { cont ->

        val url = "$BASE_URL_STORE$GET_STORES_PAGINATED"
        val path = "?page=$page&per_page=$perPage&sort_order=asc"

        requestQueue.add(
            getRequest(url, path, { response ->
                try{
                    val jsonArray = response.getJSONArray("data")
                    val stores = mutableListOf<Store>()
                    for (i in 0 until jsonArray.length()) {
                        val item = jsonArray.getJSONObject(i)
                        stores.add(
                            Store(
                                id = item.getString("id"),
                                name = item.getString("name")
                            )
                        )
                    }
                    cont.resume(stores)
                } catch (e: Exception) {
                    //showToast(context.getString(R.string.error_database_integrity), context)
                    print(e.message)
                    cont.resumeWithException(e)
                }

            }, {
                cont.resumeWithException(it)
            })
        )
    }


    suspend fun fetchStockByProductIdAndStoreId(
        productId: String?,
        storeId: String?,
        context: Context,
    ): Stock = suspendCoroutine { cont ->

        val url = "$BASE_URL_PRODUCTS_STOCK"
        val path = "$GET_PRODUCTS_BY_ID_BY_STORE?id_product=$productId&id_store=$storeId"

        requestQueue.add(
            getRequest(url, path, { response ->
                try{
                    val productJson = response.getJSONObject("product")
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
                        id = response.optString("id"),
                        quantity_in_stock = response.optInt("quantity_in_stock"),
                        product = product
                    )

                    cont.resume(stock)
                } catch (e: Exception) {
                    //showToast(context.getString(R.string.error_database_integrity), context)
                    cont.resumeWithException(e)
                }

            }, { error ->
                val networkResponse = error.networkResponse
                val errorMessage = extractVolleyErrorMessage(networkResponse, context)
                showToast(errorMessage, context)
                cont.resumeWithException(error)
            })
        )
    }


    suspend fun fetchPaginatedClientVisits(page: Int, perPage: Int, token : String? ) : List<ClientVisit> = suspendCoroutine { cont ->

        val todaysDate: String = LocalDateTime
            .now()
            .format(DATE_FORMATTER)

        val url = "$BASE_VISITS$GET_PAGINATED_VISITS$todaysDate"
        val path = "?page=$page&per_page=$perPage&sort_order=asc"

        requestQueue.add(
            getRequestWithToken(url, path, { response ->
                try{
                    val jsonArray = response.getJSONArray("data")
                    val clientVisits = mutableListOf<ClientVisit>()
                    for (i in 0 until jsonArray.length()) {
                        val item = jsonArray.getJSONObject(i)
                        val clientJson = item.getJSONObject("client")
                        clientVisits.add(
                            ClientVisit(
                                id = item.optString("id"),
                                description = item.optString("description"),
                                visitDate = item.optString("visit_date"),
                                sellerId = item.optString("seller_id"),
                                userId = item.optString("user_id"),
                                client =  ClientSimple(
                                    id = clientJson.optString("id"),
                                    name = clientJson.optString("name"),
                                    clientType = clientJson.optString("client_type"),
                                    zone = clientJson.optString("zone")
                                )
                            )
                        )
                    }
                    cont.resume(clientVisits)
                } catch (e: Exception) {
                    //showToast(context.getString(R.string.error_database_integrity), context)
                    print(e.message)
                    cont.resumeWithException(e)
                }

            }, {
                cont.resumeWithException(it)
            },
                token
            )
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

    private fun getRequestWithToken(
        base: String,
        path: String,
        responseListener: Response.Listener<JSONObject>,
        errorListener: Response.ErrorListener,
        token: String?
    ): JsonObjectRequest {
        return object : JsonObjectRequest(Method.GET, base + path,null, responseListener, errorListener) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
                headers["Authorization"] = "Bearer $token"
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

    suspend fun uploadVideoFile(
        context: Context,
        fileUri: Uri,
        token: String?
    ): CreatedUpload = suspendCoroutine { cont ->

        val contentResolver = context.contentResolver
        val inputStream = contentResolver.openInputStream(fileUri)
        val fileBytes = inputStream?.readBytes()

        if (fileBytes == null) {
            cont.resumeWithException(Exception("Cannot read selected file"))
            return@suspendCoroutine
        }

        val request = object : VolleyMultipartRequest(
            Method.POST,
            BASE_URL_DOCUMENT_MANAGER+ DOCUMENT_UPLOAD,
            { response ->
                try {
                    val jsonResponse = JSONObject(String(response.data))
                    val createdUpload = CreatedUpload(
                        id = jsonResponse.getString("id"),
                        file_name = jsonResponse.getString("file_name"),
                        path_source = jsonResponse.getString("path_source"),
                        user_id = jsonResponse.getString("user_id"),
                        created_at = jsonResponse.getString("created_at"),
                        updated_at = jsonResponse.getString("updated_at")
                    )
                    cont.resume(createdUpload)
                } catch (e: Exception) {
                    cont.resumeWithException(e)
                }
            },
            { error ->
                cont.resumeWithException(error)
            }
        ) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
                headers["Authorization"] = "Bearer $token"
                headers["x-token"] = INTERNAL_TOKEN
                return headers
            }

            override fun getByteData(): Map<String, DataPart> {
                val params = HashMap<String, DataPart>()
                params["file"] = DataPart("video.csv", fileBytes, "video/mp4")
                return params
            }
        }

        requestQueue.add(request)
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
                "stock not found" -> context.getString(R.string.error_stock_not_found)
                "id_store is required" -> context.getString(R.string.error_id_store_required)
                "id_product is required" -> context.getString(R.string.error_id_product_required)
                else -> context.getString(R.string.error_unknown)
            }
        } catch (e: Exception) {
            context.getString(R.string.error_database_integrity)
        }
    }
}
