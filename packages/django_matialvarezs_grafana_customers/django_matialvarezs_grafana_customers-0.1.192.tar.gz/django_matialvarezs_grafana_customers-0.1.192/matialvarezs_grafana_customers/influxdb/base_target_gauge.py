def get_target_gauge(measurement, field, **options):
    alias = options.get("alias", "")
    refId = options.get("refId", None)
    return {
               "alias": alias,
               "groupBy": [],
               "measurement": measurement,
               "orderByTime": "ASC",
               "policy": "default",
               "refId": refId,
               "resultFormat": "time_series",
               "select": [
                   [
                       {
                           "params": [
                               field
                           ],
                           "type": "field"
                       },
                       {
                           "params": [],
                           "type": "last"
                       }
                   ]
               ],
               "tags": []
           }
