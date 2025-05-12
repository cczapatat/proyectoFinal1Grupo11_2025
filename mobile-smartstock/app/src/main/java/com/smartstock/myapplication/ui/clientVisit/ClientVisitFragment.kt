package com.smartstock.myapplication.ui.clientVisit

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.smartstock.myapplication.R
import com.smartstock.myapplication.adapters.ClientVisitAdapter
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.databinding.FragmentListVisitsBinding
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.UserSessionRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ClientVisitFragment : Fragment() {

    private var _binding: FragmentListVisitsBinding? = null
    private val binding get() = _binding!!

    private lateinit var userSessionRepository: UserSessionRepository
    private lateinit var viewModel: ClientVisitViewModel
    private lateinit var adapter: ClientVisitAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentListVisitsBinding.inflate(inflater, container, false)

        // Prepare the repository
        val dao = AppDatabase.getDatabase(requireContext()).userTokenDao()
        userSessionRepository = UserSessionRepository(requireActivity().application, dao)

        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Show bottom nav if needed
        requireActivity().findViewById<View>(R.id.bottom_navigation)?.visibility = View.VISIBLE

        // 1) Initialize adapter & RecyclerView synchronously
        adapter = ClientVisitAdapter { visit ->
            Toast.makeText(
                requireContext(),
                "${getString(R.string.seleccionado)} ${visit.client.name}",
                Toast.LENGTH_SHORT
            ).show()
        }
        binding.visitClientsRv.apply {
            layoutManager = LinearLayoutManager(requireContext())
            this.adapter = this@ClientVisitFragment.adapter
        }

        // 2) Load token, then create ViewModel and start collecting
        viewLifecycleOwner.lifecycleScope.launch {
            // a) Fetch saved token off the main thread
            val token = withContext(Dispatchers.IO) {
                userSessionRepository.getSavedToken()
            }

            // b) Create ViewModel with the real token
            val factory = ClientVisitViewModelFactory(
                NetworkServiceAdapter.getInstance(requireContext()),
                token
            )
            viewModel = ViewModelProvider(
                this@ClientVisitFragment,
                factory
            )[ClientVisitViewModel::class.java]

            // c) Observe paging data
            viewModel.clientsVisits.collectLatest { pagingData ->
                adapter.submitData(pagingData)
            }
        }
    }

    override fun onResume() {
        super.onResume()
        // Safe: adapter is already initialized in onViewCreated
        adapter.refresh()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}