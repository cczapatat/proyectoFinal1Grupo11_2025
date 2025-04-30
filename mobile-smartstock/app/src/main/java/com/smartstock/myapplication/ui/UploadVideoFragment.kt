package com.smartstock.myapplication.ui

import android.app.Activity
import android.app.DatePickerDialog
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.OpenableColumns
import android.text.TextUtils
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.findNavController
import com.smartstock.myapplication.R
import com.smartstock.myapplication.database.AppDatabase
import com.smartstock.myapplication.databinding.FragmentUploadVideoBinding
import com.smartstock.myapplication.models.Recommendation
import com.smartstock.myapplication.network.NetworkServiceAdapter
import com.smartstock.myapplication.repositories.UserSessionRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Calendar

class UploadVideoFragment: Fragment() {

    private var _binding: FragmentUploadVideoBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!
    private lateinit var adapter: NetworkServiceAdapter
    private lateinit var dateEdt: EditText
    private var selectedClientId: String? = ""

    private val PICK_VIDEO_REQUEST = 1
    private var selectedFileUri: Uri? = null
    private var uploadedFileId: String? = null
    private var uploadedFileName: String? = null
    private lateinit var userSessionRepository: UserSessionRepository

    private var isSubmitting = false
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentUploadVideoBinding.inflate(inflater, container, false)

        adapter = NetworkServiceAdapter.getInstance(requireContext())
        val userTokenDao = AppDatabase.getDatabase(requireContext()).userTokenDao()
        userSessionRepository = UserSessionRepository(requireActivity().application, userTokenDao)


