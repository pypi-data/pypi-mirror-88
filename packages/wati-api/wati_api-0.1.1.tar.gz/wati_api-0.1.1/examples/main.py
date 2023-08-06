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

import os
import json
import hashlib

from wati_api import client

if __name__ == '__main__':
    try:
        endpoint = os.environ['WATI_API_ENDPOINT']
        token = os.environ['WATI_API_TOKEN']
    except KeyError as e:
        print('Missing environment variables! %s' % str(e))
        raise e
    wa_client = client.Client(endpoint, token)
    print(wa_client.get_template("85253332683"))
    template_parameters = [
        {'name': 'name', 'value': 'Ken'},
        {'name': 'amount', 'value': '100'},
        {'name': 'partnername', 'value': 'WATI.io'},
        {'name': 'paymentlink', 'value': 'https://app.wati.io/payment'}
    ]
    message = wa_client.send_template(
        whatsapp_number="85253332683",
        template_name="payment_reminder",
        template_parameters=template_parameters
    )
    print(message)
