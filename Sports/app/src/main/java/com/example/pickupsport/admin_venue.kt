package com.example.pickupsport

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.google.gson.GsonBuilder
//import com.squareup.okhttp.OkHttpClient
//import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.admin_home.view.*
import kotlinx.android.synthetic.main.admin_venue.view.*
import okhttp3.*
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import java.io.IOException

class admin_venue : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.admin_venue, container, false)

        view.back_buttonvenue.setOnClickListener({
            // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(admin_home(), false)
        })


        return view
    }

   override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        doAsync {
            Log.d("DEBUG", "button clicked");
            val gotresponse = fetchInfo()
            Log.d("DEBUG", "fetching info");
            val venues = JSONArray(gotresponse)
            print(venues)
        }
    }

    private fun fetchInfo() {

        val url = "https://my-apad-project.appspot.com/app/venues"

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onResponse(call: Call, response: Response) {
                val body = response?.body()?.string()
                println(body)

                val gson = GsonBuilder().create()

                val venueFeed = gson.fromJson(body, VenueFeed::class.java)
            }

            override fun onFailure(call: Call, e: IOException) {
                println("failed")
            }
        })

//        Log.d("DEBUG", "inside fetch info")
//
//        val url = "https://my-apad-project.appspot.com/app/venues"
//
//        val client = OkHttpClient()
//        val request = Request.Builder()
//            .url(url)
//            .header("User-Agent", "Android")
//            .build()
//        try {
//            val response = client.newCall(request).execute()
//            val bodyStr =  response.body()?.string() // this can be consumed only once
//            println(bodyStr)
//            return bodyStr
//        } catch (e: Exception) {
//            println(e.printStackTrace())
//            return ""
//        }

    }
}

class VenueFeed(val venues: List<Venue>)

data class Venue(
    val id : Int,
    val name : String,
    val location : String,
    val description : String
)
