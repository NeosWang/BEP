import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query,Filter

host = "redis-18202.c233.eu-west-1-1.ec2.cloud.redislabs.com"
port = "18202"
password = "mxtpCloMZZTVrOorWZ8BVEEB3aCTngdi"

r = redis.Redis(host=host, port=port, password=password)


r.flushall()



snt1 = {
        "lpcode": "LP00632689899995",
        "altcode": "4008649775161679",
        "productcode": "UNISZ",
        "delivered": 1
    }

snt2 = {
        "lpcode": "LP00633298063699",
        "altcode": "4008649990492671",
        "productcode": "UNISZ",
        "delivered": 0
    }



r.json().set(f"ttint:SPIAC00001733564", Path.root_path(), snt1)
r.json().set(f"ttint:SPIAC00001745627", Path.root_path(), snt2)


def create_index(prefix="ttint"):
    try:
        # check to see if index exists
        r.ft(prefix).info()
        print("Index already exists!")
    except:
        # schema
        schema = (
            TextField("$.lpcode", as_name="lpcode"),
            TextField("$.altcode", as_name="altcode"),
            TagField("$.product", as_name="product"),
            TagField("$.client", as_name="client"),
            NumericField("$.delivered", as_name="delivered")
            )

        # index Definition
        definition = IndexDefinition(
            prefix=[prefix], 
            index_type=IndexType.JSON
            )

        # create Index
        r.ft(prefix).create_index(fields=schema, definition=definition)


create_index()

r.json().get("tting:SPIAC00001745627")
# r.ft().search("LP00633298063699")
r.ft().search(
    Query("@lpcode:*9999*")
)


r.ft("SNT").get("SPIAC00001745627").docs



res = r.ft("TEM").search(
    Query("LP0*")
    
    ).docs
res
# res = r.ft().search(Query("UNISZ*").add_filter(NumericFilter("delivered",0, 0))).docs



# https://stackoverflow.com/questions/77398925/cannot-create-vector-index-in-redis




r.json().get("SNT:SPIAC00001745627")

r.keys()

for key in r.scan_iter("*SPIAC*"):
    print(key)




rs.search("4008649775161679")



rs.search(
    Query("Paul").return_field("$.city", as_field="city")
).docs

rs.search(
    Query("@delivered:1")
).docs


{
    "barcode":
}