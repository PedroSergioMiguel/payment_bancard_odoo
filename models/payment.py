# coding: utf-8

import os
import sys
import json
import random
import hashlib
import logging
import requests
import pprint
from decimal import Decimal
from requests.exceptions import HTTPError
from werkzeug import urls
from collections import namedtuple

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round

from odoo.addons.payment_bancard.controllers.main import BancardController


_logger = logging.getLogger(__name__)


class AcquirerBancard(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('bancard', 'Bancard')])
    bancard_publicKey = fields.Char('Clave Pública', required_if_provider='bancard', groups='base.group_user')
    bancard_privateKey = fields.Char('Clave Privada', required_if_provider='bancard', groups='base.group_user')


@api.model

def bancard_form_generate_values(self, values):
    base_url = self.get_base_url()

    marketplace_charge_id = random.randrange(500000, sys.maxsize >> 8)
    amount = Decimal(values['amount'])
    currency = 'PYG'
    description = '%s: %s' % (self.company_id.name, values['reference'])
    additional_data = ''
    approved_url = urls.url_join(base_url, BancardController._success_url)
    cancelled_url = urls.url_join(base_url, BancardController._cancel_url)
    private_key = self.bancard_privateKey
    public_key = self.bancard_publicKey

    bancard_token = "%s%s%s%s" % (private_key, marketplace_charge_id, amount, currency)

    bancard_body_request = dict(values)

    bancard_body_request.update({
        'public_key': public_key,
        'operation': {
            'token': hashlib.md5(bancard_token).hexdigest(),
                'shop_process_id': str(marketplace_charge_id),
                'currency': currency,
                'amount': amount,
                'additional_data': additional_data,
                'description': description,
                'return_url': approved_url,
                'cancel_url': cancelled_url
            }
        })


    bancard_response = __call_bancard_webservice(bancard_body_request, self._get_bancard_urls(environment)['bancard_form_url'])

    return bancard_response
    

def _get_bancard_urls(self, environment):
    """ Bancard URLS """
    if environment == 'prod':
        return {
            'bancard_form_url': 'https://vpos.infonet.com.py:8888/vpos/api/0.3/single_buy',
        }
    else:
        return {
            'bancard_form_url': 'https://vpos.infonet.com.py:8888/vpos/api/0.3/single_buy',
        }



def bancard_get_form_action_url(self):
    self.ensure_one()
    environment = 'prod' if self.state == 'enabled' else 'test'
    return self._get_bancard_urls(environment)['bancard_form_url']



def __call_webservice(params, wsurl):


    bancard_body_request = json.dumps(params) if type(params) is dict else (params if type(params) is str else str(params))
    headers = {"Content-Type": "application/json"}
    response = requests.post(wsurl, data=bancard_body_request, headers=headers)
    bancard_response = json.loads(response.content.decode("utf-8")) if response.content else dict()
    
    return bancard_response
