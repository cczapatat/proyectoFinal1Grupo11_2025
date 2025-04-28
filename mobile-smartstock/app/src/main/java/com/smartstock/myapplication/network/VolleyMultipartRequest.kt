package com.smartstock.myapplication.network

import com.android.volley.AuthFailureError
import com.android.volley.NetworkResponse
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.VolleyError
import com.android.volley.toolbox.HttpHeaderParser
import java.io.ByteArrayOutputStream
import java.io.DataOutputStream
import java.io.IOException

abstract class VolleyMultipartRequest (
    method: Int,
    url: String,
    private val listener: Response.Listener<NetworkResponse>,
    errorListener: Response.ErrorListener
) : Request<NetworkResponse>(method, url, errorListener) {

    override fun getBodyContentType() = "multipart/form-data;boundary=$boundary"

    @Throws(AuthFailureError::class)
    override fun getBody(): ByteArray {
        val bos = ByteArrayOutputStream()
        val dos = DataOutputStream(bos)

        try {
            // Populate data
            for ((key, dataPart) in getByteData()) {
                buildPart(dos, key, dataPart)
            }
            // End boundary
            dos.writeBytes("--$boundary--\r\n")
        } catch (e: IOException) {
            e.printStackTrace()
        }

        return bos.toByteArray()
    }

    override fun parseNetworkResponse(response: NetworkResponse): Response<NetworkResponse> {
        return try {
            Response.success(response, HttpHeaderParser.parseCacheHeaders(response))
        } catch (e: Exception) {
            Response.error(VolleyError(e))
        }
    }

    override fun deliverResponse(response: NetworkResponse) {
        listener.onResponse(response)
    }

    abstract fun getByteData(): Map<String, DataPart>

    private fun buildPart(dos: DataOutputStream, parameterName: String, dataFile: DataPart) {
        try {
            dos.writeBytes("--$boundary\r\n")
            dos.writeBytes("Content-Disposition: form-data; name=\"$parameterName\"; filename=\"${dataFile.fileName}\"\r\n")
            if (dataFile.type != null) {
                dos.writeBytes("Content-Type: ${dataFile.type}\r\n")
            }
            dos.writeBytes("\r\n")

            val fileData = dataFile.content
            dos.write(fileData)

            dos.writeBytes("\r\n")
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }

    data class DataPart(val fileName: String, val content: ByteArray, val type: String? = null)

    companion object {
        private var boundary = "apiclient-${System.currentTimeMillis()}"
    }
}