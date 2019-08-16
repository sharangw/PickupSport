package com.example.pickupsport

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.squareup.okhttp.Callback
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import com.squareup.okhttp.Response
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.login_fragment.view.*
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import java.io.IOException

/**
 * Fragment representing the login screen for Shrine.
 */
class LoginFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.login_fragment, container, false)

        view.next_button.setOnClickListener {
            doAsync {
                Log.d("DEBUG", "button clicked");
                val gotresponse = fetchInfo()
                Log.d("DEBUG", "fetching info");
                val jsonarray = JSONArray(gotresponse)

                //val venue = jsonarray.getJSONObject(i)

            }
        }
        return view
    }

    private fun fetchInfo(): String {
        val url = "https://my-apad-project.appspot.com/app/login"
        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        val response = client.newCall(request).execute()
        val bodyStr = response.body().string() // this can be consumed only once
        println("bodyStr")
        println(bodyStr)
        return bodyStr
    }
}




