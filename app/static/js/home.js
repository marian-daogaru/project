var home = new Vue({
  el: "#home",
  delimiters: ['${', '}'],
  data: {
    latestRestaurants: '',
    latestReviews: ''
  },

  mounted() {
    this.loadLatest()
  },

  methods: {
    loadLatest: function() {
      this.$http.get(
        '/api/home/'
      ).then(
        function(response) {
          this.latestRestaurants = response.data.latestRestaurants,
          this.latestReviews = response.data.latestReviews
        },
        function(err) {
          console.log(err),
          console.log("ERROR")
        }
      )
    }
  } // methods
})
