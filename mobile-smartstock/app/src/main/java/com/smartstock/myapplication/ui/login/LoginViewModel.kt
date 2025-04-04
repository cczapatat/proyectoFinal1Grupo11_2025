package com.smartstock.myapplication.ui.login

import android.content.Context
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.smartstock.myapplication.models.User
import com.smartstock.myapplication.network.NetworkServiceAdapter
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class LoginViewModel(private val context: Context) : ViewModel() {

    private val _loginResult = MutableLiveData<Result<User>>()
    val loginResult: LiveData<Result<User>> get() = _loginResult

    private val networkService = NetworkServiceAdapter.getInstance(context)


    fun login(user: User) {
        viewModelScope.launch(Dispatchers.Default) {
            try {
                val loggedInUser = networkService.login(user, context)
                _loginResult.postValue(Result.success(loggedInUser))
            } catch (e: Exception) {
                _loginResult.postValue(Result.failure(e))
            }
        }
    }

}
