# TODO (snimu) create data structure that:
#   - registers each function by namespace/name
#   - checks duplicate namespace/names
#   - marks if they were used or not
#   - marks if the function's use was guaranteed
#   - includes counter for the number of uses of the function
#   - includes the function signature
#   Structure:
#       f"{namespace} + "/" + {name}"
#           : "has_test"
#           : "signature"
#           : "counter"
#   for each namespace/name
#   A function should be registered to unittest that is executed after
#   all other tests: it checks whether or not 
