package com.example.pickupsport

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.admin_home.view.*
import kotlinx.android.synthetic.main.admin_venue.view.*

class admin_venue : Fragment(){
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view =  inflater.inflate(R.layout.admin_venue, container, false)

        view.back_buttonvenue.setOnClickListener({
            // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(admin_home(), false)
        })

        fetchInfo()

        return view
    }
    private fun fetchInfo(): String {
        val url = "https://my-apad-project.appspot.com/app/venues"
        println("inside fetchinfo")

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        val response = client.newCall(request).execute()
        println("inside fetchinfo after execute")
        val bodyStr = response.body().string() // this can be consumed only once
        println("bodyStr")
        println(bodyStr)
        return bodyStr
    }
}
