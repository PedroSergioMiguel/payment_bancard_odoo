odoo.define('payment_bancard.bancard_form', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Dialog = require("web.Dialog");

    var _t = core._t;
    var qweb = core.qweb;

    ajax.loadXML('/payment_bancard/static/src/xml/templates.xml', qweb)

    console.log(this);

    $(document).ready(function() {
        var $modal;

        $('#o_payment_form_pay').on('click', function(ev) {
            ev.preventDefault();
            // we retrieve the payment form
            var parent_form = ev.target.form;
            // then the checked radio
            var checked_radio = $('input[type="radio"]:checked', parent_form);
            // check if there's one checked radio
            if (checked_radio.length != 1) {
                return;
            }
            // if there's a checked radio, we retrieve the usefull data
            var acquirer_id = checked_radio.data('acquirerId');
            var provider = checked_radio.data('provider');
            var is_form_payment = checked_radio.data('form-payment') === "True";
            
            // now we check if the user has clicked on stripe radio button and wants to pay via the checkout form
            if (provider != "bancard" || is_form_payment !== true) {
                return;
            }

            var styles = {
                'input-background-color' : '#453454',
                'input-text-color': '#B22222',
                'input-border-color' : '#CCCCCC',
                'input-placeholder-color' : '#999999',
                'button-background-color' : '#5CB85C',
                'button-text-color' : '#FFFFFF',
                'button-border-color' : '#4CAE4C',
                'form-background-color' : '#999999',
                'form-border-color' : '#DDDDDD',
                'header-background-color' : '#F5F5F5',
                'header-text-color' : '#333333',
                'hr-border-color' : '#B22222'
            };

            var options = {
                styles: styles
            };

            var temp = 0;
            var loader = "<div class='bancard_payment_loder' style='display:none;'></div>";
            $('.o_payment_form').after(loader);

            if (temp == 0) {
                var amount = $('#payment-form').find('input[name="amount"]').val();
                temp = 1;

                $('.bancard_payment_loder').show();
                if (!$modal) {
                    ajax.jsonRpc("/bancard/modal", 'call', {}).then(function(data) {
                        $modal = $(data);
                        
                        $('#o_payment_form_pay').hide();
                        $('#o_payment_form_pay').after($modal);

                        $('#myModal').modal('show');
                        //Bancard.Cards.createForm('iframe-container', '8Q.1S*blA4WPuJwGd9fc', options);
                        // important part for create tx
                        //create_draft_transaction();
                    });
                }
                return false;
            }
        });

        
    });
});