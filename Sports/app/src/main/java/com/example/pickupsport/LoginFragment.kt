package com.example.pickupsport

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.google.gson.JsonParser
//import com.squareup.okhttp.*
import okhttp3.*
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.admin_home.*
import kotlinx.android.synthetic.main.listing_fragment.*
import kotlinx.android.synthetic.main.listing_fragment.view.*
import kotlinx.android.synthetic.main.listing_fragment.view.menulist
import kotlinx.android.synthetic.main.login_fragment.*
import kotlinx.android.synthetic.main.login_fragment.view.*
import kotlinx.android.synthetic.main.login_fragment.view.username_edit_text
import org.jetbrains.anko.activityUiThread
import org.jetbrains.anko.doAsync
import kotlinx.android.synthetic.main.listing_fragment.view.*
import org.jetbrains.anko.uiThread

/**
 * Fragment representing the login screen for Shrine.
 */
class LoginFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.login_fragment, container, false)

        view.admin_button.setOnClickListener{
            doAsync {
                Log.d("DEBUG", "button clicked");

                println("email: " + username_edit_text.text.toString())
                println("password: " + password_edit_text.text.toString())

                val url = "https://my-apad-project.appspot.com/app/admin"
                val map: HashMap<String, String> = hashMapOf("email" to username_edit_text.text.toString(), "password" to password_edit_text.text.toString())
                val invalidMap: HashMap<String, String> = hashMapOf("email" to "", "password" to "")
                val notAdminMap: HashMap<String, String> = hashMapOf("email" to "lebron@lakers.com", "password" to "cav")

                val client = OkHttpClient()
                val req = OkHttpRequest(client)
                val resp = req.fetchPost(url, map)
                val invalidResp = req.fetchPost(url, invalidMap)
                val notAdminResp = req.fetchPost(url, notAdminMap)
                println("resp: " + resp)
                println(resp?.javaClass?.name)


                uiThread {
                    if (resp.equals(notAdminResp)) {
                        println("Not admin")
                        password_text_input.error = getString(R.string.error_admin)
                    } else if (resp.equals(invalidResp)) {
                        println("Wrong credentials")
                        password_text_input.error = getString(R.string.error_invalid)
                    } else {
                        password_text_input.error = null
                        // Navigate to the next Fragment.
                        (activity as NavigationHost).navigateTo(admin_home(), false)
                    }
                }

            }
        }

        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        view.next_button.setOnClickListener {
            doAsync {
                Log.d("DEBUG", "button clicked");

                println("email: " + username_edit_text.text.toString())
                println("password: " + password_edit_text.text.toString())

                val url = "https://my-apad-project.appspot.com/app/login"
                val map: HashMap<String, String> = hashMapOf("email" to username_edit_text.text.toString(), "password" to password_edit_text.text.toString())
                val invalidMap: HashMap<String, String> = hashMapOf("email" to "", "password" to "")

                val client = OkHttpClient()
                val req = OkHttpRequest(client)
                val resp = req.fetchPost(url, map)
                val invalidResp = req.fetchPost(url, invalidMap)
                println("resp: " + resp)
                println(resp?.javaClass?.name)


                uiThread {
                    if (!resp.equals(invalidResp)) {
                        println("Logged in")
                        password_text_input.error = null
                        // Navigate to the next Fragment.
                        (activity as NavigationHost).navigateTo(user_home(), false)
                    } else {
                        println("Wrong credentials")
                        password_text_input.error = getString(R.string.error_invalid)
                    }
                }

            }
        }

        view.username_edit_text.setOnKeyListener({ _, _, _ ->
            // Clear the error once user tries to change username
            password_text_input.error = null
            false
        })

        view.password_edit_text.setOnKeyListener({ _, _, _ ->
            // Clear the error once user tries to change password
            password_text_input.error = null
            false
        })
    }

    private fun fetchInfo() {
        val url = "https://my-apad-project.appspot.com/app/login"

        val map: HashMap<String, String> = hashMapOf("email" to "lebron@lakers.com", "password" to "cav")

        val json = """
        "{\n" +
            "    \"email\": \"lebron@lakers.com\",\n" +
            "    \"password\": \"cav\"\n" +
            "}"
        """.trimIndent()



        /*val body = RequestBody.create(MediaType.parse("application/json; charset=utf-8"), json)
        val client = OkHttpClient()
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onResponse(call: Call, response: Response) {
                val body = response?.body()?.string()
                println(body)
            }

            override fun onFailure(call: Call, e: IOException) {
                println("failed")
            }
        })*/

       /* try {
//            val response = client.newCall(request).execute()
            println("inside fetchinfo after execute")
//            val bodyStr = response.body().string() // this can be consumed only once
            println("bodyStr")
//            println(bodyStr)
            return "test"
        } catch (e: Exception) {
            println(e.printStackTrace())
            return ""
        }*/



    }
}




