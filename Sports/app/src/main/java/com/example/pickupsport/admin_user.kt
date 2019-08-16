package com.example.pickupsport

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.admin_user.view.*
import kotlinx.android.synthetic.main.admin_venue.view.*

class admin_user : Fragment(){
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view =  inflater.inflate(R.layout.admin_user, container, false)

        view.back_buttonuser.setOnClickListener({
            // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(admin_home(), false)
        })
        // Set an error if the password is less than 8 characters.
        /*view.back_button.setOnClickListener({
            // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(LoginFragment(), false)
        })*/
        return view
    }
}