        // Set User:
        val sharedPreferences = requireContext().getSharedPreferences("CLL_APP", Context.MODE_PRIVATE)
        val type = sharedPreferences.getString("type", "")
        val id = sharedPreferences.getString("id", "")
        val name = sharedPreferences.getString("name", "")
        val clientDropdown = binding.autoCompleteTextViewCreate1
        if (type == "CLIENT"){
            clientDropdown.setText(name, false)
            clientDropdown.isEnabled = true
            clientDropdown.isFocusable = false
            clientDropdown.isClickable = false
            selectedClientId = id
        } else {
            // Logic to fetch seller clients
            clientDropdown.setText("", false)
            clientDropdown.isEnabled = false
            clientDropdown.isFocusable = false
            clientDropdown.isClickable = false
            lifecycleScope.launch {
                try {
                    val clients = adapter.fetchPaginatedClientsBySellerId(
                        sellerId = id!!, // `id` is the sellerId
                        page = 1,
                        perPage = 100 // Fetch enough clients for dropdown
                    )
                    val clientNames = clients.map { it.name }
                    clientDropdown.isEnabled = true
                    clientDropdown.isFocusable = true
                    clientDropdown.isClickable = true
                    // Bind names to dropdown
                    val dropdownAdapter = ArrayAdapter(
                        requireContext(),
                        R.layout.list_item, // Use the same list_item layout
                        clientNames
                    )
                    clientDropdown.setAdapter(dropdownAdapter)

                    // Handle client selection
                    clientDropdown.setOnItemClickListener { parent, _, position, _ ->
                        val selectedClient = clients[position]
                        selectedClientId = selectedClient.id.toString()
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                    showMessage("Failed to load clients", requireContext())
                }
            }
        }

        // Set Calendar
        val c = Calendar.getInstance()
        val df = SimpleDateFormat("dd-MM-yyyy")
        val formattedDate: String = df.format(c.time)
        dateEdt = binding.datePickerCreate
        dateEdt.setText(formattedDate)
        dateEdt.showSoftInputOnFocus = false
        dateEdt.setOnClickListener {

            val c = Calendar.getInstance()
            val year = c.get(Calendar.YEAR)
            val month = c.get(Calendar.MONTH)
            val day = c.get(Calendar.DAY_OF_MONTH)

            val datePickerDialog = DatePickerDialog(
                binding.root.context,
                { _, year, monthOfYear, dayOfMonth ->
                    val dat = String.format("%02d-%02d-%04d", dayOfMonth, monthOfYear + 1, year)
                    dateEdt.setText(dat)
                },
                year,
                month,
                day
            )
            // Prevent past date selection
            datePickerDialog.datePicker.minDate = System.currentTimeMillis() - 1000
            datePickerDialog.show()
        }

        // Setup file upload
        binding.videoUploadIcon.setOnClickListener {
            val intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.type = "video/mp4"
            startActivityForResult(Intent.createChooser(intent, "Select MP4"), PICK_VIDEO_REQUEST)
        }
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
                addVideo()
            }
        }
    }

    private fun addVideo() {

        //val seller_id = UUID.randomUUID()
        val releaseDateOld = binding.datePickerCreate.text.toString()
        val arr = releaseDateOld.split("-")
        val videoDate = "${arr[2]}-${arr[1]}-${arr[0]} 23:59:30"


        val argsArray: ArrayList<String?> = arrayListOf(selectedClientId, videoDate, uploadedFileId)
        if (this.formIsValid(argsArray)) {

            lifecycleScope.launch {
                val token = withContext(Dispatchers.IO) {
                    userSessionRepository.getSavedToken()
                }
                val recomendation = Recommendation(
                    id = null,
                    document_id = uploadedFileId,
                    file_path = uploadedFileName,
                    store_id = selectedClientId,
                    tags = "",
                    enabled = true,
                    update_date = videoDate,
                    creation_date = videoDate,
                )

                try {
                    val createdRecomendation = adapter.addRecomendation(recomendation, requireContext(), token)
                    Toast.makeText(requireContext(), getString(R.string.cargar_video_procesando), Toast.LENGTH_LONG).show()
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
        binding.autoCompleteTextViewCreate1.setText("")
        binding.datePickerCreate.setText("")
    }

    private fun formIsValid(array: ArrayList<String?>): Boolean {
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
            UploadVideoFragmentDirections.actionUploadVideoFragmentToClientFragment()
        )
    }
    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == PICK_VIDEO_REQUEST && resultCode == Activity.RESULT_OK && data != null && data.data != null) {
            selectedFileUri = data.data
            val contentResolver = requireContext().contentResolver
            // Check MIME type
            val type = contentResolver.getType(selectedFileUri!!)
            if (type != "video/mp4") {
                Toast.makeText(requireContext(), getString(R.string.cargar_video_error_formato), Toast.LENGTH_SHORT).show()
                return
            }

            // Check file size
            val cursor = contentResolver.query(selectedFileUri!!, null, null, null, null)
            val sizeIndex = cursor?.getColumnIndex(OpenableColumns.SIZE) ?: -1
            var size: Long = 0
            if (cursor != null && sizeIndex != -1) {
                cursor.moveToFirst()
                size = cursor.getLong(sizeIndex)
                cursor.close()
            }

            if (size > 20 * 1024 * 1024) {
                Toast.makeText(requireContext(), getString(R.string.cargar_video_error_tamano), Toast.LENGTH_SHORT).show()
                return
            }

            lifecycleScope.launch {
                val token = withContext(Dispatchers.IO) {
                    userSessionRepository.getSavedToken()
                }
                try {
                    val result = adapter.uploadVideoFile(requireContext(), selectedFileUri!!, token)
                    uploadedFileId = result.id
                    uploadedFileName = result.file_name
                    Toast.makeText(requireContext(), "Video uploaded successfully!", Toast.LENGTH_SHORT).show()
                    binding.videoStatus.text = getString(R.string.cargar_video_seleccionado) + getString(R.string.cargar_video_seleccionado_ok)
                } catch (e: Exception) {
                    e.printStackTrace()
                    Toast.makeText(requireContext(), "Failed to upload video", Toast.LENGTH_SHORT).show()
                    binding.videoStatus.text = getString(R.string.cargar_video_seleccionado) + getString(R.string.cargar_video_seleccionado_bad)

                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}