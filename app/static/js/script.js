// import swal from 'sweetalert';  // don't actually need this!!!!

window.onload = function() {
    console.log("mamamia!");
};


// document.querySelector('.testDelete').onclick = function(){
//   console.log("hei!");
//   swal({
//     title: "Are you sure?"
//     text: "Deleted groups cannot be recovered!"
//     type: "warning",
//     showCancekButton: true,
//     confirmButtonClass: 'btn-danger',
//     confirmButtonText: 'Yes, delete group',
//     closeOnConfirm: false,
//   },
//   function(){
//     swal("Deleted", "Your group was deleted!", "success");
//   });
// };
//
function testDel(groupID, userID) {
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
    window.location.replace(Flask.url_for('user', {id: userID, groupID: groupID}));
  });
};
