var groupAPI = new Vue({
  el: "#groupAPI",
  delimiters: ['${', '}'],
  data: {
    group: null,
    emails: '',
    errors: null,
    confirmation: null,
    response: null,
    isActive: false,
    ratingValue: 2,
    response: '',
    map: null,
    currentLocation: {
      lat: 44.4267288,
      lng: 26.1024337
    }  // default Unirii fountain location
  },

  mounted() {
    this.loadGroup()
  }, // mounted

  methods: {
    giveRating: function (restaurant, buttonNo){
      // this.isActive = true,
      this.$http.put(
        '/api/group/' + this.group.id + '/' + [this.group.userID, restaurant.id, buttonNo]
      ).then(
        function(response) {
          this.response = response.data,
          restaurant.userRating = buttonNo,
          restaurant.rating = this.response.rating,
          console.log(this.response)
        },
        function(err) {
          console.error(err),
          console.log("ERROR!!!")
        }
      ).then(
        function() {
          if (this.response.accessDenied){
            window.location.href = '/accessDenied'
          }
        }
      )
    },  // giveRating

    loadGroup: function() {
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(result) {
          this.group = result.data
        },
        function(err) {
          console.log(err),
          console.log('error')
        }).then( // first then
          function() {
            if (this.group) {
              if (this.group.id === -1){
                window.location.href = '/home'
              } else {
                var createMap = this.createMap
                this.getLocation().then(createMap)
              }
            }
          })  // second then
    },  // loadGroup

    editRedirect: function() {
      window.location.href = '/group/' + this.group.id + '/edit'
    },  // editRediect

    addPeople: function(){
      form = {
        emails: this.emails
      },
      console.log(form),
      this.$http.post(
        '/api/group/' + this.group.id, form
      ).then(
        function(response) {
          this.errors = response.data.errors,
          this.confirmation = response.data.added,
          this.emails = null,
          console.log(response)

        },
        function(err) {
          console.log(err),
          console.log('error')
        })
    },  // addPeople

    successfullyLeft: function(){
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Left",
        text: "You left the group successfully!",
        type: "success",
        closeOnConfirm: true,
        confirmButtonClass: 'btn-success',
        confirmButtonText: 'Go back to profile'
      },
      function() {
        console.log('/user/' + thisVue.response.id),
        window.location.href = '/user/' + thisVue.response.id
      })
    },

    leaveGroupAlert: function() {
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Are you sure you want to leave this group?",
        text: "You can come back later if you leave.",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: false,
        confirmButtonClass: 'btn-danger',
        confirmButtonText: 'Leave group',
      },
      function(){
        thisVue.leaveGroup(false)
      })
    },  //leaveGroupAlert

    leaveGroupAlertLastAdmin: function() {
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "You are the last admin!",
        text: "You are the last admin of this group. If you leave, the group will be deleted",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: false,
        confirmButtonClass: 'btn-danger',
        confirmButtonText: 'Leave group',
      },
      function(){
        thisVue.leaveGroup(true)
      })
    },  //finalAdmin

    leaveGroup: function(consentToLeave) {
      console.log(this.parent),
      console.log(this.group.id),
      form = {
        groupID: this.group.id,
        consent: consentToLeave
      },
      console.log(form)
      this.$http.post(
        '/api/group/leave', form
      ).then(
        function(res) {
          this.response = res.data
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(
        function() {
          if (this.response.lastAdmin){
            this.leaveGroupAlertLastAdmin()
          }
          if (this.response.left){
            this.successfullyLeft()
          }
        })
    },

    deleteGroupAlert: function () {
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Are you sure?",
        text: "Deleted groups cannot be recovered!",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: false,
        confirmButtonClass: 'btn-danger',
        confirmButtonText: 'Yes, delete group',
      },
      function(){
        thisVue.deleteGroup()
      })
    }, //deleteGroupAlert

    deleteGroup: function(){
      this.$http.delete(
        '/api/group/' + this.group.id + '/delete'
      ).then(
        function(response) {
          this.response = response.data,
          this.errors = response.data.errors,
          console.log(response)
        },
        function(err) {
          console.error(err),
          console.log('error')
        }).then(
          function(){
            if (this.response.deleted){
              this.successfullyLeft()
            }
          }
        )
    }, // deleteGroup

    addRestaurantRedirect: function() {
      window.location.href = '/group/' + this.group.id + '/addRestaurant'
    },  // addRestaurantRedirect

    removeRestaurant: function(restaurant) {
      console.log(restaurant);
      this.$http.delete(
        '/api/group/' + this.group.id + '/' + [this.group.userID, restaurant.id]
      ).then(
        function(response) {
          this.response = response.data,
          this.confirmation = response.data.confirmation,
          restaurant.rating = 0,
          console.log(this.response)
        },
        function(err) {
          console.error(err),
          console.log("ERROR!!!")
        }
      ).then(
        function() {
          if (this.response.accessDenied){
            window.location.href = '/accessDenied'
          }
        }
      )
    },  // remove Restaurant

    getLocation: function() {
      if (navigator.geolocation) {
          var self = this
          return new Promise(
            function(resolve, reject) {
              navigator.geolocation.getCurrentPosition(
                function(position) {
                  self.currentLocation.lat = parseFloat(position.coords.latitude),
                  self.currentLocation.lng = parseFloat(position.coords.longitude),
                  resolve(false)
                },
                function(err) {
                  console.log(err),
                  console.log("GMAPS ERROR"),
                  resolve(true)
                },
                {
                  enableHighAccuracy: true,
                  timeout: 10000,
                  maximumAge: 0
                })
              }
            )
      } else {
          return new Promise (
            function(resolve) {
              console.log("Geolocation is not supported by this browser."),
              resolve(true)
            }
          )
        }
    },

    createMap: function(defaultLocation) {
      console.log(this.currentLocation)
      this.map = new google.maps.Map(document.getElementById('map-canvas'), {
          center: this.currentLocation,
          zoom: 12,
          mapTypeId: 'roadmap'
        });

      if (!defaultLocation) {
        this.icon = {
          url:'http://maps.google.com/mapfiles/kml/paddle/blu-circle.png', // url
          scaledSize: new google.maps.Size(35, 35)
        },

        marker = new google.maps.Marker({
            position: this.currentLocation,
            map: this.map,
            icon: this.icon
          });
      }

      for (var i = 0; i < this.group.restaurants.length; i ++) {
        if (this.group.restaurants[i].lon) {
          marker = new google.maps.Marker({
              position: {
                lat: this.group.restaurants[i].lat,
                lng: this.group.restaurants[i].lon
              },
              map: this.map
            });
        }
      }

      // google.maps.event.trigger(this.map, "resize")
    }
  }  // methods
})  //groupAPI
