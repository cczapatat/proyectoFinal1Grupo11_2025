package com.smartstock.myapplication

import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.view.MenuItem
import android.view.View
import android.widget.PopupMenu
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.NavController
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.NavigationUI
import androidx.navigation.ui.setupWithNavController
import com.smartstock.myapplication.R
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.smartstock.myapplication.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private var currentDestination = 0

    private lateinit var navController: NavController
    private lateinit var binding: ActivityMainBinding
    private lateinit var sharedPreferences: SharedPreferences

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val bundle = intent.extras
        sharedPreferences = getSharedPreferences("CLL_APP", Context.MODE_PRIVATE)
        val userType = bundle?.getString("type", "CLIENT") ?: "CLIENT"
        sharedPreferences.edit().putString(
            "type", userType).apply()
        val userId = bundle?.getString("userId", "")
        sharedPreferences.edit().putString(
            "userId", userId).apply()
        val token = bundle?.getString("token", "")
        sharedPreferences.edit().putString(
            "token", token).apply()

        // Set up navigation with BottomNavigationView
        val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
        navController = navHostFragment.navController
        val bottomNavigationView = findViewById<BottomNavigationView>(R.id.bottom_navigation)

        // Connect BottomNavigationView to NavController
        bottomNavigationView.setupWithNavController(navController)

        // Handle menu clicks
        bottomNavigationView.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_menu -> {
                    showPopupMenu(bottomNavigationView.findViewById(R.id.nav_menu), userType)
                    return@setOnItemSelectedListener false  // Prevent default behavior
                }
                else -> {
                    NavigationUI.onNavDestinationSelected(item, navController)
                    return@setOnItemSelectedListener true
                }
            }
        }

        // Show/Hide BottomNavigationView based on the fragment
        navController.addOnDestinationChangedListener { _, destination, _ ->
            when (destination.id) {
                R.id.nav_clients, R.id.nav_menu -> {
                    bottomNavigationView.visibility = View.GONE
                }
                else -> {
                    bottomNavigationView.visibility = View.VISIBLE
                }
            }
        }

    }

    private fun showPopupMenu(anchorView: View, userType: String) {
        val popup = PopupMenu(this, anchorView)
        popup.menuInflater.inflate(R.menu.popup_menu, popup.menu)
        popup.menu.setGroupVisible(0, false)

        when (userType) {
            "SELLER" -> {
                popup.menu.findItem(R.id.RegisterClientFragment).isVisible = true
                popup.menu.findItem(R.id.RegistrarVisita).isVisible = true
                popup.menu.findItem(R.id.ListarClientes).isVisible = true
                popup.menu.findItem(R.id.ConsultaProductos).isVisible = true
                popup.menu.findItem(R.id.Pedidos).isVisible = true
                popup.menu.findItem(R.id.CargarVideo).isVisible = true

            }

            "CLIENT" -> {
                popup.menu.findItem(R.id.ConsultaProductos).isVisible = true
                popup.menu.findItem(R.id.Pedidos).isVisible = true
                popup.menu.findItem(R.id.CargarVideo).isVisible = true

            }
            // Filter menu based on user type
        }
        popup.menu.findItem(R.id.CerrarSesion).isVisible = true

        popup.setOnMenuItemClickListener { menuItem: MenuItem ->
            when (menuItem.itemId) {
                R.id.RegisterClientFragment -> navController.navigate(R.id.RegisterClientFragment)
                R.id.RegistrarVisita -> navController.navigate(R.id.RegistrarVisita)
                R.id.ListarClientes -> navController.navigate(R.id.ListarClientes)
                R.id.ConsultaProductos -> navController.navigate(R.id.ConsultaProductos)
                R.id.Pedidos -> navController.navigate(R.id.Pedidos)
                R.id.CargarVideo -> navController.navigate(R.id.CargarVideo)
                R.id.CerrarSesion -> closeSesion()
            }
            true
        }

        popup.show()
    }

    fun closeSesion(){
        sharedPreferences.edit().remove("type").apply()
        sharedPreferences.edit().remove("userId").apply()
        sharedPreferences.edit().remove("token").apply()
        val intent = Intent(this, LoginActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)

    }

}