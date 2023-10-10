var J = {

    log: function(mess, row, vars) {
        console.log("ENTERING =====" + mess)
        console.log(row)
        console.log(vars)
        console.log("LEAVING =====" + mess)
    },

    tranformdate : function(row, f) {
        if (row[f] === undefined) return undefined
        return row[f].substring(0,10)
    },

    getexpandstyle: function () {
        return {
          style: {
            backgroundColor: "#ece6e2",
            boxShadow: '0 0 10px rgba(0, 0, 0, 0.3)',
            margin: "10px"
          }
        }
      },

      getexpandstyledown: function () {
        return {
          style: {
            backgroundColor: "#ecf2f473",
            boxShadow: '0 0 10px rgba(0, 0, 0, 0.3)',
            margin: "10px"
          }
        }
      },

}