"""graph commands for cmem command line interface."""

import hashlib
import json
import os
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib

from six.moves.urllib.parse import quote

import click

from jinja2 import Template

from cmem.cmemc.cli import completion
from cmem.cmemc.cli.utils import (
    convert_uri_to_filename,
    get_graphs,
    read_rdf_graph_files
)
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.dp.authorization import refresh
from cmem.cmempy.dp.proxy import graph as graph_api
from cmem.cmempy.dp.proxy.sparql import get as sparql_api


def count_graph(graph_iri):
    """Count triples in a graph and return integer."""
    query = "SELECT (COUNT(*) as ?triples)" +\
            " FROM <" + graph_iri + ">" +\
            " WHERE { ?s ?p ?o }"
    result = json.loads(sparql_api(query, owl_imports_resolution=False))
    count = result["results"]["bindings"][0]["triples"]["value"]
    return int(count)


def _get_graph_to_file(
        graph_iri, file_path,
        app,
        numbers=None,
        overwrite=True):
    """Request a single graph to a single file.

    numbers is a tupel of current and count (for output only).
    """
    if os.path.exists(file_path):
        if overwrite is True:
            app.echo_warning(
                "Output file {} does exist: will overwrite it."
                .format(file_path)
            )
        else:
            app.echo_warning(
                "Output file {} does exist: will append to it."
                .format(file_path)
            )
    if numbers is not None:
        running_number, count = numbers
        if running_number is not None and count is not None:
            app.echo_info(
                "Export graph {}/{}: {} to {} ... "
                .format(running_number, count, graph_iri, file_path),
                nl=False
            )
    # create and write the .ttl content file
    if overwrite is True:
        triple_file = click.open_file(file_path, "wb")
    else:
        triple_file = click.open_file(file_path, "ab")
    # TODO: use a streaming approach here
    data = graph_api.get(graph_iri).content
    triple_file.write(data)
    if numbers is not None:
        app.echo_success("done")


def _get_export_names(app, iris, template):
    """Get a dictionary of generated file names based on a template.

    Args:
        app: the context click application
        iris: list of graph iris
        template (str): the template string to use

    Returns:
        a dictionary with IRIs as keys and filenames as values

    Raises:
        ValueError in case the template string produces a naming clash,
            means two IRIs result in the same filename
    """
    template_data = app.get_template_data()
    _names = {}
    for iri in iris:
        template_data.update(
            hash=hashlib.sha256(iri.encode("utf-8")).hexdigest(),
            iriname=convert_uri_to_filename(iri)
        )
        _name_created = Template(template).render(template_data) + ".ttl"
        _names[iri] = _name_created
    if len(_names.values()) != len(set(_names.values())):
        raise ValueError(
            "The given template string produces a naming clash. "
            "Please use a different template to produce unique names."
        )
    return _names


@click.command(name="list")
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON."
)
@click.option(
    "--filter", "filter_",
    type=click.Choice(
        ["readonly", "writeable"],
        case_sensitive=True
    ),
    help="Filter list based on access conditions."
)
@click.pass_obj
def list_command(app, raw, filter_):
    """List accessible graphs."""
    if filter_ == "writeable":
        graphs = get_graphs(writeable=True, readonly=False)
    elif filter_ == "readonly":
        graphs = get_graphs(writeable=False, readonly=True)
    else:
        graphs = get_graphs(writeable=True, readonly=True)

    if raw:
        app.echo_result(graphs)
    else:
        for graph_desc in graphs:
            app.echo_result(graph_desc["iri"])


