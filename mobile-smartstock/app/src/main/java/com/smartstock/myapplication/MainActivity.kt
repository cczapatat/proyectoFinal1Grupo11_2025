package com.smartstock.myapplication

import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.util.Log
import android.view.MenuItem
import android.view.View
import android.widget.PopupMenu
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContentProviderCompat.requireContext
import androidx.lifecycle.lifecycleScope
import androidx.navigation.NavController
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.NavigationUI
import androidx.navigation.ui.setupWithNavController
import com.smartstock.myapplication.R
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.databinding.ActivityMainBinding
import com.smartstock.myapplication.repositories.UserSessionRepository
import com.smartstock.myapplication.network.FirebaseNotificationService
import com.smartstock.myapplication.util.NotificationTracker
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    private var currentDestination = 0

    private lateinit var navController: NavController
    private lateinit var binding: ActivityMainBinding
    private lateinit var sharedPreferences: SharedPreferences
    private lateinit var bottomNavigationView: BottomNavigationView

    private val firebaseNotificationService = FirebaseNotificationService()
    private lateinit var notificationTracker: NotificationTracker
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        notificationTracker = NotificationTracker(applicationContext)

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
        val id = bundle?.getString("id", "")
        sharedPreferences.edit().putString(
            "id", id).apply()
        val name = bundle?.getString("name", "")
        sharedPreferences.edit().putString(
            "name", name).apply()

        // Set up navigation with BottomNavigationView
        val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
        navController = navHostFragment.navController
        bottomNavigationView = findViewById<BottomNavigationView>(R.id.bottom_navigation)

        // Connect BottomNavigationView to NavController
        bottomNavigationView.setupWithNavController(navController)

        // Handle menu clicks
        bottomNavigationView.setOnItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_menu -> {
                    showPopupMenu(bottomNavigationView.findViewById(R.id.nav_menu), userType)
                    return@setOnItemSelectedListener false  // Prevent default behavior
                }
                R.id.nav_clients -> {
                    navController.navigate(R.id.ClientFragment)
                    true}
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

        listenForNotifications()

    }

    private fun listenForNotifications() {
        lifecycleScope.launch {
            firebaseNotificationService.getNewNewsAlerts().collectLatest { newsAlert ->
                // Check if the alarm_id is valid and not already displayed
                if (newsAlert.alarm_id.isNotEmpty() && !notificationTracker.isAlarmDisplayed(newsAlert.alarm_id)) {
                    runOnUiThread {
                        val toastMessage = "🔔 ${newsAlert.notes}"
                        Toast.makeText(
                            this@MainActivity,
                            toastMessage,
                            Toast.LENGTH_LONG
                        ).show()

                        // Mark this alarm_id as displayed
                        notificationTracker.markAlarmAsDisplayed(newsAlert.alarm_id)
                    }
                } else {
                    // Optional: Log if the alert is empty or already displayed
                    if (newsAlert.alarm_id.isEmpty()) {
                        Log.d("NotificationListener", "Received NewsAlert with empty alarm_id.")
                    } else {
                        Log.d("NotificationListener", "NewsAlert for alarm_id ${newsAlert.alarm_id} already displayed or empty.")
                    }
                }
            }
        }
    }

    private fun showPopupMenu(anchorView: View, userType: String) {
        val popup = PopupMenu(this, anchorView)
        popup.menuInflater.inflate(R.menu.popup_menu, popup.menu)
        popup.menu.setGroupVisible(0, false)

        popup.menu.findItem(R.id.action_show_notifications).isVisible = true

        when (userType) {
            "SELLER" -> {
                popup.menu.findItem(R.id.RegisterClientFragment).isVisible = true
                popup.menu.findItem(R.id.RoutesCreateVisitFragment).isVisible = true
                popup.menu.findItem(R.id.SearchStockFragment).isVisible = true
                popup.menu.findItem(R.id.ClientVisitFragment).isVisible = true
                popup.menu.findItem(R.id.CreateOrderFragment).isVisible = true
                popup.menu.findItem(R.id.UploadVideoFragment).isVisible = true
            }

            "CLIENT" -> {
                popup.menu.findItem(R.id.SearchStockFragment).isVisible = true
                popup.menu.findItem(R.id.CreateOrderFragment).isVisible = true
                popup.menu.findItem(R.id.UploadVideoFragment).isVisible = false
            }
            // Filter menu based on user type
        }
        popup.menu.findItem(R.id.CerrarSesion).isVisible = true

        popup.setOnMenuItemClickListener { menuItem: MenuItem ->
            when (menuItem.itemId) {
                R.id.RegisterClientFragment -> navController.navigate(R.id.RegisterClientFragment)
                R.id.RoutesCreateVisitFragment -> navController.navigate(R.id.RoutesCreateVisitFragment)
                R.id.SearchStockFragment -> navController.navigate(R.id.SearchStockFragment)
                R.id.ClientVisitFragment -> navController.navigate(R.id.ClientVisitFragment)
                R.id.CreateOrderFragment -> navController.navigate(R.id.CreateOrderFragment)
                R.id.UploadVideoFragment -> navController.navigate(R.id.UploadVideoFragment)
                R.id.action_show_notifications -> {
                    navController.navigate(R.id.notificationsListFragment)
                }
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