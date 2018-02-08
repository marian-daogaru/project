var loginAPI = new Vue({
  el: "#loginAPI",
  delimiters: ['${', '}'],
  data: {
    user: null,
    email: '',
    password: '',
    rememberMe: false,
    errors: null,
    response: '',
    secretKey: '',
    recaptchaRenderID: -1,
  },

  mounted() {
    this.loadUser(),
    this.initReCaptcha()
  },

  methods: {
    initReCaptcha: function() {
      var self = this;
      setTimeout(function() {
        if(typeof grecaptcha === 'undefined') {
          self.initReCaptcha();
        }
        else {
          self.recaptchaRenderID = grecaptcha.render('recaptchaDIV', {
              sitekey: self.secretKey,
              badge: 'inline',
              callback: self.submit
          });
        }
      }, 50);
    },
    submit: function(token) {
        console.log(token);
    },

    loadUser: function() {
      this.$http.get(
        '/api/login'
      ).then(
        function(res) {
          this.user = res.data
          this.secretKey = res.data.RECAPTCHA_SITE_KEY
        },
        function(err) {
          console.error(err),
          console.log('error')
        },
      )
    },

    login: function() {
      console.log(grecaptcha),
      console.log(typeof grecaptcha),
      form = {
        email: this.email,
        password: this.password,
        rememberMe: this.rememberMe,
        loginAttempts: this.user.loginAttempts
      }
      if (this.user.loginAttempts >= 3){
        form['recaptcha'] = grecaptcha.getResponse()
      }
      this.$http.post('/api/login', form).then(
        function(res) {
          this.user = res.data,
          this.errors = res.data.errors
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(
          function() {
            grecaptcha.reset(this.recaptchaRenderID)
            if (this.user.id !== -1){
              window.location.href = '/user/' + this.user.id
            }
          }
        )
    },  // login

    redirectSignUp: function(){
      window.location.href = '/signup'
    },

    resetPassword: function() {
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Are you sure!",
        text: "Please provide the email address for the account.",
        type: "input",
        showCancelButton: true,
        closeOnConfirm: false,
        inputPlaceholder: "email@domani.com",
        confirmButtonText: 'Send reset link',
      },
      function (inputValue) {
        if (inputValue === false) return false;
        if (inputValue === "") {
          swal.showInputError("You need to write something!");
          return false
        }
        thisVue.sendReset(inputValue)
        if (thisVue.sendReset(inputValue)) {
          alert('hello')
          swal.showInputError("Invalid Email!");
          return false
        }
        swal("Confirm!", "A password reset email was sent to " + inputValue, "success");
      })
    },

    sendReset: function(email) {
      this.$http.put(
        '/api/reset/nobodyisgoingtogethere/' + email
      ).then(
        function(response) {
          this.response = response.data
        },
        function(err) {
          console.log(err),
          console.log("ERROR")
        }
      )
    }
  }
})