# pylint: disable=too-many-arguments
@click.command(name="export")
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Export all (readable) graphs"
)
@click.option(
    "--output-dir",
    type=click.Path(
        writable=True,
        file_okay=False
    ),
    help="Export to this directory"
)
@click.option(
    "--output-file",
    type=click.Path(
        writable=True,
        allow_dash=True,
        dir_okay=False
    ),
    default="-",
    show_default=True,
    autocompletion=completion.triple_files,
    help="Export to this file"
)
@click.option(
    "--filename-template", "-t", "template",
    default="{{hash}}",
    show_default=True,
    type=click.STRING,
    help="Template for the export file name(s). "
         "Used together with --output-dir. "
         "Possible placeholders are (Jinja2): "
         "{{hash}} - sha256 hash of the graph IRI, "
         "{{iriname}} - graph IRI converted to filename, "
         "{{connection}} - from the --connection option and "
         "{{date}} - the current date as YYYY-MM-DD. "
         "The file suffix will be appended. "
         "Needed directories will be created."
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.graph_uris
)
@click.pass_obj
def export_command(app, all_, iris, output_dir, output_file, template):
    """Export graph(s) as NTriples to stdout (-), file or directory.

    In case of file export, data from all selected graphs will be concatenated
    in one file.
    In case of directory export, .graph and .nt files will be created
    for each graph.
    """
    if iris == () and not all_:
        raise ValueError("Either specify at least one graph "
                         + "IRI or use the --all option to export all graphs.")
    if all_:
        # in case --all is given,
        # list of graphs is filled with all available graph IRIs
        iris = ([iri["iri"] for iri in get_graphs()])

    count: int = len(iris)
    current: int = 1
    app.echo_debug("graph count is " + str(count))
    if output_dir:
        # output directory set
        app.echo_debug("output is directory")
        # pre-calculate all filenames with the template,
        # in order to output errors on naming clashes as early as possible
        _names = _get_export_names(app, iris, template)
        # create directory
        if not os.path.exists(output_dir):
            app.echo_warning("Output directory does not exist: "
                             + "will create it.")
            os.makedirs(output_dir)
        # one .graph, one .ttl file per named graph
        for iri in iris:
            # join with given output directory and normalize full path
            triple_file_name = os.path.normpath(
                os.path.join(output_dir, _names[iri])
            )
            graph_file_name = triple_file_name + ".graph"
            # output directory is created lazy
            pathlib.Path(
                os.path.dirname(triple_file_name)
            ).mkdir(parents=True, exist_ok=True)
            # create and write the .ttl.graph meta data file
            graph_file = click.open_file(graph_file_name, "w")
            graph_file.write(iri + "\n")
            _get_graph_to_file(
                iri, triple_file_name,
                app,
                numbers=(current, count)
            )
            current = current + 1
    else:
        # no output directory set -> file export
        if output_file == "-":
            # in case a file is stdout,
            # all triples from all graphs go in and other output is suppressed
            app.echo_debug("output is stdout")
            for iri in iris:
                _get_graph_to_file(iri, output_file, app)
        else:
            # in case a file is given, all triples from all graphs go in
            app.echo_debug("output is file")
            for iri in iris:
                _get_graph_to_file(
                    iri, output_file,
                    app,
                    numbers=(current, count),
                    overwrite=False
                )
                current = current + 1


