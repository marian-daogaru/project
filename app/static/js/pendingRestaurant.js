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
