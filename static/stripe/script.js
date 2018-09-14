 $(document).ready(function () {

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
    var card = elements.create('card', {style: style});

    // Add an instance of the card Element into the `card-element` <div>.
    var el = document.getElementById('card-element');
    card.mount(el);
    console.log(card);

    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function(event) {
      var displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });


    function openSubForm(planId, price){
        $('#subModal').modal('show');
        var $form = $('form#subForm');

        $form.find('#payBtn').html('Pay £' + price);
        $(document).on('submit', 'form#subForm', function (e) {
            e.preventDefault();
            pay(planID=planId)
        })

    }


    function pay(planID) {
        var token = stripeTokenHandler();
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
                    });

            }).fail(function (res) {
                console.log("Error");
                console.log(res);
                swal("Ooops!", res.msg, "error");
            });
        } else {

        }

    }


    function stripeTokenHandler() {
        stripe.createToken(card).then(function (result) {
            // console.log(">>>>");
            // console.log(result);
            // console.log(">>>>");
            if (result.error) {
                // Inform the user if there was an error.
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
                 swal("Ooops!",result.error.message, "error");
                return null;
            } else {
                // Send the token to your server.
                console.log("token generated");
                return result.token;
            }
        });
    }

 });

