Vue.component("hello", {
  template: "<div><h1> Hellom {{name.id}}  hh! </h1> \
            <p><a href='{{ url_for(\"group\", id={{name.id}})}}'> Click me </a></p></div>",
  props: ['name']
})

var userAPI = new Vue({
  el: "#userAPI",
  delimiters: ['${', '}'],
  data: {
    user: null,
    id: ID,
  },
  mounted() {
    this.loadUser(),
    // this.id = res.ID,
    console.log(this.id),
    console.log(typeof this.id)
  },
  methods: {
    loadUser: function() {
      this.$http.get(
        '/api/user/' + this.id
      ).then(
        function(res) {
          this.user = res.data
        },
        function(err) {
          console.error(err)
        },
      )
    },
  },
})
