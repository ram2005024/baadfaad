from django_redis import get_redis_connection

redis=get_redis_connection("default")
redis.connection_pool.connection_kwargs["decode_responses"]=True
