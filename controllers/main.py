# -*- coding: utf-8 -*-
import logging
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class BancardController(http.Controller):
    _success_url = '/payment/bancard/success'
    _cancel_url = '/payment/bancard/cancel'

    @http.route(['/payment/bancard/success', '/payment/bancard/cancel'], type='http', auth='public')
    def bancard_success(self, **kwargs):
        request.env['payment.transaction'].sudo().form_feedback(kwargs, 'bancard')
        return werkzeug.utils.redirect('/payment/process')


 