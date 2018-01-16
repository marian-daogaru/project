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

    pr: function() {
      console.log(document.getElementsByName("password")[0].valued),
      form = {email: this.email,
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
      ).then(function(){
        if (this.user.id !== '-1'){
          window.location.href = '/user/' + this.user.id
        }
      })
    }
  }
})
