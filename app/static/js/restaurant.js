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
    userReview: '',
    user: '',
    response: ''
  },

  mounted() {
    this.loadRestaurant(),
    this.loadUser()
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
    loadUser: function(){
      this.$http.get(
        '/api/home'
      ).then(
        function(response) {
          this.user = response.data
        },
        function(err) {
          console.log(err),
          console.log('ERROR')
        }
      )
    },  // loadUser

    redirectWebsite: function(){
      window.location = this.restaurant.website
    },

    submitReview: function(){
      console.log(this.userReview),
      console.log('/api/restaurant/' + this.restaurant.id + '/user/' + this.user.id + '/' + this.userReview)
      if (this.userReview.length > 0) {
        this.$http.put(
          '/api/restaurant/' + this.restaurant.id + '/user/' + this.user.id + '/' + this.userReview
        ).then(
          function(response) {
            this.response = response.data,
            this.errors = response.data.errors
            console.log(this.response)
          },
          function(err){
            console.log(err),
            console.log("ERROR")
          }
        ).then(
          function() {
            if (this.response.accessDenied){
              window.location.href = '/accessDenied'
            }
          }
        )
      }
    }  // submitReview
  }  //methods
})  // restaurantAPI


var searchRestaurantAPI = new Vue({
  el: "#searchRestaurantAPI",
  delimiters: ['${','}'],
  data:{
    restaurants: null,
    errors: null,
    confirmations: null,
    restaurantName: ''
  },

  mounted() {
    this.loadSearch()
  },

  methods: {
    loadSearch: function() {
      console.log('/restaurant/search/'.length)
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
