var editGroupAPI = new Vue({
  el: "#editGroupAPI",
  delimiters: ['${','}'],
  data:{
    group: null,
    checkedIDs: [],
    kickIDs: [],
    errors: '',
    name: '',
    aboutGroup: '',
    avatar: '',
    update: ''
  }, // data

  mounted() {
    this.loadGroup()
  },  // mounted

  methods: {
    loadGroup: function() {
      console.log("hello"),
      path =   window.location.pathname
      if (window.location.pathname.substring(0, 6) === '/group' &&
          window.location.pathname.slice(-5) === '/edit'){
        this.$http.get(
          '/api' + window.location.pathname
        ).then(
          function(response) {
            this.group = response.data,
            this.name = this.group.name,
            this.aboutGroup = this.group.aboutGroup,
            this.kickIDs.push(this.group.id)
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

    sendUpdate: function(){
      form = {
        name: this.name,
        aboutGroup: this.aboutGroup,
        avatar: this.avatar,
        ids: this.checkedIDs
      },
      this.$http.post(
        '/api/group/' + this.group.id + '/edit', form
      ).then(
        function(response) {
          this.errors = response.data.errors,
          this.updated = response.data.updated
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(
        function() {
          if (this.updated) {
            window.location.href = '/group/' + this.group.id
          }
        }
      )
    },  // sendUpdate

    onFileChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
      this.createImage(files[0]);
    },

    createImage(file) {
      var image = new Image();
      var reader = new FileReader();
      var vm = this;

      reader.onload = (e) => {
        this.avatar = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    kickPeople: function() {
      console.log('/api/group/-1/edit/' + this.kickIDs),
      this.$http.delete(
        '/api/group/-1/edit/' + this.kickIDs
      ).then(
        function(response) {
          console.log(response.data),
          console.log('hello')
          if (response.data.removed){
            this.loadGroup()
          }
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      )
    },

    goBackGroup: function() {
      window.location.href = '/group/' + this.group.id
    },

    redirectPendingUsers: function() {
      console.log('PUsers'),
      window.location.href = '/group/' + this.group.id + '/edit/pendingUsers'
    },

    redirectPendingRestaurants: function() {
      console.log('PRests')
      window.location.href = '/group/' + this.group.id + '/edit/pendingRestaurants'
    }  // redirectPendingRestaurants
  } // methods

}) // main brackets
