package com.smartstock.myapplication.ui

import android.content.Context
import android.os.Bundle
import android.text.TextUtils
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.AutoCompleteTextView
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.lifecycleScope
import androidx.navigation.findNavController
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import com.smartstock.myapplication.R
import com.google.android.material.datepicker.MaterialDatePicker
import com.google.android.material.timepicker.MaterialTimePicker
import com.google.android.material.timepicker.TimeFormat
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.database.dao.ClientDao
import com.smartstock.myapplication.databinding.FragmentRegisterClientBinding
import com.smartstock.myapplication.models.Client
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.ClientRepository
import com.smartstock.myapplication.repositories.UserSessionRepository
import com.smartstock.myapplication.ui.client.ClientViewModel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale
import java.util.UUID

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class RegisterClientFragment : Fragment() {

    private var _binding: FragmentRegisterClientBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!
    private lateinit var adapter: NetworkServiceAdapter

    private lateinit var clientTypeMap: Map<String, String>
    private lateinit var zoneMap: Map<String, String>
    private lateinit var userSessionRepository: UserSessionRepository
    private var isSubmitting = false
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentRegisterClientBinding.inflate(inflater, container, false)

        clientTypeMap = mapOf(
            getString(R.string.client_type_supermarket) to "SUPERMARKET",
            getString(R.string.client_type_corner_store) to "CORNER_STORE"
        )
        zoneMap = mapOf(
            getString(R.string.zone_south) to "SOUTH",
            getString(R.string.zone_north) to "NORTH",
            getString(R.string.zone_east) to "EAST",
            getString(R.string.zone_west) to "WEST",
            getString(R.string.zone_center) to "CENTER",
            getString(R.string.zone_northeast) to "NORTHEAST",
            getString(R.string.zone_northwest) to "NORTHWEST",
            getString(R.string.zone_southeast) to "SOUTHEAST",
            getString(R.string.zone_southwest) to "SOUTHWEST"
        )
        adapter = NetworkServiceAdapter.getInstance(requireContext())
        val userTokenDao = AppDatabase.getDatabase(requireContext()).userTokenDao()
        userSessionRepository = UserSessionRepository(requireActivity().application, userTokenDao)
        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        requireActivity().findViewById<View>(R.id.bottom_navigation)?.visibility = View.GONE
        binding.buttonCancelCreate.setOnClickListener {
            navigateToClients()
        }
        binding.buttonAcceptCreate.setOnClickListener {
            if (!isSubmitting) {
                isSubmitting = true
                binding.buttonAcceptCreate.isEnabled = false
                addClient()
            }


        }
        setupDropdowns()

    }

    private fun setupDropdowns() {
        val adapterType = ArrayAdapter(requireContext(), R.layout.list_item, clientTypeMap.keys.toList())
        val adapterZone = ArrayAdapter(requireContext(), R.layout.list_item, zoneMap.keys.toList())

        binding.autoCompleteTextViewCreate1.setAdapter(adapterType)
        binding.autoCompleteTextViewCreate2.setAdapter(adapterZone)
    }

    private fun addClient() {
        val name = binding.name.text?.toString()?:""
        val phone = binding.phone.text?.toString()?:""
        val email = binding.emailCreateClient.text?.toString()?:""
        val address = binding.address.text?.toString()?:""
        //val seller_id = UUID.randomUUID()
        val user_id = UUID.randomUUID()

        val selectedType = binding.autoCompleteTextViewCreate1.text.toString()
        val selectedZone = binding.autoCompleteTextViewCreate2.text.toString()
        // Convert user-friendly dropdown values to request values
        val mappedType = clientTypeMap[selectedType] ?: ""
        val mappedZone = zoneMap[selectedZone] ?: ""


        val argsArray: ArrayList<String> = arrayListOf(name, phone, email, address, mappedType, mappedZone)
        if (this.formIsValid(argsArray)) {

            lifecycleScope.launch {
                val userId = withContext(Dispatchers.IO) {
                    userSessionRepository.getSavedUserId()
                }
                val client = Client(
                    name = name,
                    phone = phone,
                    email = email,
                    address = address,
                    clientType = mappedType,
                    zone = mappedZone,
                    userId = user_id,
                    sellerId = UUID.fromString(userId)
                )

                try {
                    val createdClient = adapter.addClient(client, requireContext())
                    Toast.makeText(requireContext(), getString(R.string.success_add_client), Toast.LENGTH_LONG).show()
                    clearForm()
                    navigateToClients()
                } catch (e: Exception) {
                    e.printStackTrace()
                } finally {
                    isSubmitting = false
                    binding.buttonAcceptCreate.isEnabled = true
                }
            }


        } else {
            showMessage(getString(R.string.error_add_client_fields), this.requireContext())
            binding.buttonAcceptCreate.isEnabled = true
            isSubmitting = false
        }
    }

    private fun clearForm() {
        binding.name.setText("")
        binding.phone.setText("")
        binding.emailCreateClient.setText("")
        binding.address.setText("")
        binding.autoCompleteTextViewCreate1.setText("")
        binding.autoCompleteTextViewCreate2.setText("")
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
        requireActivity().runOnUiThread{
            Toast.makeText(context, s, Toast.LENGTH_LONG).show()
        }
    }

    private fun navigateToClients() {

        binding.root.findNavController().navigate(
            RegisterClientFragmentDirections.actionRegisterClientFragmentToClientFragment()
        )
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}