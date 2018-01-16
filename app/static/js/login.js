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
