var userAPI = new Vue({
  el: "#userAPI",
  delimiters: ['${', '}'],
  data: {
    userLocal: null,
    user: null
  },

  mounted() {
    this.loadID()
  },

  methods: {
    loadID: function() {
    this.$http.get(
      '/api/home/id'
    ).then(
      function(res) {
        this.userLocal = res.data,
        console.log("this should be first")
      },
      function(err) {
        console.error(err),
        console.log('error')
      },
    ).then( function() {
      if (this.userLocal && window.location.pathname.substring(0, 5) === '/user') {
        this.loadUser()
      }})
    },  // loadID

    loadUser: function() {
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(res) {
          this.user = res.data
          console.log("this should be last")
        },
        function(err) {
          console.error(err)
          if (err.status === 404) {
            window.location.href = '/404'
          }
        },
      ).then(
        function() {
          if (this.user.accessDenied){
            window.location.href = '/accessDenied'
          }
        }
      )
    },  // loadUser

    redirectEdit: function() {
      window.location.href = '/edit'
    },  // redirectEdit

    redirectCreateGroup: function() {
      window.location.href = '/createGroup'
    }  // redirectCreateGroup
  },
})
