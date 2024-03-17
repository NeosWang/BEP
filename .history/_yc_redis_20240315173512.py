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




rs = r.ft("idx:SNT")
schema_SNT = (
    TextField("$.lpCode", as_name="lpCode"), 
    TextField("$.altCode", as_name="altCode"), 
    TextField("$.productCode", as_name="productCode"), 
    TextField("$.delivered", as_name="delivered")
)
rs.create_index(
    schema_SNT,
    definition=IndexDefinition(
        prefix=["SNT:"], index_type=IndexType.JSON
    )
)
snt = {
    "lpCode": "LP00632689899995",
    "altCode": "4008649775161679",
    "delivered": "0"
}
r.json().set("SNT:SPIAC00001733564", Path.root_path(), snt)



snt = {
    "lpCode": "LP00632689899995",
    "altCode": "4008649990492671",
    "delivered": "0"
}
r.json().set("SNT:SPIAC00001745627", Path.root_path(), snt)







r.ft("idx:SNT").search(   "32689899995")



rs.search(
    Query("Paul").return_field("$.city", as_field="city")
).docs

rs.search(
    Query("@delivered:1")
).docs


{
    "barcode":
}