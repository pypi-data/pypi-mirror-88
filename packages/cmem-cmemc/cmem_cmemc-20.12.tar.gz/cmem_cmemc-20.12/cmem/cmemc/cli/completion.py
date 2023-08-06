"""Utility functions for CLI auto-completion functionality."""
# pylint: disable=unused-argument, broad-except
import os

from cmem.cmemc.cli.context import CONTEXT
from cmem.cmemc.cli.utils import get_graphs
from cmem.cmempy.plugins.marshalling import get_marshalling_plugins
from cmem.cmempy.queries import QUERY_CATALOG
from cmem.cmempy.vocabularies import get_vocabularies
from cmem.cmempy.workflow import get_workflows
from cmem.cmempy.workflow.workflows import get_workflows_io
from cmem.cmempy.workspace import (
    get_task_plugin_description,
    get_task_plugins,
)
from cmem.cmempy.workspace.projects.project import get_projects
from cmem.cmempy.workspace.search import list_items


def add_metadata_parameter(list_=None):
    """Extend a list with metadata keys and key descriptions."""
    if list_ is None:
        list_ = []
    list_.insert(
        0,
        ("description", "Metadata: A description.")
    )
    list_.insert(
        0,
        ("label", "Metadata: A name.")
    )
    return list_


def dataset_parameter(ctx, args, incomplete):
    """Prepare a list of dataset parameter for a dataset type."""
    CONTEXT.set_connection_from_args(args)
    incomplete = incomplete.lower()
    # look if cursor is in value position of the -p option and
    # return nothing in case it is (values are not completed atm)
    if args[len(args) - 2] in ("-p", "--parameter"):
        return []
    # try to determine the dataset type
    dataset_type = None
    for num, arg in enumerate(args):
        if arg == "--type":
            dataset_type = args[num + 1]
    # without type, we know nothing
    if dataset_type is None:
        return []
    plugin = get_task_plugin_description(dataset_type)
    properties = plugin["properties"]
    options = []
    for key in properties:
        description = "{}: {}".format(
            properties[key]["title"],
            properties[key]["description"],
        )
        options.append((key, description))
    options = add_metadata_parameter(options)
    # restrict to search
    options = [
        key for key in options
        if (key[0].lower().find(incomplete.lower()) != -1
            or key[1].lower().find(incomplete.lower()) != -1
            )
    ]
    return options


def dataset_types(ctx, args, incomplete):
    """Prepare a list of dataset types."""
    CONTEXT.set_connection_from_args(args)
    incomplete = incomplete.lower()
    options = []
    plugins = get_task_plugins()
    for plugin_id in plugins:
        plugin = plugins[plugin_id]
        title = plugin["title"]
        description = "{}: {}".format(
            title,
            plugin["description"].partition("\n")[0]
        )
        if plugin["taskType"] == "Dataset" and (
                title.lower().find(incomplete.lower()) != -1
                or description.lower().find(incomplete.lower()) != -1):
            options.append(
                (
                    plugin_id,
                    description
                )
            )
    return options


def dataset_ids(ctx, args, incomplete):
    """Prepare a list of projectid:datasetid dataset identifier."""
    CONTEXT.set_connection_from_args(args)
    options = []
    results = list_items(item_type="dataset")
    datasets = results["results"]
    for _ in datasets:
        options.append(
            (
                _["projectId"] + r"\:" + _["id"],
                _["label"]
            )
        )
    options = [
        dataset for dataset in options
        if dataset not in args
        # to-complete string can match ID or label
        and (dataset[0].lower().find(
            incomplete.lower()
        ) != -1 or dataset[1].lower().find(
            incomplete.lower()) != -1
        )
    ]
    return options


def vocabularies(ctx, args, incomplete, filter_="all"):
    """Prepare a list of vocabulary graphs for auto-completion."""
    CONTEXT.set_connection_from_args(args)
    incomplete = incomplete.lower()
    options = []
    try:
        vocabs = get_vocabularies(filter_=filter_)
    except Exception:
        # if something went wrong, die silently
        return []
    for _ in vocabs:
        url = _["iri"].replace(":", r"\:")
        label = _["vocabularyLabel"] or "Vocabulary in graph " + url
        if url in args:
            continue
        if incomplete != "":
            if url.lower().find(incomplete) != -1 \
                    or label.lower().find(incomplete) != -1:
                options.append((url, label))
        else:
            options.append((url, label))
    return options


def installed_vocabularies(ctx, args, incomplete):
    """Prepare a list of installed vocabulary graphs."""
    return vocabularies(ctx, args, incomplete, filter_="installed")


def installable_vocabularies(ctx, args, incomplete):
    """Prepare a list of installable vocabulary graphs."""
    return vocabularies(ctx, args, incomplete, filter_="installable")


