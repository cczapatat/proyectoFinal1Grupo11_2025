package com.smartstock.myapplication.repositories

import android.app.Application
import android.content.Context
import com.smartstock.myapplication.database.dao.ClientDao
import com.smartstock.myapplication.models.Client
import com.smartstock.myapplication.network.NetworkServiceAdapter

class ClientRepository(
    private val application: Application,
    private val clientDao: ClientDao) {

    suspend fun getClients(): List<Client> {
        //return NetworkServiceAdapter.getInstance(application).getClients()
        return emptyList()
    }

    suspend fun refreshDataForced(): List<Client> {
        //val clients = NetworkServiceAdapter.getInstance(application).getClients()
        this.clientDao.deleteAll()
        //this.clientDao.insertManyRaw(clients)
        //return clients
        return emptyList()
    }

    suspend fun addClient(client: Client, context:Context, token: String?): Client {
        val newClient = NetworkServiceAdapter.getInstance(application).addClient(client, context, token)
        this.clientDao.insert(newClient) // Store locally
        return newClient
    }
}
