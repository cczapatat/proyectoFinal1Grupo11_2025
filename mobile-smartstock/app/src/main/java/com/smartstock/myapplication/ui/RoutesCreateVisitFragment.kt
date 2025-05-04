package com.smartstock.myapplication.ui

import android.content.Context
import android.os.Bundle
import android.text.TextUtils
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.smartstock.myapplication.R
import com.smartstock.myapplication.adapters.SelectedProductAdapter
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.databinding.FragmentRoutesCreateVisitBinding
import com.smartstock.myapplication.models.RouteVisit
import com.smartstock.myapplication.models.SimpleProductName
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.UserSessionRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter

class RoutesCreateVisitFragment : Fragment() {

    private var _binding: FragmentRoutesCreateVisitBinding? = null
    private val binding get() = _binding!!

    private lateinit var networkAdapter: NetworkServiceAdapter
    private lateinit var userSessionRepository: UserSessionRepository

    // Holds the user’s selected products
    private val pickedProducts = mutableListOf<SimpleProductName>()
    private lateinit var pickedAdapter: SelectedProductAdapter

    private var selectedClientId: String? = null
    private var isSubmitting = false
    private val DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentRoutesCreateVisitBinding.inflate(inflater, container, false)

        networkAdapter = NetworkServiceAdapter.getInstance(requireContext())
        val dao = AppDatabase.getDatabase(requireContext()).userTokenDao()
        userSessionRepository = UserSessionRepository(requireActivity().application, dao)

        setupClientDropdown()
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        requireActivity().findViewById<View>(R.id.bottom_navigation)?.visibility = View.GONE

        // Set up the “picked” list
        pickedAdapter = SelectedProductAdapter(pickedProducts) { toRemove ->
            val idx = pickedProducts.indexOf(toRemove).takeIf { it >= 0 } ?: return@SelectedProductAdapter
            pickedProducts.removeAt(idx)
            binding.simpleProductsRv.adapter?.notifyItemRemoved(idx)
        }
        binding.simpleProductsRv.apply {
            adapter = pickedAdapter
            layoutManager = LinearLayoutManager(requireContext())
        }

        // Add product button → show dialog
        binding.buttonAddProduct.setOnClickListener {
            AddSimpleProductNameDialogFragment { picked ->
                val newIndex = pickedProducts.size
                pickedProducts.add(picked)
                pickedAdapter.notifyItemInserted(newIndex)
                binding.simpleProductsRv.scrollToPosition(newIndex)
            }.show(parentFragmentManager, "AddProductDialog")
        }

        // Cancel / Save
        binding.buttonCancelCreate.setOnClickListener { navigateToClients() }
        binding.buttonAcceptCreate.setOnClickListener { submitVisit() }
    }

    private fun setupClientDropdown() {
        val prefs = requireContext().getSharedPreferences("CLL_APP", Context.MODE_PRIVATE)
        val type = prefs.getString("type", "")
        val idPref = prefs.getString("id", null)
        val name = prefs.getString("name", "")
        val clientDropdown = binding.autoCompleteTextViewCreate1

        if (type == "CLIENT") {
            clientDropdown.setText(name, false)
            clientDropdown.isEnabled = false
            selectedClientId = idPref
        } else {
            clientDropdown.setText("", false)
            clientDropdown.isEnabled = false
            lifecycleScope.launch {
                try {
                    val clients = withContext(Dispatchers.IO) {
                        networkAdapter.fetchPaginatedClientsBySellerId(
                            sellerId = idPref!!,
                            page = 1,
                            perPage = 100
                        )
                    }
                    val names = clients.map { it.name }

                    val dropdownAdapter = ArrayAdapter(
                        requireContext(),
                        R.layout.list_item,
                        names
                    )
                    clientDropdown.setAdapter(dropdownAdapter)
                    clientDropdown.isEnabled = true
                    clientDropdown.setOnItemClickListener { _, _, pos, _ ->
                        selectedClientId = clients[pos].id.toString()
                    }

                } catch (e: Exception) {
                    e.printStackTrace()
                    Toast.makeText(
                        requireContext(),
                        R.string.registrar_visita_error,
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }
    }

    private fun submitVisit() {
        if (isSubmitting) return

        if (pickedProducts.isEmpty() || selectedClientId.isNullOrBlank()) {
            Toast.makeText(
                requireContext(),
                R.string.error_add_client_fields,
                Toast.LENGTH_LONG
            ).show()
            return
        }

        isSubmitting = true
        binding.buttonAcceptCreate.isEnabled = false

        val visitDateFormatted: String = LocalDateTime
            .now(ZoneOffset.UTC)
            .format(DATE_TIME_FORMATTER)

        val route = RouteVisit(
            client_id   = selectedClientId!!,
            visit_date  = visitDateFormatted,
            description = binding.longDescriptionField.text.toString(),
            products    = ArrayList(pickedProducts)
        )

        lifecycleScope.launch {
            val token = withContext(Dispatchers.IO) { userSessionRepository.getSavedToken() }
            try {
                networkAdapter.addRouteVisit(route, requireContext(), token)
                Toast.makeText(
                    requireContext(),
                    R.string.registrar_visita_existoso,
                    Toast.LENGTH_LONG
                ).show()
                navigateToClients()
            } catch (e: Exception) {
                print(e.message)
                Toast.makeText(
                    requireContext(),
                    e.localizedMessage,
                    Toast.LENGTH_LONG
                ).show()
            } finally {
                isSubmitting = false
                binding.buttonAcceptCreate.isEnabled = true
            }
        }
    }

    private fun navigateToClients() =
        binding.root.findNavController()
            .navigate(RoutesCreateVisitFragmentDirections.actionRoutesCreateVisitFragmentToClientFragment())

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}