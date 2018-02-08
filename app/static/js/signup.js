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
          window.location.href = '/home'
        }
      })
    } //singUp function
  } // methods

}) // main brackets
