from pkgutil import extend_path
import requests
import os
import json
from hestia_earth.schema import SchemaType

__path__ = extend_path(__path__, __name__)

s3_client = None


# improves speed for connecting on subsequent calls
# TODO: find a better way to do this, like profiling?
def get_s3_client():
    global s3_client
    import boto3
    s3_client = boto3.client('s3') if s3_client is None else s3_client
    return s3_client


def non_empty_value(value): return value != '' and value is not None and value != []


def join_args(values): return '&'.join(list(filter(non_empty_value, values))).strip()


def api_url(): return os.environ.get('API_URL', 'https://api.hestia.earth')


def search_url(): return os.environ.get('SEARCH_URL', 'https://search.hestia.earth')


def request_url(base_url: str, **kwargs):
    args = list(map(lambda key: '='.join([key, str(kwargs.get(key))]) if kwargs.get(key) else None, kwargs.keys()))
    return f"{base_url}?{join_args(args)}"


def find_related(node_type: SchemaType, id: str, related_type: SchemaType, limit=100, offset=0, relationship=None):
    try:
        url = request_url(f"{api_url()}/{node_type.value.lower()}s/{id}/{related_type.value.lower()}s",
                          limit=limit, offset=offset, relationship=relationship)
        return requests.get(url).json()
    except requests.exceptions.RequestException:
        return None


def load_from_bucket(bucket: str, key: str):
    from botocore.exceptions import ClientError
    try:
        return json.loads(get_s3_client().get_object(Bucket=bucket, Key=key)['Body'].read())
    except ClientError:
        return None


def download_hestia(node_id: str, node_type=SchemaType.TERM, mode=''):
    # try to download file from s3 first, if fail use api
    try:
        return load_from_bucket(os.getenv('AWS_BUCKET'), f"{node_type.value}/{node_id}.jsonld")
    except ImportError:
        url = request_url(f"{api_url()}/download", type=node_type.value, id=node_id, mode=mode)
        return requests.get(url).json()
    except requests.exceptions.RequestException:
        return None


def find_node(node_type: SchemaType, args: dict, limit=10):
    headers = {'Content-Type': 'application/json'}
    query_args = list(map(lambda key: {'match': {key: args.get(key)}}, args.keys()))
    must = [{'match': {'@type': node_type.value}}]
    must.extend(query_args)
    hits = requests.post(search_url(), json.dumps({
        'query': {'bool': {'must': must}},
        'limit': limit,
        '_source': {'includes': ['name', '@id']}
    }), headers=headers).json()['hits']['hits']
    return list(map(lambda res: res.get('_source'), hits))


def find_node_exact(node_type: SchemaType, args: dict):
    headers = {'Content-Type': 'application/json'}
    query_args = list(map(lambda key: {'match': {key: args.get(key)}}, args.keys()))
    must = [{'match': {'@type': node_type.value}}]
    must.extend(query_args)
    hits = requests.post(search_url(), json.dumps({
        'query': {'bool': {'must': must}},
        'limit': 2,
        '_source': {'includes': ['name', '@id']}
    }), headers=headers).json()['hits']['hits']
    # do not return a duplicate
    return hits[0].get('_source') if len(hits) == 1 else None