@click.command(name="import")  # noqa: C901
@click.option(
    "--replace",
    is_flag=True,
    help="Replace (overwrite) original graph data."
)
@click.argument(
    "input_path",
    required=True,
    autocompletion=completion.triple_files,
    type=click.Path(
        allow_dash=False,
        readable=True
    )
)
@click.argument(
    "iri",
    type=click.STRING,
    required=False,
    autocompletion=completion.graph_uris
)
@click.pass_obj
def import_command(app, input_path, replace, iri):
    """Import graph(s) to the store.

    If input is an directory, it scans for file-pairs such as xxx.ttl and
    xxx.ttl.graph where xxx.ttl is the actual triples file and xxx.ttl.graph
    contains the graph IRI as one string: "https://mygraph.de/xxx/".
    If input is a file, content will be uploaded to IRI.
    If --replace is set, the data will be overwritten,
    if not, it will be added.
    """
    # is an array of tuples like this [('path/to/triple.file', 'graph IRI')]
    graphs: list
    if os.path.isdir(input_path):
        if iri is not None:
            raise ValueError("Either specify an input file AND a graph IRI "
                             + "or an input directory ONLY.")
        # in case a directory is the source,
        # the graph/nt file structure is crawled
        graphs = read_rdf_graph_files(input_path)
    elif os.path.isfile(input_path):
        if iri is None:
            raise ValueError("Either specify an input file AND a graph IRI "
                             + "or an input directory ONLY.")
        graphs = [(input_path, iri)]
    else:
        # TODO: support for stdin stream
        raise NotImplementedError(
            "Input from special files "
            + "(socket, FIFO, device file) is not supported."
        )

    processed_graphs: set = set()
    count: int = len(graphs)
    current: int = 1
    for (triple_file, graph_iri) in graphs:
        app.echo_info("Import file {}/{}: {} from {} ... "
                      .format(current, count, graph_iri, triple_file),
                      nl=False)
        # prevents re-replacing of graphs in a single run
        _replace = False if graph_iri in processed_graphs else replace
        graph_api.post(graph_iri, triple_file, replace=_replace)
        app.echo_success("replaced" if _replace else "added")
        # refresh access conditions in case of dropped AC graph
        if graph_iri == refresh.AUTHORIZATION_GRAPH_URI:
            refresh.get()
            app.echo_debug("Access conditions refreshed.")
        processed_graphs.add(graph_iri)
        current += 1


@click.command(name="delete")
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Drop all (writeable) graphs"
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.writable_graph_uris
)
@click.pass_obj
def delete_command(app, all_, iris):
    """Delete graph(s) from the store."""
    if iris == () and not all_:
        raise ValueError("Either specify at least one graph IRI "
                         + "or use the --all option to drop all graphs.")
    if all_:
        # in case --all is given,
        # list of graphs is filled with all available graph IRIs
        iris = (
            [iri["iri"] for iri in get_graphs(writeable=True, readonly=False)]
        )

    count: int = len(iris)
    current: int = 1
    for iri in iris:
        app.echo_info("Drop graph {}/{}: {} ... "
                      .format(current, count, iri), nl=False)
        graph_api.delete(iri)
        app.echo_success("done")
        # refresh access conditions in case of dropped AC graph
        if iri == refresh.AUTHORIZATION_GRAPH_URI:
            refresh.get()
            app.echo_debug("Access conditions refreshed.")
        current = current + 1


@click.command(name="open")
@click.argument(
    "iri",
    type=click.STRING,
    autocompletion=completion.graph_uris
)
@click.pass_obj
def open_command(app, iri):
    """Open / explore a graph in the browser."""
    explore_uri = get_cmem_base_uri() + "/explore?graph=" + quote(iri)
    click.launch(explore_uri)
    app.echo_debug(explore_uri)


@click.command(name="count")
@click.option(
    "-a", "--all", "all_",
    is_flag=True,
    help="Count all graphs"
)
@click.option(
    "-s", "--summarize",
    is_flag=True,
    help="Display only a sum of all counted graphs together"
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    autocompletion=completion.graph_uris
)
@click.pass_obj
def count_command(app, all_, summarize, iris):
    """Count triples in graph(s).

    This command lists graphs with their triple count.
    Counts are done without following imported graphs.
    """
    if iris == () and not all_:
        raise ValueError("Either specify at least one graph IRI "
                         + "or use the --all option to count all graphs.")
    if all_:
        # in case --all is given,
        # list of graphs is filled with all available graph IRIs
        iris = (
            [iri["iri"] for iri in get_graphs()]
        )

    count: int
    overall_sum: int = 0
    current: int = 1
    for iri in iris:
        count = count_graph(iri)
        overall_sum = overall_sum + count
        current = current + 1
        if not summarize:
            app.echo_result("{} {}".format(str(count), iri))
    if summarize:
        app.echo_result(overall_sum)


@click.group()
def graph():
    """List, import, export, delete or open graphs.

    Graphs are identified by an IRI. The get a list of existing graphs,
    execute the list command or use tab-completion.
    """


graph.add_command(count_command)
graph.add_command(list_command)
graph.add_command(export_command)
graph.add_command(delete_command)
graph.add_command(import_command)
graph.add_command(open_command)
