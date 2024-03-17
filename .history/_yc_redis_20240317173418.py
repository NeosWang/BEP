import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query


__host = "redis-18202.c233.eu-west-1-1.ec2.cloud.redislabs.com"
__port = "18202"
__password = "mxtpCloMZZTVrOorWZ8BVEEB3aCTngdi"

__myRedis = redis.Redis(host=__host, port=__port, password=__password)




class Redis_TTINT():
    def __init__(self) -> None:
  
   



    def __create_index(self, prefix="ttint"):
        try:
            # check to see if index exists
            __myRedis.ft(prefix).info()
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
            __myRedis.ft(prefix).create_index(fields=schema, definition=definition)

    def set_json(self, key, dct):
        __myRedis.json().set(f"ttint:{key}",Path.root_path,dct)

# r.flushall()



# snt1 = {
#         "lpcode": "LP00632689899995",
#         "altcode": "4008649775161679",
#         "productcode": "UNISZ",
#         "delivered": 1
#     }

# snt2 = {
#         "lpcode": "LP00633298063699",
#         "altcode": "4008649990492671",
#         "productcode": "UNISZ",
#         "delivered": 0
#     }



# r.json().set(f"ttint:SPIAC00001733564", Path.root_path(), snt1)
# r.json().set(f"ttint:SPIAC00001745627", Path.root_path(), snt2)


# def create_index(prefix="ttint"):
#     try:
#         # check to see if index exists
#         r.ft(prefix).info()
#         print("Index already exists!")
#     except:
#         # schema
#         schema = (
#             TextField("$.lpcode", as_name="lpcode"),
#             TextField("$.altcode", as_name="altcode"),
#             TagField("$.product", as_name="product"),
#             TagField("$.client", as_name="client"),
#             NumericField("$.delivered", as_name="delivered")
#             )

#         # index Definition
#         definition = IndexDefinition(
#             prefix=[prefix], 
#             index_type=IndexType.JSON
#             )

#         # create Index
#         r.ft(prefix).create_index(fields=schema, definition=definition)


# create_index()

# r.json().get("ttint:SPIAC00001745627")
# # r.ft().search("LP00633298063699")
# r.ft("ttint").search(
#     Query("@lpcode:*9999*")
# )

