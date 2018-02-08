// -----------------------------------------------------------------------------
// PENDING RESTAURANT
// -----------------------------------------------------------------------------
var pendingUserAPI = new Vue({
  el: "#pendingUserAPI",
  delimiters: ['${','}'],
  data:{
    users: '',
    checkedUsers: [],
    groupID: -1,
    confirmations: null,
    errors: null,
    response: ''
  },

  mounted() {
    this.loadPending()
  },

  methods: {
    loadPending: function() {
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(response) {
          this.users = response.data.users,
          this.groupID = response.data.groupID
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(
        function() {
          if (this.users.accessDenied) {
            window.location.href = '/accessDenied'
          }
        }
      )
    },  // loadPending

    addChecked: function() {
      if (this.checkedUsers.length > 0) {
        this.$http.put(
          '/api/group/' + this.groupID + '/edit/pendingUsers/' + this.checkedUsers
        ).then(
          function(response) {
            this.response = response.data,
            this.confirmations = response.data.confirmations,
            this.errors = response.data.errors
          },
          function(err) {
            console.log(err),
            console.log("ERROR")
          }
        ).then(
          function() {
            if (this.confirmations) {
              this.loadPending()
            }
            if (this.response.accessDenied) {
              window.location.href = '/accessDenied'
            }
          }
        )
      } else {
        this.errors = ['Please select at least one user to be added.']
      }
    },  // addChecked

    removeChecked: function() {
      if (this.checkedUsers.length > 0) {
        this.$http.delete(
          '/api/group/' + this.groupID + '/edit/pendingUsers/' + this.checkedUsers
        ).then(
          function(response) {
            this.response = response.data,
            this.confirmations = response.data.confirmations,
            this.errors = response.data.errors
          },
          function(err) {
            console.log(err),
            console.log("ERROR")
          }
        ).then(
          function() {
            if (this.confirmations) {
              this.loadPending()
            }
            if (this.response.accessDenied) {
              window.location.href = '/accessDenied'
            }
          }
        )
      } else {
        this.errors = ['Please select at least one user to be added.']
      }
    },  // removeChecked

    redirectGroup: function() {
      window.location.href = '/group/' + this.groupID
    }
  }  // methods
})
