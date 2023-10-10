var B = {

    // ---------------------------------------
    // trips
    // ---------------------------------------

    inittripupdate: function (row, vars) {
        return {
            tripdate: [vars.start_time, vars.end_time]
        }
    },

    gettripsdelpars: function (row, vars) {
        return {
            method: "DELETE",
            restaction: "trips/action",
            params: { what: "delete", pk: row.pk_trips }
        }
    },

    getexpandtrips: function (row, vars) {
        return {
            list: "trips/liste",
            params: { trip_id : row.pk_trips },
            props : J.getexpandstyledown()
        };

    },

    gettripstags: function(row,vars) {

        var res = []
        var name = "transportation"
        var color = "green" 
        if (row.eventtype == 1) {
            name = "flight"
            color = "red"
        }
        if (row.eventtype == 2) {
            name = "stay"
            color = "cyan"
        }
        res.push({
            value: { messagedirect: name },
            props: { color: color}
        })
        return res
    },

    // ------------------
    // users
    // ------------------

    getusersdelpars: function (row, vars) {
        return {
            method: "DELETE",
            restaction: "users/action",
            params: { what: "delete", pk: row.pk_users }
        }

    },

    // ----------------------------
    // transportation
    // ----------------------------

    inittransportationpars: function (row, vars) {
        J.log("initransportationpars", row, vars)
        var tripid = vars.pk_trips
        return {
            method: "GET",
            restaction: "transportation/list",
            params: { trip_id: tripid }
        }

    },

    gettransportationdelpars: function (row, vars) {
        return {
            method: "DELETE",
            restaction: "transportation/action",
            params: { what: "delete", pk: row.pk_ground_transportation }
        }
    },

    // ----------------------------
    // flights
    // ----------------------------

    initflighpars: function (row, vars) {
        var tripid = vars.pk_trips
        return {
            method: "GET",
            restaction: "flight/list",
            params: { trip_id: tripid }
        }

    },

    getflightdelpars: function (row, vars) {
        return {
            method: "DELETE",
            restaction: "flight/action",
            params: { what: "delete", pk: row.pk_flights }
        }
    },

    // ----------------------------
    // stays
    // ----------------------------

    initstayspars: function (row, vars) {
        var tripid = vars.pk_trips
        return {
            method: "GET",
            restaction: "stays/list",
            params: { trip_id: tripid }
        }

    },

    getstaysdelpars: function (row, vars) {
        return {
            method: "DELETE",
            restaction: "stays/action",
            params: { what: "delete", pk: row.pk_stays }
        }
    },


}