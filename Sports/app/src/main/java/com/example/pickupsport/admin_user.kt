package com.example.pickupsport

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.admin_user.view.*
import okhttp3.*
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import java.io.IOException
import kotlinx.android.synthetic.main.admin_venue.view.*
import org.json.JSONException
import java.lang.Exception
import java.util.ArrayList
import android.widget.ArrayAdapter
import android.widget.ListView
import kotlinx.android.synthetic.main.listing_fragment.view.*
import org.jetbrains.anko.uiThread

class admin_user : Fragment(){

    private var response: String? = null
    private var userlist: ListView? = null
    private var userModelArrayList: ArrayList<User_Model>? = null
    private var customAdapter: CustomAdapter? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view =  inflater.inflate(R.layout.admin_user, container, false)
        view.back_buttonuser.setOnClickListener({
            // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(admin_home(), false)
        })

        doAsync {
            val users = getUsers()
            response = users
            uiThread {
                println("response")
                println(response)
                userlist = view.userlist
                userModelArrayList = getInfo(response!!)
                customAdapter = CustomAdapter(view.context, userModelArrayList!!)
                userlist!!.adapter = customAdapter

            }
        }

        return view
    }

     fun getUsers() : String? {

        val url = "https://my-apad-project.appspot.com/app/users"

        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        val response = client.newCall(request).execute()
        val bodyStr =  response?.body()?.string() // this can be consumed only once
        println("bodyStr")
        println(bodyStr)
        return bodyStr
    }


    fun getStrings(response: String): ArrayList<String> {
        val userArrayList = ArrayList<String>()
        try {
            val dataArray = JSONArray(response)
            for (i in 0 until dataArray.length()) {
                val dataobj = dataArray.getJSONObject(i)
                userArrayList.add(dataobj.toString())
            }
        } catch (e: JSONException) {
            e.printStackTrace()
        }

        return userArrayList
    }

    fun getInfo(response: String): ArrayList<User_Model> {
        val userModelArrayList = ArrayList<User_Model>()
        try {
            val dataArray = JSONArray(response)
            for (i in 0 until dataArray.length()) {
                val usersModel = User_Model()
                val dataobj = dataArray.getJSONObject(i)
                usersModel.setNames(dataobj.getString("name"))
                usersModel.setPhones(dataobj.getString("phone"))
                usersModel.setPasswords(dataobj.getString("password"))
                usersModel.setIds(dataobj.getInt("id"))
                usersModel.setEmails(dataobj.getString("email"))
                userModelArrayList.add(usersModel)
            }
        } catch (e: JSONException) {
            e.printStackTrace()
        }

        return userModelArrayList
    }

    fun loadJSONFromAssets(): String? {
        var json: String? = null
        try {
            val inputStream = this.context?.assets?.open("users.json")
            val size = inputStream?.available()
            val buffer = ByteArray(size!!)
            inputStream.read(buffer)
            inputStream.close()

            json = String(buffer, Charsets.UTF_8)
        } catch (e: IOException) {
            e.printStackTrace()
        }

        return json
    }
}