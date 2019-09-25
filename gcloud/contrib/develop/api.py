# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import logging

try:
    import ujson as json
except ImportError:
    import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from gcloud.conf import settings
from gcloud.utils.handlers import handle_api_error

logger = logging.getLogger('root')
get_client_by_user = settings.ESB_GET_CLIENT_BY_USER


@require_GET
def esb_get_systems(request):
    client = get_client_by_user(request.user.username)
    esb_data = client.esb.get_systems()
    if not esb_data['result']:
        message = handle_api_error(system='esb',
                                   api_name='get_systems',
                                   params={},
                                   result=esb_data)
        return JsonResponse({'result': False, 'message': message})
    result = {
        'result': True,
        'data': esb_data['data']
    }
    return JsonResponse(result)


@require_GET
def esb_get_components(request):
    client = get_client_by_user(request.user.username)
    system_names = json.loads(request.GET.get('system_names', '[]'))
    esb_data = client.esb.get_components({'system_names': system_names})
    if not esb_data['result']:
        message = handle_api_error(system='esb',
                                   api_name='get_components',
                                   params={},
                                   result=esb_data)
        return JsonResponse({'result': False, 'message': message})
    result = {
        'result': True,
        'data': esb_data['data']
    }
    return JsonResponse(result)
