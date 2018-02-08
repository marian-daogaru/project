// import axios from 'axios';

// Vue.use(axios)


var baseAPI = new Vue({
  el: "#baseAPI",
  delimiters: ['${', '}'],
  data: {
    User: null,
    brandLocation: '/static/data/media/avatars/brand.png',
    restaurantName: ''
  },

  mounted() {
    this.loadUser()
  },

  methods: {
    loadUser: function() {
      this.$http.get(
        '/api/home/id'
      ).then(
        function(res) {
          this.User = res.data
        },
        function(err) {
          console.error(err),
          console.log('error')
        },
      )
    },  // loadUser

    searchRestaurantRedirect: function() {
      console.log(this.restaurantName.length)
      if (this.restaurantName.length > 0) {
        window.location.href = '/restaurant/search/' + this.restaurantName
      }
    }  //searchRestaurant
  },  //methods
})
