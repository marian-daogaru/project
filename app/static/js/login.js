var loginAPI = new Vue({
  el: "#loginAPI",
  delimiters: ['${', '}'],
  data: {
    user: null,
    email: '',
    password: '',
    rememberMe: false,
    errors: null,
  },

  mounted() {
    this.loadUser()
  },

  methods: {
    loadUser: function() {
      this.$http.get(
        '/api/login'
      ).then(
        function(res) {
          this.user = res.data
        },
        function(err) {
          console.error(err),
          console.log('error')
        },
      )
    },

    login: function() {
      console.log(document.getElementsByName("password")[0].valued),
      form = {
        email: this.email,
        password: this.password,
        rememberMe: this.rememberMe
      },
      this.$http.post('/api/login', form).then(
        function(res) {
          this.user = res.data,
          this.errors = res.data.errors
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(function() {
        if (this.user.id !== -1){
          window.location.href = '/user/' + this.user.id
        }
      })
    }
  }
})

var signupAPI = new Vue({
  el: "#signupAPI",
  delimiters: ['${','}'],
  data:{
    email: '',
    password: '',
    confpwd: '',
    rememberMe: false,
    errors: null
  }, // data

  methods:
  {
    signUp: function(){
      form = {email: this.email,
              password: this.password,
              confpwd: this.confpwd,
              rememberMe: this.rememberMe
      },
      console.log(form),
      this.$http.post('/api/signup', form).then(
        function(res) {
          this.user = res.data,
          this.errors = res.data.errors
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(function() {
        console.log("asdas")
      }).then(function() {
        if (this.user.id !== -1){
          window.location.href = '/user/' + this.user.id
        }
      })
    } //singUp function
  } // methods

}) // main brackets


var passwordReset = new Vue({
  el: "#passwordReset",
  delimiters: ['${','}'],
  data:{
    password: '',
    confpwd: '',
    errors: null,
    response: '',
    email: ''
  }, // data
  mounted() {
    this.loadUser()
  },

  mounted() {
    this.loadToken()
  },

  methods: {
    loadToken: function() {
      console.log("hello")
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(response) {
          console.log("hello2")
          this.response = response.data,
          this.errors = response.data.errors,
          this.email = response.data.email
        },
        function(err) {
          console.log(err),
          console.log("ERROR")
        }
      )
    },

    resetPWD: function() {
      form = {
          email: this.email,
          password: this.password,
          confpwd: this.confpwd
        },
      this.$http.post(
        '/api' + window.location.pathname, form
      ).then(
        function(response) {
          this.response = response.data,
          this.errors = response.data.errors
        },
        function(err) {
          console.log(err),
          console.log("ERROR")
        }
      ).then(
        function() {
          if (this.response.unlocked){
            this.successfulReset()
          }
        }
      )
    },

    successfulReset: function(){
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Reset Successful",
        text: "You successfully reset your password!",
        type: "success",
        closeOnConfirm: true,
        confirmButtonClass: 'btn-success',
        confirmButtonText: 'OK.'
      },
      function() {
        window.location.href = '/login'
      })
    },
  } // methods
})  // passwordReset
