//------------------------------------------------------------------------------
var createGroupApi = new Vue({
  el: "#createGroupAPI",
  delimiters: ['${','}'],
  data:{
    user: null,
    groupName: '',
    aboutGroup: '',
    errors: null,
    response: '',
  }, // data

  mounted() {
    this.loadUser()
  },  //mounted

  methods:
  {
    loadUser: function() {
      this.$http.get(
        '/api/createGroup'
      ).then(
        function(response) {
          this.user = response.data
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      )
    }, //loadUser

    createGroup: function() {
      form = {
        name: this.groupName,
        aboutGroup: this.aboutGroup
      }
      this.$http.post(
        '/api/createGroup', form
      ).then(
        function(response) {
          this.errors = response.data.errors,
          this.response = response.data
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(  // first then
        function(){
          if (this.response.created) {
            this.createdSuccessfully()
          }
        }
      )
    },  // createGroup

    createdSuccessfully: function() {
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Group Created succesfully",
        text: "You created the group successfully!",
        type: "success",
        closeOnConfirm: true,
        confirmButtonClass: 'btn-success',
        confirmButtonText: 'Go to new the group.'
      },
      function() {
        console.log('/group/' + thisVue.response.groupID),
        window.location.href = '/group/' + thisVue.response.groupID
      })
    }
  } // methods
}) // main brackets
