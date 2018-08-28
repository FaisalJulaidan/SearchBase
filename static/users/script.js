


$(document).ready(function () {

    console.log("Script Works");


// $(document).on('submit', '#userForm', function (e) {
//     e.preventDefault();
//     submitUserForm(this)
// })



});


function deleteUser(userID) {
    swal({
          title: "Are you sure?",
          text: "User will be removed completely from the system",
          icon: "warning",
          buttons: true,
          dangerMode: true,
        })
        .then((willDelete) => {
          if (willDelete) {

            $.ajax({
                url: '/admin/user/' + userID,
                type: "DELETE"
            }).done(function (res) {
                console.log(res);
                swal("Success!", "User has been deleted successfully", "success").then((value) => {
                  document.location.reload()
                });
            }).fail(function (res) {
                let resJson = JSON.parse(res.responseText);
                swal("Error!", resJson.msg, "error").then((value) => {
                  document.location.reload()
                });
            });

          } else {
            // When clicking the cancel button in the alert box
          }
        });

 }

function submitEditUserForm(form,userID, event) {
    console.log('EDIT USER.');
     $.ajax({
        url: '/admin/user/' + userID,
        type: "PUT",
        data: $('#userForm').serialize()
    }).done(function (res) {
        console.log(res);
        swal("Success!", "User has been updated successfully", "success").then((value) => {
          document.location.reload()
        });
    }).fail(function (res) {
        let resJson = JSON.parse(res.responseText);
        swal("Error!", resJson.msg, "error").then((value) => {
        });
    });
}

function submitNewUserForm(form, event) {
    console.log('NEW USER.');
    console.log();
    $.ajax({
        url: '/admin/user',
        type: "POST",
        data: $('#userForm').serialize()
    }).done(function (res) {
        console.log(res);
        swal("Success!", "User has been created successfully", "success").then((value) => {
          document.location.reload()
        });
    }).fail(function (res) {
        let resJson = JSON.parse(res.responseText);
        swal("Error!", resJson.msg, "error").then((value) => {
        });
    });
}

function fillUserForm(userID, edit=false){
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

    // Bind the appropriate handlers depends on edit value
    $(document).on('submit', '#userForm', function (e) {
    e.preventDefault();
    if (edit){submitEditUserForm(this,userid=userID, event=e)}
    else {submitNewUserForm(this, event=e)}
    })

}

// Once the modal is closed, unbind all onSubmit handlers from the userForm
$(document).on('hide.bs.modal', '#userModal', function (e) {
    console.log('Unbind submit event.');
    $(document).off('submit', '#userForm');
});

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