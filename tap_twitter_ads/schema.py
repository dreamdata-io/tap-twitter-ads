import os
import json
import singer
from singer import metadata
from .streams import flatten_streams


LOGGER = singer.get_logger()

GRANULARITIES = ["HOUR", "DAY", "TOTAL"]

ENTITY_TYPES = [
    "ACCOUNT",
    "CAMPAIGN",
    "FUNDING_INSTRUMENT",
    "LINE_ITEM",
    "MEDIA_CREATIVE",
    "ORGANIC_TWEET",
    "PROMOTED_TWEET",
    "PROMOTED_ACCOUNT",
]

SEGMENTS = [
    "NO_SEGMENT",
    "AGE",
    "AMPLIFY_MARKETPLACE_PREROLL_VIDEOS",
    "AMPLIFY_PUBLISHER_TWEETS",
    "APP_STORE_CATEGORY",
    "AUDIENCES",
    "CONVERSATIONS",
    "CONVERSION_TAGS",
    "DEVICES",
    "EVENTS",
    "GENDER",
    "INTERESTS",
    "KEYWORDS",
    "LANGUAGES",
    "LOCATIONS",
    "METROS",
    "PLATFORM_VERSIONS",
    "PLATFORMS",
    "POSTAL_CODES",
    "REGIONS",
    "SIMILAR_TO_FOLLOWERS_OF_USER",
    "SWIPEABLE_MEDIA",
    "TV_ADS",
    "TV_SHOWS",
]


# Reference:
# https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#Metadata


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_shared_schema_refs():
    shared_schemas_path = get_abs_path("schemas/shared")

    shared_file_names = [
        f
        for f in os.listdir(shared_schemas_path)
        if os.path.isfile(os.path.join(shared_schemas_path, f))
    ]

    shared_schema_refs = {}
    for shared_file in shared_file_names:
        with open(os.path.join(shared_schemas_path, shared_file)) as data_file:
            shared_schema_refs[shared_file] = json.load(data_file)

    return shared_schema_refs


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def nested_ref_replace(schema, obj, refs, path=None):
    if not path:
        path = []

    for k, v in obj.items():
        if isinstance(v, dict):
            nested_ref_replace(schema, v, refs, path=path + [k])
        elif k == "$ref":
            nested_set(schema, path, refs[v])


def resolve_schema_references(schema, refs):
    if "__sdc_dimensions_hash_key" in schema["properties"]:
        nested_ref_replace(schema, schema, refs)
        nested_ref_replace(schema, schema, refs)

