


$(document).ready(function () {

    console.log("Script Works");


$(document).on('submit', '#userForm', function (e) {
    e.preventDefault();
    submitUserForm(this)
})



});


function deleteUser(userID) {
    swal({
          title: "Are you sure?",
          text: "User will be removed completely form the system",
          icon: "warning",
          buttons: true,
          dangerMode: true,
        })
        .then((willDelete) => {
          if (willDelete) {

            $.post({
                url: '/admin/user/' + userID,
                type: "DELETE"
            }).done(function (res) {
                console.log(res);
                swal("Success!", "User has been deleted successfully", "success").then((value) => {
                  document.location.reload()
                });
            }).fail(function (res) {
                let resJson = JSON.parse(res.responseText);
                swal("Success!", resJson.msg, "error").then((value) => {
                  document.location.reload()
                });
            });

          } else {
            // When clicking the cancel button in the alert box
          }
        });

 }

function submitUserForm(form) {

    console.log(form.role.value)
}

function handleUserForm(userID=0, edit=false){
    let $form = $('form#userForm');
    let $row = $('#usersTable tbody tr[data-rowID="' + userID + '"]');
    $('#userModal').modal('show');

    if(edit){
         // fill current user
        $form.find('input[name="firstname"]').val($row.find('td[data-type="firstname"]').text());
        $form.find('input[name="surname"]').val($row.find('td[data-type="surname"]').text());
        $form.find('input[name="email"]').val($row.find('td[data-type="email"]').text());
        $form.find('select[name="role"]').val($row.find('td[data-type="role"]').text()).change();
    }


}



 // $.post({
 //        url: '/admin/user/' + userID,
 //        contentType: 'application/json',
 //        data: JSON.stringify({
 //            token: result.token,
 //            coupon: $(document.getElementById('promoCode')).val()
 //        }),
 //        success: (res) => {
 //            if (res.error) {
 //                alertError('Error', '<h2> ' + res.error)
 //            } else {
 //                example.classList.add('submitted');
 //
 //
 //            }
 //        }
 //    });