
var userAPI = new Vue({
  el: "#userAPI",
  delimiters: ['${', '}'],
  data: {
    userLocal: null,
    user: null
  },
  // async created(){
  //   await this.loadID(),
  //   await console.log("print this")
  //
  // },
  mounted() {
    // console.log("this should be second.")
    // this.loadID().then( function() {
    //   this.loadUser()
    // }),
    // this.id = res.ID,
    this.loadID()
  },
  methods: {
    loadID: function() {
    this.$http.get(
      '/api/home'
    ).then(
      function(res) {
        this.userLocal = res.data,
        console.log("this should be first")
      },
      function(err) {
        console.error(err),
        console.log('error')
      },
    ).then( function() {
      if (this.userLocal){
        this.loadUser()
      }})
  },
    loadUser: function() {
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(res) {
          this.user = res.data
          console.log("this should be last")
        },
        function(err) {
          console.error(err)
        },
      )
    },
  },
})
