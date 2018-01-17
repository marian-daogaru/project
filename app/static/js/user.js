
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
