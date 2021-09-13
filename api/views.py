import datetime
from urllib.parse import urlparse

import redis
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


@api_view(['POST'])
def visited_links(request, *args, **kwargs):
    # try:
    #     item = json.loads(request.body)
    # except JSONDecodeError as e:
    #     response = {'status': 'bad json'}
    #     return Response(response, 400)

    links_list = request.data.getlist('links')

    if not links_list and not isinstance(links_list, list):
        response = {'status': 'fail'}
        return Response(response, 400)

    for link in links_list:
        domain = urlparse(link)
        domain = domain.netloc or domain.path
        create_date = datetime.datetime.now().timestamp()
        redis_instance.set(domain, create_date)
    response = {
        'status': 'оk'
    }
    return Response(response, 201)


@api_view(['GET'])
def visited_domains(request, *args, **kwargs):
    now_date = datetime.datetime.now().timestamp()
    from_date = request.GET.get('from', 0)
    to_date = request.GET.get('to', now_date)
    try:
        from_date = float(from_date)
        to_date = float(to_date)
    except ValueError as e:
        response = {'status': 'bad GET parameter'}
        return Response(response, 400)

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
