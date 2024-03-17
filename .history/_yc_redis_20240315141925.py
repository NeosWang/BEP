import redis


host = "redis-18202.c233.eu-west-1-1.ec2.cloud.redislabs.com"
port = "18202"
password = "mxtpCloMZZTVrOorWZ8BVEEB3aCTngdi"

r = redis.Redis(host=host, port=port, password=password)

print(r.set('foo', 'bar'))
r.get('foo')
