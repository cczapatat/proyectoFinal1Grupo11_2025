package com.smartstock.myapplication.network

import android.util.Log
import com.google.firebase.database.ChildEventListener
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import com.smartstock.myapplication.models.NewsAlert
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow

/**
 * Service class for managing Firebase notifications related to NewsAlerts.
 */
class FirebaseNotificationService {

    // Firebase database instance pointing to the specific database URL
    private val databaseInstance = FirebaseDatabase.getInstance("https://miso-proyecto-final2-2025-default-rtdb.firebaseio.com/")
    private val newsRef = databaseInstance.getReference("news") // Reference to the "news" node in the database

    companion object {
        private const val TAG = "FirebaseNotificationSvc" // Tag for logging
    }

    /**
     * Sends a NewsAlert to the Firebase database.
     *
     * @param newsAlert The NewsAlert object to be sent.
     */
    fun sendNewsAlert(newsAlert: NewsAlert) {
        val newAlertRef = newsRef.push() // Create a new child node under "news"
        newAlertRef.setValue(newsAlert) // Set the value of the new node to the NewsAlert object
            .addOnSuccessListener {
                Log.d(TAG, "NewsAlert sent successfully: ${newAlertRef.key}")
            }
            .addOnFailureListener { e ->
                Log.e(TAG, "Failed to send NewsAlert", e)
            }
    }

    /**
     * Retrieves a flow of new NewsAlerts from the Firebase database.
     *
     * @return A Flow emitting NewsAlert objects when new alerts are added to the database.
     */
    fun getNewNewsAlerts(): Flow<NewsAlert> = callbackFlow {
        val childEventListener = object : ChildEventListener {
            /**
             * Called when a new child is added to the "news" node.
             *
             * @param snapshot The DataSnapshot containing the new child data.
             * @param previousChildName The key name of the previous sibling, if any.
             */
            override fun onChildAdded(snapshot: DataSnapshot, previousChildName: String?) {
                try {
                    val newsAlert = snapshot.getValue(NewsAlert::class.java) // Deserialize the snapshot into a NewsAlert object
                    newsAlert?.let { alert ->
                        alert.firebaseKey = snapshot.key ?: "" // Set the Firebase key for the alert
                        Log.d(TAG, "New NewsAlert received: ${alert.notes}, Key: ${alert.firebaseKey}")
                        trySend(alert).isSuccess // Emit the alert through the flow
                    } ?: run {
                        Log.w(TAG, "Received null NewsAlert object for key: ${snapshot.key}")
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Error parsing NewsAlert snapshot for key: ${snapshot.key}", e)
                }
            }

            override fun onChildChanged(snapshot: DataSnapshot, previousChildName: String?) {
                Log.d(TAG, "NewsAlert changed: ${snapshot.key}")
            }

            override fun onChildRemoved(snapshot: DataSnapshot) {
                Log.d(TAG, "NewsAlert removed: ${snapshot.key}")
            }

            override fun onChildMoved(snapshot: DataSnapshot, previousChildName: String?) {
                Log.d(TAG, "NewsAlert moved: ${snapshot.key}")
            }

            /**
             * Called when the listener is canceled due to an error.
             *
             * @param error The DatabaseError containing details about the cancellation.
             */
            override fun onCancelled(error: DatabaseError) {
                Log.w(TAG, "Firebase NewsAlert listener cancelled", error.toException())
                close(error.toException()) // Close the flow with the error
            }
        }

        newsRef.addChildEventListener(childEventListener) // Attach the listener to the "news" node

        awaitClose {
            Log.d(TAG, "Removing Firebase NewsAlert listener.")
            newsRef.removeEventListener(childEventListener) // Remove the listener when the flow is closed
        }
    }

    /**
     * Fetches all news alerts from the "news" node once.
     * @return A Flow that emits a single list of all NewsAlert objects or an error.
     */
    fun getAllNewsAlerts(): Flow<List<NewsAlert>> = callbackFlow {
        val valueEventListener = object : ValueEventListener {
            override fun onDataChange(snapshot: DataSnapshot) {
                val alertsList = mutableListOf<NewsAlert>()
                if (snapshot.exists()) {
                    for (alertSnapshot in snapshot.children) {
                        try {
                            val newsAlert = alertSnapshot.getValue(NewsAlert::class.java)
                            newsAlert?.let { alert ->
                                alert.firebaseKey = alertSnapshot.key ?: ""
                                alertsList.add(alert)
                            }
                        } catch (e: Exception) {
                            Log.e(TAG, "Error parsing individual NewsAlert snapshot during getAll: ${alertSnapshot.key}", e)
                        }
                    }
                }
                Log.d(TAG, "Fetched ${alertsList.size} news alerts.")
                trySend(alertsList.reversed()).isSuccess // Emit the list (reversed to show newest first, optional)
                close() // Close the flow after emitting once
            }

            override fun onCancelled(error: DatabaseError) {
                Log.e(TAG, "Failed to fetch all news alerts", error.toException())
                close(error.toException()) // Close the flow with an error
            }
        }

        newsRef.addListenerForSingleValueEvent(valueEventListener) // Use addListenerForSingleValueEvent to fetch once

        awaitClose {
            Log.d(TAG, "getAllNewsAlerts flow closed.")
        }
    }

    /**
     * Marks a specific NewsAlert as read in the Firebase database.
     *
     * @param alertKey The key of the NewsAlert to be marked as read.
     */
    fun markNewsAlertAsRead(alertKey: String) {
        if (alertKey.isNotEmpty()) {
            newsRef.child(alertKey).child("read").setValue(true) // Update the "read" field of the specified alert
                .addOnSuccessListener {
                    Log.d(TAG, "NewsAlert $alertKey marked as read.")
                }
                .addOnFailureListener { e ->
                    Log.e(TAG, "Failed to mark NewsAlert $alertKey as read", e)
                }
        } else {
            Log.w(TAG, "markNewsAlertAsRead called with empty alertKey.")
        }
    }
}