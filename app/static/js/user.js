var userAPI = new Vue({
  el: "#userAPI",
  delimiters: ['${', '}'],
  data: {
    userLocal: null,
    user: null
  },

  mounted() {
    this.loadID()
  },

  methods: {
    loadID: function() {
    this.$http.get(
      '/api/home/id'
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
      if (this.userLocal && window.location.pathname.substring(0, 5) === '/user') {
        this.loadUser()
      }})
    },  // loadID

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
      ).then(
        function() {
          if (this.user.accessDenied){
            window.location.href = '/accessDenied'
          }
        }
      )
    },  // loadUser

    redirectEdit: function() {
      window.location.href = '/edit'
    },  // redirectEdit

    redirectCreateGroup: function() {
      window.location.href = '/createGroup'
    }  // redirectCreateGroup
  },
})


var editUserAPI = new Vue({
  el: "#editUserAPI",
  delimiters: ['${','}'],
  data:{
    user: null,
    nickname: '',
    aboutMe: '',
    password: '',
    confpwd: '',
    avatar: '',
    errors: ''

  }, // data

  mounted() {
    this.loadUser()
  },

  methods:
  {
    sendUpdate: function() {
      form = {
        nickname: this.nickname,
        aboutMe: this.aboutMe,
        password: this.password,
        confpwd: this.confpwd,
        avatar: this.avatar
      },
      console.log(form),
      this.$http.post(
        '/api/edit', form
      ).then(
        function(result) {
          this.user = result.data,
          this.errors = result.data.errors
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(  // first then
        function() {
          if (this.user.id !== -1){
            window.location.href = '/user/' + this.user.id
        }}
      )  // second then
    }, // sendUpdate

    loadUser: function() {
      this.$http.get(
        '/api/edit'
      ).then(
        function(result) {
          this.user = result.data
        },
        function(err) {
          console.log(err),
          console.log('error')
        }
      ).then(  // first then
        function() {
        this.nickname = this.user.nickname,
        this.aboutMe = this.user.aboutMe
      })  //second then
    }, // getUser

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

  } // methods
}) // main brackets


// -----------------------------------------------------------------------------
// PENDING RESTAURANT
// -----------------------------------------------------------------------------
var pendingUserAPI = new Vue({
  el: "#pendingUserAPI",
  delimiters: ['${','}'],
  data:{
    users: '',
    checkedUsers: [],
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
          this.users = response.data.users,
          this.groupID = response.data.groupID
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(
        function() {
          if (this.users.accessDenied) {
            window.location.href = '/accessDenied'
          }
        }
      )
    },  // loadPending

    addChecked: function() {
      if (this.checkedUsers.length > 0) {
        this.$http.put(
          '/api/group/' + this.groupID + '/edit/pendingUsers/' + this.checkedUsers
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
        this.errors = ['Please select at least one user to be added.']
      }
    },  // addChecked

    removeChecked: function() {
      if (this.checkedUsers.length > 0) {
        this.$http.delete(
          '/api/group/' + this.groupID + '/edit/pendingUsers/' + this.checkedUsers
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
        this.errors = ['Please select at least one user to be added.']
      }
    },  // removeChecked

    redirectGroup: function() {
      window.location.href = '/group/' + this.groupID
    }
  }  // methods
})
