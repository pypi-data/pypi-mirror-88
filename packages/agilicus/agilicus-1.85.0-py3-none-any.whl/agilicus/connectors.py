import agilicus

from . import context
from .input_helpers import get_org_from_input_or_ctx


def query(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    query_results = apiclient.connectors_api.list_connector(**kwargs)
    return query_results


def query_agents(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    query_results = apiclient.connectors_api.list_agent_connector(**kwargs)
    return query_results


def add_agent(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    spec = agilicus.AgentConnectorSpec(org_id=org_id, **kwargs)
    connector = agilicus.AgentConnector(spec=spec)
    return apiclient.connectors_api.create_agent_connector(connector)


def get_agent(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    return apiclient.connectors_api.get_agent_connector(
        connector_id, org_id=org_id, **kwargs
    )


def delete_agent(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    return apiclient.connectors_api.delete_agent_connector(
        connector_id, org_id=org_id, **kwargs
    )


def get_agent_info(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    return apiclient.connectors_api.get_agent_info(connector_id, org_id=org_id, **kwargs)


def replace_agent(
    ctx,
    connector_id,
    connection_uri=None,
    max_number_connections=None,
    name=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    connector = apiclient.connectors_api.get_agent_connector(
        connector_id, org_id=org_id, **kwargs
    )

    if connection_uri:
        connector.spec.connection_uri = connection_uri

    if max_number_connections:
        connector.spec.max_number_connections = max_number_connections

    if name:
        connector.spec.name = name

    return apiclient.connectors_api.replace_agent_connector(
        connector_id, agent_connector=connector
    )
