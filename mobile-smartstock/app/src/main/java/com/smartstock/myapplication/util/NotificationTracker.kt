package com.smartstock.myapplication.util

import android.content.Context
import android.content.SharedPreferences

class NotificationTracker(context: Context) {

    companion object {
        private const val PREFS_NAME = "NotificationTrackerPrefs"
        private const val KEY_DISPLAYED_ALARM_IDS = "displayed_alarm_ids"
    }

    private val sharedPreferences: SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    /**
     * Checks if a given alarm_id has already been marked as displayed.
     * @param alarmId The alarm_id to check.
     * @return True if the alarm_id has been displayed, false otherwise.
     */
    fun isAlarmDisplayed(alarmId: String): Boolean {
        val displayedIds = sharedPreferences.getStringSet(KEY_DISPLAYED_ALARM_IDS, emptySet()) ?: emptySet()
        return displayedIds.contains(alarmId)
    }

    /**
     * Marks a given alarm_id as displayed by adding it to the stored set.
     * @param alarmId The alarm_id to mark as displayed.
     */
    fun markAlarmAsDisplayed(alarmId: String) {
        val displayedIds = sharedPreferences.getStringSet(KEY_DISPLAYED_ALARM_IDS, HashSet()) ?: HashSet()
        val mutableDisplayedIds = HashSet(displayedIds)
        mutableDisplayedIds.add(alarmId)
        sharedPreferences.edit().putStringSet(KEY_DISPLAYED_ALARM_IDS, mutableDisplayedIds).apply()
    }

    /**
     * (Optional) Clears all stored displayed alarm_ids. Useful for testing or reset.
     */
    fun clearDisplayedAlarms() {
        sharedPreferences.edit().remove(KEY_DISPLAYED_ALARM_IDS).apply()
    }
}