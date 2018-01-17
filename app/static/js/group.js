var groupAPI = new Vue({
  el: "#groupAPI",
  delimiters: ['${', '}'],
  data: {
    group: null,
    emails: '',
    errors: null,
    confirmation: null,
    response: null,
  },

  mounted() {
    this.loadGroup()
  }, // mounted
  methods: {
    loadGroup: function() {
      this.$http.get(
        '/api' + window.location.pathname
      ).then(
        function(result) {
          this.group = result.data
        },
        function(err) {
          console.log(err),
          console.log('error')
        }).then( // first then
          function() {
            if (this.group.id === -1){
              window.location.href = '/home'
            }
          })  // second then
    },  // loadGroup

    editRedirect: function() {
      window.location.href = '/group/' + this.group.id + '/edit'
    },  // editRediect

    addPeople: function(){
      form = {
        emails: this.emails
      },
      console.log(form),
      this.$http.post(
        '/api/group/' + this.group.id, form
      ).then(
        function(response) {
          this.errors = response.data.errors,
          this.confirmation = response.data.added,
          this.emails = null,
          console.log(response)

        },
        function(err) {
          console.log(err),
          console.log('error')
        })
    },  // addPeople

    successfullyLeft: function(){
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Left",
        text: "You left the group successfully!",
        type: "success",
        closeOnConfirm: true,
        confirmButtonClass: 'btn-success',
        confirmButtonText: 'Go back to profile'
      },
      function() {
        console.log('/user/' + thisVue.response.id),
        window.location.href = '/user/' + thisVue.response.id
      })
    },

    leaveGroupAlert: function() {
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Are you sure you want to leave this group?",
        text: "You can come back later if you leave.",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: false,
        confirmButtonClass: 'btn-danger',
        confirmButtonText: 'Leave group',
      },
      function(){
        thisVue.leaveGroup(false)
      })
    },  //leaveGroupAlert

    leaveGroupAlertLastAdmin: function() {
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "You are the last admin!",
        text: "You are the last admin of this group. If you leave, the group will be deleted",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: false,
        confirmButtonClass: 'btn-danger',
        confirmButtonText: 'Leave group',
      },
      function(){
        thisVue.leaveGroup(true)
      })
    },  //finalAdmin

    leaveGroup: function(consentToLeave) {
      console.log(this.parent),
      console.log(this.group.id),
      form = {
        groupID: this.group.id,
        consent: consentToLeave
      },
      console.log(form)
      this.$http.post(
        '/api/group/leave', form
      ).then(
        function(res) {
          this.response = res.data
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(
        function() {
          if (this.response.lastAdmin){
            this.leaveGroupAlertLastAdmin()
          }
          if (this.response.left){
            this.successfullyLeft()
          }
        })
    },

    deleteGroupAlert: function () {
      var thisVue = this;  // otherwise in swal this is replaced by local inst
      swal({
        title: "Are you sure?",
        text: "Deleted groups cannot be recovered!",
        type: "warning",
        showCancelButton: true,
        closeOnConfirm: false,
        confirmButtonClass: 'btn-danger',
        confirmButtonText: 'Yes, delete group',
      },
      function(){
        thisVue.deleteGroup()
      })
    }, //deleteGroupAlert

    deleteGroup: function(){
      this.$http.delete(
        '/api/group/' + this.group.id + '/delete'
      ).then(
        function(response) {
          this.response = response.data,
          this.errors = response.data.errors,
          console.log(response)
        },
        function(err) {
          console.error(err),
          console.log('error')
        }).then(
          function(){
            if (this.response.deleted){
              this.successfullyLeft()
            }
          }
        )
    } // deleteGroup
  }  // methods
})  //groupAPI

  var createGroupApi = new Vue({
    el: "#createGroupAPI",
    delimiters: ['${','}'],
    data:{

    }, // data

    methods:
    {

    } // methods

  }) // main brackets

  // var editGroupAPI = new Vue({
  //   el: "#editGroupAPI",
  //   delimiters: ['${','}'],
  //   data:{
  //
  //   }, // data
  //
  //   methods:
  //   {
  //
  //   } // methods
  //
  // }) // main brackets
