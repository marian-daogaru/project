var groupAPI = new Vue({
  el: "#groupAPI",
  delimiters: ['${', '}'],
  data: {
    group: null,
    emails: ''
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
          this.group = result.data,
          console.log(this.group)
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
      console.log(form)
    },  // addPeople

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
        swal("Left", "You left the group successfully!", "success");
        thisVue.leaveGroup()
      })
    },  //leaveGroupAlert

    leaveGroup: function() {
      console.log(this.parent),
      console.log(this.group.id),
      form = {
        groupID: this.group.id
      },
      console.log(form)
      this.$http.post(
        '/api/group/leave', form
      ).then(
        function(res) {
          response = res.data,
          console.log(response)
        },
        function(err) {
          console.error(err),
          console.log('error')
        }
      ).then(
        function() {
          console.log(response)
        })
    },

    deleteGroupAlert: function () {
      // THIS MUST BE FINISHED!!!
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
        swal("Deleted", "Your group was deleted!", "success");
        // window.location.replace({{"/user/"}} + groupID);
        // window.location.replace(Flask.url_for('user', {id: userID, groupIDDelete: groupID}));
      });
    } //deleteGroup
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
