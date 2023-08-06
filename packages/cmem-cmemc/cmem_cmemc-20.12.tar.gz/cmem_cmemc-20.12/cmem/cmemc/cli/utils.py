"""Utility functions for CLI interface."""

import os
import re
import unicodedata

from cmem.cmempy.dp import proxy  # noqa: I100


def read_rdf_graph_files(directory_path):
    """Read all files from directory_path and output as tuples.

    The tuple format is (filepath, graph_name),
    for example ("/tmp/rdf.nt", "http://example.com")
    """
    rdf_graphs = []
    for root, _, files in os.walk(directory_path):
        for _file in files:
            full_file_path = os.path.join(root, _file)
            graph_file_name = _file + ".graph"
            full_graph_file_name_path = os.path.join(
                root,
                graph_file_name
            )
            if(not _file.endswith(".graph")
               and os.path.exists(full_graph_file_name_path)):
                graph_name = read_file_to_string(
                    full_graph_file_name_path
                ).strip()
                rdf_graphs.append(
                    (full_file_path, graph_name)
                )
    return rdf_graphs


def read_ttl_files(directory_path):
    """Read all files from directory_path.

    Filter the files which ends with .ttl
    Returns list of tuples (full_path_to_file, filename)
    """
    ttl_files = []
    for root, _, files in os.walk(directory_path):
        for _file in files:
            full_file_path = os.path.join(root, _file)
            if _file.endswith(".ttl"):
                ttl_files.append(
                    (full_file_path, _file)
                )
    return ttl_files


def read_file_to_string(file_path):
    """Read file to string."""
    with open(file_path, "rb") as _file:
        return _file.read().decode("utf-8")


def get_graphs(writeable=True, readonly=True):
    """Retrieve list of accessible graphs from DP endpoint.

    readonly=True|writeable=True outputs all graphs
    readonly=False|writeable=True outputs only writeable graphs
    readonly=True|writeable=False outputs graphs without write access
    (but read access)
    """
    all_graphs = proxy.get()['graphs']
    filtered_graphs = []
    for graph in all_graphs:
        if graph['writeable'] and writeable:
            filtered_graphs.append(graph)
        if not graph['writeable'] and readonly:
            filtered_graphs.append(graph)
    return filtered_graphs


def convert_uri_to_filename(value, allow_unicode=False):
    """Convert URI to unix friendly filename.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert / to underscore. Convert to lowercase.
    Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value)\
            .encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'\.', '_', value.lower())
    value = re.sub(r'/', '_', value.lower())
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
