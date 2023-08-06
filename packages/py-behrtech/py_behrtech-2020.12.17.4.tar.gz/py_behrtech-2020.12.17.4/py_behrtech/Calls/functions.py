

def buildParameter(params: dict) -> str:
    """
    Builds endpoint URL for URL variables

    :param params: Input parameters of function
    :return: Endpoint URL for URL variables
    """

    parameters = ''

    for x in params:
        if x != 'self' and params[x]:
            if not parameters:
                if x == 'start':
                    parameters += f'?from={params[x]}'
                elif x == 'end':
                    parameters += f'?to={params[x]}'
                else:
                    parameters += f'?{x}={params[x]}'
            else:
                if x == 'start':
                    parameters += f'&from={params[x]}'
                elif x == 'end':
                    parameters += f'&to={params[x]}'
                else:
                    parameters += f'&{x}={params[x]}'

    return parameters
