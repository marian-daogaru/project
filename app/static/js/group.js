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
            if (this.group){
              if (this.group.id === -1){
                window.location.href = '/home'
            }}
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
      },
    } // methods
  }) // main brackets



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
        if (window.location.pathname.substring(0, 6) === '/group'){
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
      }
    } // methods

  }) // main brackets
