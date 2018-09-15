
// Create a Stripe client.
var stripe = Stripe('pk_test_e4Tq89P7ma1K8dAjdjQbGHmR');

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    lineHeight: '18px',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style});

// Add an instance of the card Element into the `card-element` <div>.
// var el = document.getElementById('card-element');
// console.log(card);

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});


function warn() {
    subID = sessionStorage.getItem('subID');
    if (subID !== 'null' || subID !== '' || subID !== undefined || subID !== null) {
        swal({
            title: "Are you sure?",
            text: "You will lose your active subscription.",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                return true;
            } else {
                return false;
         }
        });
    }
    return true;
}

function openSubForm(planId, price){

    subID = sessionStorage.getItem('subID');
    if (subID !== 'null' || subID !== '' || subID !== undefined || subID !== null) {
        
        swal({
            title: "Are you sure?",
            text: "You will lose your active subscription.",
            icon: "warning",
            buttons: true,
            dangerMode: true

        }).then((willDelete) => {
            if (willDelete) {

                $('#subModal').modal('show');
                var $form = $('form#subForm');
                $form.find('#payBtn').html('Pay £' + price);
                card.mount('#card-element');
                $(document).on('submit', 'form#subForm', function (e) {
                    e.preventDefault();
                    stripeTokenHandler(planId)
                })

            } else {
                document.location.href = '/admin/pricing'
            }
        });
    }
}




 function stripeTokenHandler(planID) {
        card.mount('#card-element');
        stripe.createToken(card).then(function (result) {
        if (result.error) {
            // Inform the user if there was an error.
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
             swal("Ooops!",result.error.message, "error");
            pay(planID, null)
        } else {
            // Send the token to your server.
            console.log("token generated");
            pay(planID, result.token)
            // return result.token;
        }
    });
}

function pay(planID, token) {
    // var token = stripeTokenHandler();
    console.log(token);
    if(token){
        $.ajax({
        url: '/admin/subscribe/' + planID,
        type: "POST",
        contentType: 'application/json', //this is important
        data: JSON.stringify({
            "token": token ,
            "coupon": $(document.getElementById('promo-code')).val()
        })

        }).done(function (res) {

        console.log("Successful Payment");
        swal({
                  title: "Successful Payment",
                  text: res.msg,
                  icon: "success"
        }).then((value) => {
          document.location.reload()
        });

        }).fail(function (res) {
            let resJson = JSON.parse(res.responseText);
            swal("Ooops!", resJson.msg, "error");
        });
    } else {

    }

}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}