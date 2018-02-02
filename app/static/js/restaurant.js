var addRestaurantAPI = new Vue({
  el: "#addRestaurantAPI",
  delimiters: ['${','}'],
  data:{
      group: null,
      restaurantName: '',
      restaurantURL: '',
      errors: '',
      confirmations: '',
      restaurants: '',
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

// -----------------------------------------------------------------------------
// RESTAURANT API
// -----------------------------------------------------------------------------
var restaurantAPI = new Vue({
  el: "#restaurantAPI",
  delimiters: ['${','}'],
  data:{
    errors: '',
    restaurant: null,
    userReview: '',
    user: '',
    response: '',
    reviews: '',
    extension: '../',
    map: null
  },

  mounted() {
    this.loadUser(),
    this.loadRestaurant()
  },

  methods: {
    loadMap: function() {
      console.log('maps: ', google.maps),
      console.log(document.getElementById('map')),
      position = {
                  lat: parseFloat(this.restaurant.details.lat),
                  lng: parseFloat(this.restaurant.details.lon)
                }
      this.map = new google.maps.Map(document.getElementById('map'), {
          center: position,
          zoom: 16,
          mapTypeId: 'roadmap'
        });
      marker = new google.maps.Marker({
          position: position,
          map: this.map
        });
      // google.maps.event.trigger(this.map, "resize")
    },

    loadRestaurant: function(){
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(response) {
          this.restaurant = response.data,
          this.errors = response.data.errors
          if (this.restaurant.groupID) {
            this.extension = '../../../'
          }
        },
        function(err) {
          console.log(err),
          console.log('ERROR')
        }
      ).then(
          function() {
            this.loadReviews()
            if (this.restaurant.details && this.restaurant.details.lon) {
              this.loadMap()
            }
          }
        )
    },  // loadRestaurant

    loadUser: function(){
      this.$http.get(
        '/api/home/id'
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

    loadReviews: function() {
      this.$http.get(
        '/api' + window.location.pathname + '/reviews'
      ).then(
        function(response) {
          this.reviews = response.data,
          console.log(this.reviews)
        },
        function(err) {
          console.log(err),
          console.log("ERROR")
        }
      )
    },  // loadReview

    redirectWebsite: function(){
      window.open(this.restaurant.website, '_blank')
      if (this.restaurant.groupID) {
        this.$http.put(
          '/api/group/' + this.restaurant.groupID + '/restaurant/' + this.restaurant.id
        ).then(
          function(response) {
            this.response = response.data,
            this.errors = response.data.errors
          },
          function(err) {
            console.log(err),
            console.log("ERROR")
          }
        )
      }
    },

    submitReview: function(){
      console.log(this.userReview),
      console.log('/api/restaurant/' + this.restaurant.id + '/user/' + this.user.id + '/' + this.userReview)
      if (this.userReview.length > 0) {
        this.$http.put(
          '/api' + window.location.pathname + '/user/' + this.user.id + '/' + this.userReview
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
            this.userReview = null,
            this.loadReviews()
            // if (this.reviews.length > 0) {
            //   for (review in this.reviews){
            //     console.log(this.reviews[review].userID),
            //     console.log(parseInt(this.user.id)),
            //     console.log(parseInt(this.user.id) === parseInt(this.reviews[review].userID))
            //     if (parseInt(this.user.id) === parseInt(this.reviews[review].userID)){
            //       this.reviews[review].review = this.userReview
            //     }
            //   }
            // } else {
            //   this.loadReviews()
            // }
          }
        )
      }
    }  // submitReview
  }  //methods
})  // restaurantAPI

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


// -----------------------------------------------------------------------------
// PENDING RESTAURANT
// -----------------------------------------------------------------------------
var pendingRestaurantAPI = new Vue({
  el: "#pendingRestaurantAPI",
  delimiters: ['${','}'],
  data:{
    restaurants: '',
    checkedRestaurants: [],
    groupID: -1,
    confirmations: null,
    errors: null,
    response: ''
  },

  mounted() {
    this.loadPending()
  },

  methods: {
    loadPending: function() {
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(response) {
          this.restaurants = response.data.restaurants,
          this.groupID = response.data.groupID,
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
    },  // loadPending

    addChecked: function() {
      if (this.checkedRestaurants.length > 0) {
        this.$http.put(
          '/api/group/' + this.groupID + '/edit/pendingRestaurants/' + this.checkedRestaurants
        ).then(
          function(response) {
            this.response = response.data,
            this.confirmations = response.data.confirmations,
            this.errors = response.data.errors
          },
          function(err) {
            console.log(err),
            console.log("ERROR")
          }
        ).then(
          function() {
            if (this.confirmations) {
              this.loadPending()
            }
            if (this.response.accessDenied) {
              window.location.href = '/accessDenied'
            }
          }
        )
      } else {
        this.errors = ['Please select at least one restaurant to be added.']
      }
    },  // addChecked

    removeChecked: function() {
      if (this.checkedRestaurants.length > 0) {
        this.$http.delete(
          '/api/group/' + this.groupID + '/edit/pendingRestaurants/' + this.checkedRestaurants
        ).then(
          function(response) {
            this.response = response.data,
            this.confirmations = response.data.confirmations,
            this.errors = response.data.errors
          },
          function(err) {
            console.log(err),
            console.log("ERROR")
          }
        ).then(
          function() {
            if (this.confirmations) {
              this.loadPending()
            }
            if (this.response.accessDenied) {
              window.location.href = '/accessDenied'
            }
          }
        )
      } else {
        this.errors = ['Please select at least one restaurant to be added.']
      }
    },  // addChecked


    redirectGroup: function() {
      window.location.href = '/group/' + this.groupID
    }
  }  // methods
})
