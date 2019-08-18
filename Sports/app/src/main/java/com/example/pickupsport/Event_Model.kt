package com.example.pickupsport

class Event_Model {

    var organizer: String? = null
    var description: String? = null
    var time: String? = null


    fun getOrganizers(): String {
        return organizer.toString()
    }

    fun setOrganizers(organizer: String) {
        this.organizer = organizer
    }


    fun getDescriptions(): String {
        return description.toString()
    }

    fun setDescriptions(description: String) {
        this.description = description
    }


    fun getTimes(): String {
        return time.toString()
    }

    fun setTimes(time: String) {
        this.time = time
    }



}