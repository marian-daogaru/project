// import axios from 'axios';

// Vue.use(axios)


var baseAPI = new Vue({
  el: "#baseAPI",
  delimiters: ['${', '}'],
  data: {
    User: null
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
    },
  },
})


// async created() {
//       this.user = await axios.get('/api/home', {
//           responseType: 'json'
//       });
//     }
