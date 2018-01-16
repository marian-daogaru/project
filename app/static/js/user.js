
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
      '/api/home'
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
      if (this.userLocal){
        this.loadUser()
      }})
  },
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
        },
      )
    },
  },
})


var editUserAPI = new Vue({
  el: "#editUserAPI",
  delimiters: ['${','}'],
  data:{
    nickname: '',
    aboutMe: '',
    pasword: '',
    confpwd: '',
    error: ''

  }, // data

  methods:
  {
    sendUpdate: function() {

    } // sendUpdate
  } // methods
}) // main brackets
