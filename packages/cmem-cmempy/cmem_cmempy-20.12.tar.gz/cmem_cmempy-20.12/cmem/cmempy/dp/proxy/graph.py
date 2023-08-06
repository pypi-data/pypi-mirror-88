"""API for managing graphs in DP."""

import os
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

from cmem.cmempy import config
from cmem.cmempy.api import request


def get_graph_uri_pattern():
    """Get endpoint URI pattern for a graph (graph store protocol)."""
    return config.get_dp_api_endpoint() + "/proxy/{}/graph?graph={}"


def _get_graph_uri(endpoint_id, graph):
    escaped_graph = quote(graph)
    return get_graph_uri_pattern().format(endpoint_id, escaped_graph)


def get(
        graph,
        endpoint_id="default",
        owl_imports_resolution=True,
        accept="application/n-triples"):
    """GET graph."""
    headers = {"Accept": accept}
    uri = _get_graph_uri(endpoint_id, graph) \
        + "&owlImportsResolution=" \
        + str(owl_imports_resolution).lower()
    return request(
        uri,
        method="GET",
        headers=headers
    )


def delete(
        graph,
        endpoint_id="default"):
    """DELETE graph."""
    uri = _get_graph_uri(endpoint_id, graph)
    return request(
        uri,
        method="DELETE"
    )


def post(
        graph,
        file,
        endpoint_id="default",
        replace=False):
    """Upload graph."""
    uri = _get_graph_uri(endpoint_id, graph) \
        + "&replace=" \
        + str(replace).lower()
    return request(
        uri,
        method="POST",
        files={'file': (os.path.basename(file), open(file, 'rb'))}
    )


def put(
        graph,
        rdf_data,
        rdf_serialization,
        endpoint_id="default"):
    """PUT graph."""
    headers = {"Content-Type": rdf_serialization}
    uri = _get_graph_uri(endpoint_id, graph)
    return request(
        uri,
        method="PUT",
        data=rdf_data,
        headers=headers
    )
