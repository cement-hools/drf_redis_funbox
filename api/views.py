import datetime
import json
from json import JSONDecodeError
from urllib.parse import urlparse

import redis
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


@api_view(['GET', 'POST'])
def visited_links(request, *args, **kwargs):
    now_date = datetime.datetime.now().timestamp()
    from_date = request.GET.get('from', 0)
    to_date = request.GET.get('to', now_date)
    from_date = float(from_date)
    to_date = float(to_date)
    if request.method == 'GET':
        domains_list = []
        for key in redis_instance.keys('*'):
            redis_item_value = float(redis_instance.get(key))
            if from_date <= redis_item_value <= to_date:
                domains_list.append(key)
        response = {
            'domains': domains_list,
            'status': 'ok'
        }
        return Response(response, status=200)

    elif request.method == 'POST':
        try:
            item = json.loads(request.body)
        except JSONDecodeError as e:
            response = {'bad json': request.body}
            return Response(response, 400)

        links_list = item.get('links')
        if not links_list and not isinstance(links_list, list):
            response = {'status': 'fail'}
            return Response(response, 400)

        for link in links_list:
            domain = urlparse(link)
            domain = domain.netloc or domain.path
            create_date = now_date
            redis_instance.set(domain, create_date)
        response = {
            'status': 'оk'
        }
        return Response(response, 201)
