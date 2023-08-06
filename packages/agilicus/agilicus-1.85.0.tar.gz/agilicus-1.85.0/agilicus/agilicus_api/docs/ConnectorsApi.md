# agilicus_api.ConnectorsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_agent_connector**](ConnectorsApi.md#create_agent_connector) | **POST** /v1/agent_connectors | Create an agent connector
[**delete_agent_connector**](ConnectorsApi.md#delete_agent_connector) | **DELETE** /v1/agent_connectors/{connector_id} | Delete a agent
[**get_agent_connector**](ConnectorsApi.md#get_agent_connector) | **GET** /v1/agent_connectors/{connector_id} | Get an agent
[**get_agent_info**](ConnectorsApi.md#get_agent_info) | **GET** /v1/agent_connectors/{connector_id}/info | Get information associated with connector
[**get_connector**](ConnectorsApi.md#get_connector) | **GET** /v1/connectors/{connector_id} | Get a connector
[**list_agent_connector**](ConnectorsApi.md#list_agent_connector) | **GET** /v1/agent_connectors | list agent connectors
[**list_connector**](ConnectorsApi.md#list_connector) | **GET** /v1/connectors | List connectors
[**replace_agent_connector**](ConnectorsApi.md#replace_agent_connector) | **PUT** /v1/agent_connectors/{connector_id} | Update an agent


# **create_agent_connector**
> AgentConnector create_agent_connector(agent_connector)

Create an agent connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ConnectorsApi(api_client)
    agent_connector = agilicus_api.AgentConnector() # AgentConnector | 

    try:
        # Create an agent connector
        api_response = api_instance.create_agent_connector(agent_connector)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->create_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_connector** | [**AgentConnector**](AgentConnector.md)|  | 

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New agent |  -  |
**400** | The contents of the request body are invalid |  -  |
**409** | agent already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_agent_connector**
> delete_agent_connector(connector_id, org_id=org_id)

Delete a agent

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a agent
        api_instance.delete_agent_connector(connector_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->delete_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | agent was deleted |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_connector**
> AgentConnector get_agent_connector(connector_id, org_id=org_id)

Get an agent

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get an agent
        api_response = api_instance.get_agent_connector(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent found and returned |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_info**
> AgentConnectorInfo get_agent_info(connector_id, org_id=org_id)

Get information associated with connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get information associated with connector
        api_response = api_instance.get_agent_info(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**AgentConnectorInfo**](AgentConnectorInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent info found and returned |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connector**
> Connector get_connector(connector_id, org_id=org_id)

Get a connector

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a connector
        api_response = api_instance.get_connector(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**Connector**](Connector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | connector found and returned |  -  |
**404** | Connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_agent_connector**
> ListAgentConnectorResponse list_agent_connector(limit=limit, org_id=org_id, name=name)

list agent connectors

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ConnectorsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
name = 'host1_connector' # str | Query the connector by name (optional)

    try:
        # list agent connectors
        api_response = api_instance.list_agent_connector(limit=limit, org_id=org_id, name=name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->list_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **name** | **str**| Query the connector by name | [optional] 

### Return type

[**ListAgentConnectorResponse**](ListAgentConnectorResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of agent connectors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connector**
> ListConnectorResponse list_connector(limit=limit, org_id=org_id, name=name, type=type)

List connectors

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ConnectorsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
name = 'host1_connector' # str | Query the connector by name (optional)
type = 'agent' # str | connector type (optional)

    try:
        # List connectors
        api_response = api_instance.list_connector(limit=limit, org_id=org_id, name=name, type=type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->list_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **name** | **str**| Query the connector by name | [optional] 
 **type** | **str**| connector type | [optional] 

### Return type

[**ListConnectorResponse**](ListConnectorResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of connectors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_agent_connector**
> AgentConnector replace_agent_connector(connector_id, org_id=org_id, agent_connector=agent_connector)

Update an agent

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)
agent_connector = agilicus_api.AgentConnector() # AgentConnector |  (optional)

    try:
        # Update an agent
        api_response = api_instance.replace_agent_connector(connector_id, org_id=org_id, agent_connector=agent_connector)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **agent_connector** | [**AgentConnector**](AgentConnector.md)|  | [optional] 

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent updated |  -  |
**400** | The contents of the request body are invalid |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

