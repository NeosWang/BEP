import redis

__host = "redis-18202.c233.eu-west-1-1.ec2.cloud.redislabs.com"
__port = "18202"
__password = "mxtpCloMZZTVrOorWZ8BVEEB3aCTngdi"

myRedis = redis.Redis(host=__host, port=__port, password=__password)