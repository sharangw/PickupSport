package com.example.pickupsport

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.squareup.okhttp.*
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.admin_home.*
import kotlinx.android.synthetic.main.listing_fragment.*
import kotlinx.android.synthetic.main.listing_fragment.view.*
import kotlinx.android.synthetic.main.listing_fragment.view.userlist
import kotlinx.android.synthetic.main.login_fragment.*
import kotlinx.android.synthetic.main.login_fragment.view.*
import kotlinx.android.synthetic.main.login_fragment.view.username_edit_text
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONObject
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

        //val view =  inflater.inflate(R.layout.listing_fragment, container, false)
        view.next_button.setOnClickListener({
            // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(ListingFragment(), false)
        })

        view.admin_button.setOnClickListener({
            // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(admin_home(), false)
        })

        view.next_button.setOnClickListener {
            doAsync {
                Log.d("DEBUG", "button clicked");
                val gotresponse = fetchInfo()
                Log.d("DEBUG", "fetching info");
//                val jsonarray = JSONArray(gotresponse)
                val user = JSONObject(gotresponse)
                if (user.toString() == "Invalid") {
                    println("Invalid")
                }

                if (user.get("email").equals(username_edit_text.text.toString())){
                        print("This is right!")
                    }
                //val venue = jsonarray.getJSONObject(i)
            }
        }
        return view
    }

    private fun fetchInfo(): String {
        val url = "https://my-apad-project.appspot.com/app/login"
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




