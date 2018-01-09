import swal from 'sweetalert';

alert("TEST");
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

function testDel(){
  console.log("hei!"),
  swal({
    title: "Are you sure?"
    text: "Deleted groups cannot be recovered!"
    type: "warning",
    showCancekButton: true,
    confirmButtonClass: 'btn-danger',
    confirmButtonText: 'Yes, delete group',
    closeOnConfirm: false,
  },
  function(){
    swal("Deleted", "Your group was deleted!", "success");
  });
};
