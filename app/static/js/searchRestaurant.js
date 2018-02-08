// -----------------------------------------------------------------------------
// SEARCH RESTAURANT
// -----------------------------------------------------------------------------
var searchRestaurantAPI = new Vue({
  el: "#searchRestaurantAPI",
  delimiters: ['${','}'],
  data:{
    restaurants: '',
    errors: null,
    confirmations: null,
    restaurantName: ''
  },


  mounted() {
    this.loadSearch()
  },

  methods: {
    loadSearch: function() {
      if (window.location.pathname.substring(0, 19) === '/restaurant/search/'){
        this.$http.get(
          '/api' + window.location.pathname
        ).then(
          function(response) {
            this.restaurants = response.data,
            console.log(this.restaurants.length)
          },
          function(err) {
            console.error(err),
            console.log('error')
          }
        ).then(
          function() {
            if (this.restaurants.accessDenied) {
              window.location.href = '/accessDenied'
            }
          }
        )

      }
    },  // loadSearch

    searchRestaurant: function() {
        this.$http.get(
        '/api/restaurant/search/' + this.restaurantName
      ).then(
        function(response) {
          this.restaurants = response.data,
          console.log(this.restaurants.length),
          console.log(typeof this.restaurants)
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      )
    },  //searchRestaurant
  }  // methods
})
