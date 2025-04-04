package com.smartstock.myapplication

import android.content.Context
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
                R.id.RegisterClientFragment, R.id.RegistrarVisita -> {
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

        // Filter menu based on user type
        val isSeller = userType == "SELLER"
        popup.menu.findItem(R.id.RegisterClientFragment).isVisible = isSeller
        popup.menu.findItem(R.id.RegistrarVisita).isVisible = isSeller
        popup.menu.findItem(R.id.ListarClientes).isVisible = isSeller
        popup.menu.findItem(R.id.ConsultaProductos).isVisible = isSeller
        popup.menu.findItem(R.id.Pedidos).isVisible = isSeller
        popup.menu.findItem(R.id.CargarVideo).isVisible = isSeller
        popup.menu.findItem(R.id.CerrarSesion).isVisible = isSeller

        val isClient = userType == "CLIENT"
        popup.menu.findItem(R.id.ConsultaProductos).isVisible = isClient
        popup.menu.findItem(R.id.Pedidos).isVisible = isClient
        popup.menu.findItem(R.id.CargarVideo).isVisible = isClient
        popup.menu.findItem(R.id.CerrarSesion).isVisible = isClient

        popup.setOnMenuItemClickListener { menuItem: MenuItem ->
            when (menuItem.itemId) {
                R.id.RegisterClientFragment -> navController.navigate(R.id.RegisterClientFragment)
                R.id.RegistrarVisita -> navController.navigate(R.id.RegistrarVisita)
                R.id.ListarClientes -> navController.navigate(R.id.ListarClientes)
                R.id.ConsultaProductos -> navController.navigate(R.id.ConsultaProductos)
                R.id.Pedidos -> navController.navigate(R.id.Pedidos)
                R.id.CargarVideo -> navController.navigate(R.id.CargarVideo)
                R.id.CerrarSesion -> finish()  // Example: Close the app
            }
            true
        }

        popup.show()
    }

    /*override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onSupportNavigateUp(): Boolean {
        val navController = findNavController(R.id.nav_host_fragment_content_main)
        return navController.navigateUp(appBarConfiguration)
                || super.onSupportNavigateUp()
    }*/
}