# Copyright (c) 2020 kien@clare.ai.
# All Rights Reserved.

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json
import logging
import time

import requests

from wati_api import http
from wati_api import utils

LOG = logging.getLogger(__name__)


class Client(http.HTTPClient):
    """Client for the WATI API.
    :param endpoint: A user-supplied endpoint URL for the WATI service.
    :param token: A token get from: https://app.wati.io/register
    """

    def __init__(self, endpoint, token, **kwargs):
        """Initialize a new client for the WATI API."""
        super(Client, self).__init__(endpoint, **kwargs)
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def send_template(self, whatsapp_number, template_name,
                      template_parameters):
        """Send message templates"""
        url = utils.generate_url(
            '/api/v1/sendTemplateMessage/', whatsapp_number)
        payload = {
            "template_name": template_name,
            "broadcast_name": template_name + "_" + whatsapp_number,
            "parameters": json.dumps(template_parameters)
        }
        return self.post(url, body=payload, headers=self.headers).json()

    def get_template(self, whatsapp_number):
        """Get Messages by whatsapp number"""
        url = utils.generate_url(
            '/api/v1/getMessages/', whatsapp_number)
        return self.get(url, headers=self.headers).json()
