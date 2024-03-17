import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
from backend._redis import myRedis






class Redis_TTINT():
    def __init__(self) -> None:
        # self.__create_index()
        pass
  
    def __create_index(self, prefix="ttint"):
        try:
            # check to see if index exists
            myRedis.ft(prefix).info()
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
            myRedis.ft(prefix).create_index(fields=schema, definition=definition)

    def set_json(self, key, obj):
        return myRedis.json().set(
            f"ttint:{key}",
            ".",
            obj
            )
        
    def get_json(self, key):
        return myRedis.json().get(
            name=f"ttint:{key}")
    
    
# myRedis.flushall()





# ttint = Redis_TTINT()

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

# ttint.set_json("SPIAC00001733564", snt1)

# ttint.set_json("SPIAC00001745627", snt2)

# ttint.get_json("SPIAC00001745621")


# r.json().get("ttint:SPIAC00001745627")
# # r.ft().search("LP00633298063699")
# r.ft("ttint").search(
#     Query("@lpcode:*9999*")
# )

