import android.content.Context
import androidx.test.core.app.ApplicationProvider
import com.android.volley.RequestQueue
import com.android.volley.Response
import com.android.volley.VolleyError
import com.smartstock.myapplication.models.Client
import com.smartstock.myapplication.models.User
import com.smartstock.myapplication.models.UserVerify
import com.smartstock.myapplication.network.NetworkServiceAdapter
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.runBlocking
import org.json.JSONObject
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.mockito.ArgumentCaptor
import org.mockito.Mock
import org.mockito.Mockito.*
import org.mockito.junit.MockitoJUnitRunner
import org.mockito.kotlin.any
import java.util.UUID
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

@ExperimentalCoroutinesApi
@RunWith(MockitoJUnitRunner::class)
class NetworkServiceAdapterTest {

    @Mock
    private lateinit var mockRequestQueue: RequestQueue

    private lateinit var networkServiceAdapter: NetworkServiceAdapter
    private lateinit var context: Context

    @Before
    fun setUp() {
        context = ApplicationProvider.getApplicationContext()
        networkServiceAdapter = spy(NetworkServiceAdapter(context))
        doReturn(mockRequestQueue).`when`(networkServiceAdapter).getRequestQueue()
    }

    @Test
    fun `login should return user on success`() = runBlocking {
        val user = User("", "", "token123", "", "", "", "email@example.com", "")
        val jsonResponse = JSONObject().apply {
            put("id", "1")
            put("user_id", "123")
            put("token", "token123")
            put("name", "Test User")
        }

        val responseListener = ArgumentCaptor.forClass(Response.Listener::class.java) as ArgumentCaptor<Response.Listener<JSONObject>>

        doAnswer {
            responseListener.value.onResponse(jsonResponse)
        }.`when`(mockRequestQueue).add(any())

        val result = networkServiceAdapter.login(user, context)
        assertEquals("123", result.user_id)
        assertEquals("token123", result.token)
    }

    @Test
    fun `login should throw exception on failure`() = runBlocking {
        val user = User("", "", "token123", "", "", "", "email@example.com", "")
        val error = VolleyError("Network Error")

        val errorListener = ArgumentCaptor.forClass(Response.ErrorListener::class.java) as ArgumentCaptor<Response.ErrorListener>

        doAnswer {
            errorListener.value.onErrorResponse(error)
        }.`when`(mockRequestQueue).add(any())

        assertFailsWith<VolleyError> {
            networkServiceAdapter.login(user, context)
        }
    }

    @Test
    fun `verifyUser should return UserVerify on success`() = runBlocking {
        val jsonResponse = JSONObject().apply {
            put("user_session_id", "sess123")
            put("user_id", "user123")
            put("user_type", "admin")
        }

        val responseListener = ArgumentCaptor.forClass(Response.Listener::class.java) as ArgumentCaptor<Response.Listener<JSONObject>>

        doAnswer {
            responseListener.value.onResponse(jsonResponse)
        }.`when`(mockRequestQueue).add(any())

        val result = networkServiceAdapter.verifyUser("token123")
        assertEquals("sess123", result.user_session_id)
        assertEquals("user123", result.user_id)
    }

    @Test
    fun `addClient should return Client on success`() = runBlocking {
        val client = Client(
            id = UUID.randomUUID(),
            name = "Test Client",
            phone = "1234567890",
            email = "client@example.com",
            clientType = "CORNER_STORE",
            address = "123 Test Street",
            zone = "NORTH",
            sellerId = UUID.fromString("f7ba2395-c7af-4df2-a24a-4955d2dd80e6"),
            userId = UUID.randomUUID()
        )

        val jsonResponse = JSONObject().apply {
            put("id", UUID.randomUUID().toString())
            put("name", "Test Client")
            put("phone", "1234567890")
            put("email", "client@example.com")
            put("client_type", "CORNER_STORE")
            put("address", "123 Test Street")
            put("zone", "NORTH")
            put("user_id", client.userId.toString())
        }

        val responseListener = ArgumentCaptor.forClass(Response.Listener::class.java) as ArgumentCaptor<Response.Listener<JSONObject>>

        doAnswer {
            responseListener.value.onResponse(jsonResponse)
        }.`when`(mockRequestQueue).add(any())

        val result = networkServiceAdapter.addClient(client, context)
        assertEquals("Test Client", result.name)
    }
}
