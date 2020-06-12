# streams.py
# streams: API URL endpoints to be called
# properties:
#   <root node>: Plural stream name for the endpoint
#   path: API endpoint relative path, when added to the base URL, creates the full path,
#       default = stream_name
#   key_properties: Primary key fields for identifying an endpoint record.
#   replication_method: INCREMENTAL or FULL_TABLE
#   replication_keys: bookmark_field(s), typically a date-time, used for filtering the results
#        and setting the state
#   params: Query, sort, and other endpoint specific parameters; default = {}
#   data_key: JSON element containing the results list for the endpoint
#   bookmark_query_field: From date-time field used for filtering the query
#   bookmark_type: Data type for bookmark, integer or datetime

# pylint: disable=line-too-long
STREAMS = {
    # Reference: https://developer.twitter.com/en/docs/ads/campaign-management/api-reference/accounts#accounts
    "accounts": {
        "path": "accounts",
        "data_key": "data",
        "key_properties": ["id"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "params": {
            "account_ids": "{account_ids}",
            "sort_by": ["updated_at-desc"],
            "with_deleted": "{with_deleted}",
            "count": 1000,
            "cursor": None,
        },
    },
    # Reference: https://developer.twitter.com/en/docs/ads/campaign-management/api-reference/campaigns#campaigns
    "campaigns": {
        "path": "accounts/{account_id}/campaigns",
        "data_key": "data",
        "key_properties": ["id"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "params": {
            "sort_by": ["updated_at-desc"],
            "with_deleted": "{with_deleted}",
            "count": 1000,
            "cursor": None,
        },
    },
}
# pylint: enable=line-too-long

# De-nest children nodes for Discovery mode
def flatten_streams():
    flat_streams = {}
    # Loop through parents
    for stream_name, endpoint_config in STREAMS.items():
        flat_streams[stream_name] = endpoint_config
        # Loop through children
        children = endpoint_config.get('children')
        if children:
            for child_stream_name, child_endpoint_config in children.items():
                flat_streams[child_stream_name] = child_endpoint_config
                flat_streams[child_stream_name]['parent_stream'] = stream_name
    return flat_streams
