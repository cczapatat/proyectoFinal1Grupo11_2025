package com.smartstock.myapplication.network

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.widget.Toast
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.Response
import com.android.volley.VolleyError
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.smartstock.myapplication.R
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.models.Client
import com.smartstock.myapplication.models.User
import com.smartstock.myapplication.models.UserToken
import com.smartstock.myapplication.models.UserVerify
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject
import java.util.UUID
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException
import kotlin.coroutines.suspendCoroutine

class NetworkServiceAdapter constructor(context: Context){

    companion object {
        const val INTERNAL_TOKEN = "internal_token"
        const val BASE_URL_USER_SESSIONS = "http://192.168.0.5:3008/"
        const val BASE_URL_CLIENTS = "http://192.168.0.5:3008/"
        const val LOGIN_PATH = "user_sessions/login"
        const val CREATE_CLIENT_PATH = "user_sessions/create"
        const val VERIFY_PATH = "user_sessions/auth"
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
                    db.userTokenDao().insertToken(UserToken(userLoggedIn.user_id,
                        userLoggedIn.token, userLoggedIn.type))
                }

                cont.resume(userLoggedIn)
            }, {
                cont.resumeWithException(it)
            })
        )
    }

    suspend fun addClient(client: Client, context: Context) = suspendCoroutine { cont ->

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
            postRequestWithToken(BASE_URL_CLIENTS,CREATE_CLIENT_PATH,jsonPayload,context, { response ->
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

            },  {error ->
                val networkResponse = error.networkResponse
                val errorMessage = extractVolleyErrorMessage(networkResponse, context)
                showToast(errorMessage, context)
                cont.resumeWithException(error)
            })
        )
    }

    suspend fun verifyUser(token:String) = suspendCoroutine { cont ->

        requestQueue.add(
            getRequest(BASE_URL_USER_SESSIONS, VERIFY_PATH, token, { response ->
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
        token: String,
        responseListener: Response.Listener<JSONObject>,
        errorListener: Response.ErrorListener
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

    private fun postRequestWithToken(
        base: String,
        path: String,
        body: JSONObject,
        context: Context,
        responseListener: Response.Listener<JSONObject>,
        errorListener: Response.ErrorListener
    ): JsonObjectRequest {
        //
        // val token = getSavedToken(context) ?: ""

        println("POST URL*******************: $base$path")
        //println("POST Headers******************: Authorization=Bearer $token")
        println("POST Body**********************: $body")

        return object : JsonObjectRequest(Method.POST, base + path, body, responseListener, errorListener) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
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