package com.example.pickupsport

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.user_home.view.*

class user_home: Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // Inflate the layout for this fragment
        val view =  inflater.inflate(R.layout.user_home, container, false)

        view.logoutUser.setOnClickListener({
            // Navigate to the next Fragment.
            (activity as NavigationHost).navigateTo(LoginFragment(), false)
        })

        return view
    }
}