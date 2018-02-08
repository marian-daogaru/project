var confirmAPI = new Vue({
  el: "#confirmAPI",
  delimiters: ['${','}'],
  data:{
    response: '',
    errors: '',
  },

  mounted() {
    this.loadConfirmation()
  },

  methods: {
    loadConfirmation: function() {
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(response) {
          console.log("hello2")
          this.response = response.data,
          this.errors = response.data.errors
        },
        function(err) {
          console.log(err),
          console.log("ERROR")
        }
      )
    },

    loginRedirect: function() {
      window.location.href = '/login'
    }
  }
})
