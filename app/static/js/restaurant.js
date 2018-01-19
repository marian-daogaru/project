var addRestaurantAPI = new Vue({
  el: "#addRestaurantAPI",
  delimiters: ['${','}'],
  data:{
      group: null,
      restaurantName: '',
      restaurantURL: '',
      errors: '',
      confirmations: '',
      restaurants: null,
      checkedRestaurants: [],
    },

  mounted() {
    this.loadGroup()
  },

  methods: {
    loadGroup: function() {
      if (window.location.pathname.substring(0, 6) === '/group'){
        this.$http.get(
          '/api' + window.location.pathname
        ).then(
          function(response) {
            this.group = response.data
          },
          function(err) {
            console.error(err),
            console.log('error')
          }
        ).then(  // first then
            function() {
              if (this.group.accessDenied) {
                window.location.href = '/accessDenied'
              }
            }
          )
      }  // if
    }, //loadGroup
    searchRestaurant: function() {
      this.checkedRestaurants = [],
      console.log('search button!'),
      console.log(this.restaurantName),
      this.$http.get(
        '/api/group/' + this.group.id + '/addRestaurant/' + this.restaurantName
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

    addNewRestaurant: function() {
      form = {
        restaurantURL: this.restaurantURL
      },
      this.confirmations = '',
      console.log('search button!'),
      console.log(this.restaurantURL),
      this.$http.post(
        '/api/group/' + this.group.id + '/addRestaurant', form
      ).then(
        function(response) {
          this.response = response.data,
          this.errors = response.data.errors,
          this.confirmations = response.data.confirmations,
          console.log(this.response)
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      )
    },  // addNewRestaurant

    addCheckRestaurants: function() {
      console.log("HEEEYYY"),
      this.confirmations = '',
       this.$http.put(
         '/api/group/' + this.group.id + '/addRestaurant/' + this.checkedRestaurants
       ).then(
         function(response) {
           console.log(response.data),
           this.confirmations = response.data.confirmations,
           this.checkedRestaurants = []
         },
         function(err) {
           console.log(err),
           console.log('error')
         }
       ).then(
         function() {
           if (this.confirmations){
             this.searchRestaurant()
           }
         }
       )
    },

    goBackGroup: function() {
      window.location.href = '/group/' + this.group.id
    } // goBackGroup
  }
})


var restaurantAPI = new Vue({
  el: "#restaurantAPI",
  delimiters: ['${','}'],
  data:{
    errors: '',
    restaurant: null,
  },

  mounted() {
    this.loadRestaurant()
  },

  methods: {
    loadRestaurant: function(){
      if (window.location.pathname.substring(0, 6) === '/resta'){
        this.$http.get(
          '/api' + window.location.pathname
        ).then(
          function(response) {
            this.restaurant = response.data,
            this.errors = response.data.errors
          },
          function(err) {
            console.log(err),
            console.log('ERROR')
          }
        )
      }
    },  // loadRestaurant

    redirectWebsite: function(){
      window.location = this.restaurant.website
    }
  }  //methods
})  // restaurantAPI
