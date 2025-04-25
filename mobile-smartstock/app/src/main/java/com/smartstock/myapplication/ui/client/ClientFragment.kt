package com.smartstock.myapplication.ui.client

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.SearchView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.smartstock.myapplication.R
import com.smartstock.myapplication.adapters.ClientAdapter
import com.smartstock.myapplication.databinding.FragmentListClientsBinding
import com.smartstock.myapplication.network.NetworkServiceAdapter
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class ClientFragment: Fragment() {

    private var _binding: FragmentListClientsBinding? = null
    private val binding get() = _binding!!

    //private lateinit var sharedPreferences: SharedPreferences
    private lateinit var viewModel: ClientViewModel
    private lateinit var adapter: ClientAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentListClientsBinding.inflate(inflater, container, false)
        val sharedPreferences = requireContext().getSharedPreferences("CLL_APP", Context.MODE_PRIVATE)
        val sellerId = sharedPreferences.getString("id", "") ?: ""
        //val id = sharedPreferences.getString("id", "")

        val factory = ClientViewModelFactory(NetworkServiceAdapter.getInstance(requireContext()), sellerId)
        viewModel = ViewModelProvider(this, factory)[ClientViewModel::class.java]

        setupRecyclerView()
        observeClients()

        return binding.root
    }

    private fun setupRecyclerView() {
        adapter = ClientAdapter { client ->
            Toast.makeText(requireContext(), "${getString(R.string.seleccionado)} ${client.name}", Toast.LENGTH_SHORT).show()
        }

        binding.clientsRv.layoutManager = LinearLayoutManager(requireContext())
        binding.clientsRv.adapter = adapter
    }

    private fun observeClients() {
        lifecycleScope.launch {
            viewModel.clients.collectLatest { pagingData ->
                adapter.submitData(pagingData)
            }
        }
    }

    override fun onResume() {
        super.onResume()
        requireActivity().findViewById<View>(R.id.bottom_navigation)?.visibility = View.VISIBLE
        adapter.refresh() // Refresh if navigating back
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

}