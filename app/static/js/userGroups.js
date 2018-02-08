var userGroupsAPI = new Vue({
  el: "#userGroupsAPI",
  delimiters: ['${', '}'],
  data: {
    groups: null,
    user: null,
    accessDenied: null,
    userLocal: null,
  },

  mounted() {
    this.loadGroups()
  },

  methods: {
    loadGroups: function() {
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(response) {
          this.groups = response.data.groups,
          this.user = response.data.user,
          this.userLocal = response.data.userLocal,
          this.accessDenied = response.data.accessDenied
        },
        function(err) {
          console.error(err)
        },
      ).then(
        function() {
          if (this.accessDenied){
            window.location.href = '/accessDenied'
          }
        }
      )
    }  // loadGroups
  },
})
