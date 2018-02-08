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