def file_list(incomplete="", suffix="", description=""):
    """Prepare a list of files with specific parameter."""
    if os.path.isdir(incomplete):
        # given string is a directory, so we scan this directory and
        # add it as a prefix
        directory = incomplete
        incomplete = ""
        prefix = os.path.realpath(incomplete) + "/"
    else:
        # given string is NOT a directory so we just scan the current
        # directory
        directory = os.getcwd()
        prefix = ""
    options = []
    for file_name in os.listdir(directory):
        if os.path.isfile(file_name) \
                and file_name.endswith(suffix) \
                and file_name.lower().find(incomplete.lower()) != -1:
            options.append((prefix + file_name, description))
    return sorted(options, key=lambda x: x[1].casefold())


def workflow_io_ids(ctx, args, incomplete):
    """Prepare a list of io workflows."""
    CONTEXT.set_connection_from_args(args)
    incomplete = incomplete.lower()
    options = []
    for _ in get_workflows_io():
        workflow_id = _["projectId"] + r"\:" + _["id"]
        label = _["label"]
        if workflow_id.lower().find(incomplete) != -1 \
                or label.lower().find(incomplete) != -1:
            options.append((workflow_id, label))
    return options


def workflow_io_input_files(ctx, args, incomplete):
    """Prepare a list of acceptable workflow io input files."""
    return file_list(
        incomplete=incomplete,
        suffix=".csv",
        description="CSV Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".xml",
        description="XML Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".json",
        description="JSON Dataset resource"
    )


def workflow_io_output_files(ctx, args, incomplete):
    """Prepare a list of acceptable workflow io output files."""
    return file_list(
        incomplete=incomplete,
        suffix=".csv",
        description="CSV Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".xml",
        description="XML Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".json",
        description="JSON Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".xlsx",
        description="Excel Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".ttl",
        description="RDF file Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".nt",
        description="RDF file Dataset resource"
    )


def dataset_files(ctx, args, incomplete):
    """Prepare a list of SPARQL files."""
    return file_list(
        incomplete=incomplete,
        suffix=".csv",
        description="CSV Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".xlsx",
        description="Excel Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".xml",
        description="XML Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".json",
        description="JSON Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".ttl",
        description="RDF file Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".zip",
        description="multiCsv Dataset resource"
    ) + file_list(
        incomplete=incomplete,
        suffix=".orc",
        description="Apache ORC Dataset resource"
    )


def project_files(ctx, args, incomplete):
    """Prepare a list of workspace files."""
    return file_list(
        incomplete=incomplete,
        suffix=".project.zip",
        description="eccenca Corporate Memory project backup file"
    )


def ini_files(ctx, args, incomplete):
    """Prepare a list of workspace files."""
    return file_list(
        incomplete=incomplete,
        suffix=".ini",
        description="INI file"
    )


def workspace_files(ctx, args, incomplete):
    """Prepare a list of workspace files."""
    return file_list(
        incomplete=incomplete,
        suffix=".workspace.zip",
        description="eccenca Corporate Memory workspace backup file"
    )


def sparql_files(ctx, args, incomplete):
    """Prepare a list of SPARQL files."""
    return file_list(
        incomplete=incomplete,
        suffix=".sparql",
        description="SPARQL query file"
    ) + file_list(
        incomplete=incomplete,
        suffix=".rq",
        description="SPARQL query file"
    )


def triple_files(ctx, args, incomplete):
    """Prepare a list of triple files."""
    return file_list(
        incomplete=incomplete,
        suffix=".ttl",
        description="RDF Turtle file"
    ) + file_list(
        incomplete=incomplete,
        suffix=".nt",
        description="RDF NTriples file"
    )


def placeholder(ctx, args, incomplete):
    """Prepare a list of placeholder from the to-be executed queries."""
    # look if cursor is in value position of the -p option and
    # return nothing in case it is (values are not completed atm)
    if args[len(args) - 2] in ("-p", "--parameter"):
        return []
    # setup configuration
    CONTEXT.set_connection_from_args(args)
    # extract placeholder from given queries in the command line
    options = []
    for num, arg in enumerate(args):
        query = QUERY_CATALOG.get_query(arg)
        if query is not None:
            options.extend(
                list(query.get_placeholder_keys())
            )
    # look for already given parameter in the arguments and remove them from
    # the available options
    for num, arg in enumerate(args):
        if num - 1 > 0 and args[num - 1] in ("-p", "--parameter"):
            options.remove(arg)
    # remove all non-matching placeholder if incomplete is given
    options = [
        p for p in options
        if p.lower().find(incomplete.lower()) != -1
    ]
    # additional debug output options (needed for all completion functions)
    # options.append("incomplete: -> " + incomplete + " <-")
    # options.append("args: -> " + str(args) + " <-")
    # options.append("len(args): -> " + str(len(args)) + " <-")
    return sorted(set(options), key=str.casefold)


