// import axios from 'axios';

// Vue.use(axios)


var baseAPI = new Vue({
  el: "#baseAPI",
  delimiters: ['${', '}'],
  data: {
    User: null,
    brandLocation: '/static/data/media/avatars/brand.png'
  },

  mounted() {
    this.loadUser()
  },

  methods: {
    loadUser: function() {
      this.$http.get(
        '/api/home'
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
  },  //methods
})

var general = new Vue({
  el: "#general",
  delimiters: ['${', '}'],
  data: {
  },
  methods: {
    goHome: function() {
      window.location.href = '/home'
    }
  }
})

// async created() {
//       this.user = await axios.get('/api/home', {
//           responseType: 'json'
//       });
//     }
