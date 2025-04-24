package com.smartstock.myapplication

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.text.TextUtils
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.Observer
import androidx.lifecycle.lifecycleScope
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.databinding.FragmentLoginBinding
import com.smartstock.myapplication.models.User
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.LoginViewModelFactory
import com.smartstock.myapplication.repositories.UserSessionRepository
import com.smartstock.myapplication.ui.login.LoginViewModel
import kotlinx.coroutines.launch

class LoginActivity : AppCompatActivity() {

    private lateinit var binding: FragmentLoginBinding
    // Initialize ViewModel using the factory
    private val viewModel: LoginViewModel by viewModels { LoginViewModelFactory(this) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = FragmentLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.buttonLogin.setOnClickListener {
            val email = binding.email.text?.toString()?:""
            val password = binding.password.text?.toString()?:""
            val argsArray: ArrayList<String> = arrayListOf(email, password)
            if (this.formIsValid(argsArray)) {
                val user = User(email = email,password = password)
                viewModel.login(user)
            } else {
                showMessage(getString(R.string.error_login_fields),this)
            }
        }

        // Observe login result
        viewModel.loginResult.observe(this, Observer { result ->
            result.fold(
                onSuccess = { user ->
                    showMessage(getString(R.string.success_login), this)
                    goToMainActivity(user.type, user.user_id, user.token, user.id, user.name)

                },
                onFailure = {
                    showMessage(getString(R.string.error_login), this)
                }
            )
        })

    }

    private fun formIsValid(array: ArrayList<String>): Boolean {
        for (elem in array) {
            if (TextUtils.isEmpty(elem)) {
                return false
            }
        }
        return true
    }

    private fun showMessage(s: String, context: Context) {
        Toast.makeText(context, s, Toast.LENGTH_LONG).show()
    }

    private fun goToMainActivity(type: String, userId: String, token: String, id:String, name:String) {
        val intent = Intent(applicationContext, MainActivity::class.java)
        val sharedPref = getSharedPreferences("CLL_APP", MODE_PRIVATE)
        with(sharedPref.edit()) {
            clear() // clears all saved data
            apply()
        }
        intent.putExtra("type", type)
        intent.putExtra("userId", userId)
        intent.putExtra("token", token)
        intent.putExtra("id", id)
        intent.putExtra("name", name)

        startActivity(intent)
        finish()
    }

}