def remote_queries(ctx, args, incomplete):
    """Prepare a list of query URIs."""
    CONTEXT.set_connection_from_args(args)
    incomplete = incomplete.lower()
    options = []
    for _, query in QUERY_CATALOG.get_queries().items():
        url = query.short_url.replace(":", r"\:")
        label = query.label
        if incomplete != "":
            if url.lower().find(incomplete) != -1 \
                    or label.lower().find(incomplete) != -1:
                options.append((url, label))
        else:
            options.append((url, label))
    return sorted(options, key=lambda x: x[1].casefold())


def remote_queries_and_sparql_files(ctx, args, incomplete):
    """Prepare a list of named queries, query files and directories."""
    remote = remote_queries(ctx, args, incomplete)
    files = sparql_files(ctx, args, incomplete)
    return remote + files


def workflow_ids(ctx, args, incomplete):
    """Prepare a list of projectid:taskid workflow identifier."""
    CONTEXT.set_connection_from_args(args)
    options = []
    for project_desc in get_projects():
        for workflow_id in get_workflows(project_desc["name"]):
            options.append(project_desc["name"] + ":" + workflow_id)
    options = [
        workflow for workflow in options
        if workflow not in args
        and workflow.lower().find(incomplete.lower()) != -1
    ]
    return sorted(options, key=str.casefold)


def marshalling_plugins(ctx, args, incomplete):
    """Prepare a list of supported workspace/project import/export plugins."""
    CONTEXT.set_connection_from_args(args)
    options = get_marshalling_plugins()
    if "description" in options[0].keys():
        return [(_["id"], _["description"]) for _ in options]
    # in case, no descriptions are available, labels are fine as well
    return [(_["id"], _["label"]) for _ in options]


def project_ids(ctx, args, incomplete):
    """Prepare a list of project IDs for auto-completion."""
    CONTEXT.set_connection_from_args(args)
    try:
        catalog = get_projects()
    except Exception:
        # if something went wrong, die silently
        return []
    # strip down to an ID only list and filter for already given IDs in args
    # remove IDs where typed string is found in (not begins with)
    options = [
        project['name'] for project
        in catalog
        if project['name'] not in args
        and project['name'].lower().find(incomplete.lower()) != -1
    ]
    return sorted(options, key=str.casefold)


def graph_uris(ctx, args, incomplete):
    """Prepare a list of graphs for auto-completion."""
    CONTEXT.set_connection_from_args(args)
    try:
        graphs = get_graphs()
    except Exception:
        # if something went wrong, die silently
        return []
    # strip down to an IRI only list and filter for already given IRIs in args
    # remove IRIs where typed string is found in (not begins with)
    options = [
        graph['iri'] for graph
        in graphs
        if graph['iri'] not in args
        and graph['iri'].lower().find(incomplete.lower()) != -1
    ]
    return sorted(options, key=str.casefold)


def writable_graph_uris(ctx, args, incomplete):
    """Prepare a list of writable graphs for auto-completion."""
    # seeAlso: https://github.com/pallets/click/issues/942
    CONTEXT.set_connection_from_args(args)
    try:
        graphs = get_graphs(writeable=True, readonly=False)
    except Exception:
        # if something went wrong, die silently
        return []
    # strip down to an IRI only list and filter for already given IRIs in args
    graphs = [graph['iri'] for graph in graphs if graph['iri'] not in args]
    # remove IRIs where typed string is found in (not begins with)
    graphs = [
        iri for iri in graphs
        if iri.lower().find(incomplete.lower()) != -1
    ]
    return sorted(graphs, key=str.casefold)


def connections(ctx, args, incomplete):
    """Prepare a list of config connections for auto-completion."""
    # since ctx does not have an obj here, we re-create the object
    CONTEXT.set_connection_from_args(args)
    options = []
    for section in CONTEXT.config.sections():
        if section.lower().find(incomplete.lower()) != -1:
            options.append(section)
    return sorted(options, key=str.casefold)


def project_export_templates(ctx, args, incomplete):
    """Prepare a list of example templates for the project export command."""
    examples = [
        (
            "{{id}}",
            "Example: a plain file name"
        ),
        (
            "{{date}}-{{connection}}-{{id}}.project",
            "Example: a more descriptive file name"),
        (
            "dumps/{{connection}}/{{id}}/{{date}}.project",
            "Example: a whole directory tree"
        )
    ]
    return examples


def workspace_export_templates(ctx, args, incomplete):
    """Prepare a list of example templates for the workspace export command."""
    examples = [
        (
            "workspace",
            "Example: a plain file name"
        ),
        (
            "{{date}}-{{connection}}.workspace",
            "Example: a more descriptive file name"),
        (
            "dumps/{{connection}}/{{date}}.workspace",
            "Example: a whole directory tree"
        )
    ]
    return examples
