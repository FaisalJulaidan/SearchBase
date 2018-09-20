


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
            document.location = "admin/assistant/manage"
            $.ajax({
                url: '/admin/user/' + userID,
                type: "DELETE"
            }).done(function (res) {
                console.log(res);
                swal("Success!", "User has been deleted successfully", "success").then((value) => {
                  document.location = "admin/assistant/manage"
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

 // ----- Users ----
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



 // ----- Roles ----


// Bind the appropriate handler for roles form submission
    $(document).on('submit', '#rolesForm', function (e) {
        e.preventDefault();
        submitRolesForm(this);
    });


function submitRolesForm(form) {
    console.log('Update USER.');
    data = [];

    // Iterate through each row and get checkboxes values
    $('table#rolesTable > tbody > tr').each(function (i, row) {
        $row = $(row);
        console.log( );
        data.push({
            ID: $row.attr('data-rowID'),
            EditChatbots: $row.find('input[name="editChatbots"]').is(":checked"),
            EditUsers: $row.find('input[name="editUsers"]').is(":checked"),
            DeleteUsers: $row.find('input[name="deleteUsers"]').is(":checked"),
            AccessBilling: $row.find('input[name="accessBilling"]').is(":checked"),
        })
    });

    console.log( data );

     $.ajax({
        url: '/admin/roles',
        type: "PUT",
        data: {data: JSON.stringify(data)}
    }).done(function (res) {
        console.log(res);
        swal("Success!", "Roles has been updated successfully", "success").then((value) => {
          document.location.reload()
        });
    }).fail(function (res) {
        let resJson = JSON.parse(res.responseText);
        swal("Error!", resJson.msg, "error").then((value) => {
             document.location.reload()
        });
    });
}






