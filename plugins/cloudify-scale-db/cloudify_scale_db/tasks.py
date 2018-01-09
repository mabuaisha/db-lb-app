#!/usr/bin/env python

import subprocess
from cloudify import exceptions
from cloudify.manager import get_rest_client
from cloudify.workflows import ctx
from cloudify.decorators import workflow


def check_api(client_callable, arguments=None, _progress_handler=None):
    """ Check for API Response and handle generically. """

    try:
        if isinstance(arguments, dict):
            response = client_callable(**arguments)
        elif arguments is None:
            response = client_callable()
        elif _progress_handler is not None:
            response = client_callable(
                arguments, progress_callback=_progress_handler)
        else:
            response = client_callable(arguments)
    except ConnectionError as e:
        raise OperationRetry('Retrying after error: {0}'.format(str(e)))
    except CloudifyClientError as e:
        if e.status_code == 502:
            raise OperationRetry('Retrying after error: {0}'.format(str(e)))
        else:
            ctx.logger.error('Ignoring error: {0}'.format(str(e)))
    else:
        ctx.logger.debug('Returning response: {0}'.format(response))
        return response
    return None



@workflow
def execute_scale(deployment_id, workflow_id, parameters, **_):
    client = get_rest_client()
    client_arguments = {
        'deployment_id': deployment_id,
        'workflow_id': 'scale',
        'parameters': {
            'scalable_entity_name': 'app_group'
        }
    }
    output = check_api(client.executions.start, client_arguments)
    output = check_api(client.deployments.outputs.get, {'deployment_id': deployment_id})
