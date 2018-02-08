var editUserAPI = new Vue({
  el: "#editUserApi",
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
