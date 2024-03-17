import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

host = "redis-18202.c233.eu-west-1-1.ec2.cloud.redislabs.com"
port = "18202"
password = "mxtpCloMZZTVrOorWZ8BVEEB3aCTngdi"

r = redis.Redis(host=host, port=port, password=password)

r.flushall()

user1 = {
    "name": "Paul John",
    "email": "paul.john@example.com",
    "age": 42,
    "city": "London"
}
user2 = {
    "name": "Eden Zamir",
    "email": "eden.zamir@example.com",
    "age": 29,
    "city": "Tel Aviv"
}
user3 = {
    "name": "Paul Zamir",
    "email": "paul.zamir@example.com",
    "age": 35,
    "city": "Tel Aviv"
}

schema = (
    TextField("$.name", as_name="name"), 
    TagField("$.city", as_name="city"), 
    NumericField("$.age", as_name="age")
)

rs = r.ft("idx:users")
rs.create_index(
    schema,
    definition=IndexDefinition(
        prefix=["user:"], index_type=IndexType.JSON
    )
)

r.json().set("user:1", Path.root_path(), user1)
r.json().set("user:2", Path.root_path(), user2)
r.json().set("user:3", Path.root_path(), user3)


user3 = {
    "name": "YC",
    "age": 39,
    "city": "Rotterdam"
}
r.json().set("user:3", Path.root_path(), user3)

rs.search(
    Query("Paul").return_field("$.city", as_field="city")
).docs

rs.search(
    Query("Paul @age:[30 40]")
).docs


