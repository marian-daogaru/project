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
    }
  } // methods
})  // passwordReset
