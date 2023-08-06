# AgentConnectorSpec

The specification of the Connector
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A descriptive name for the connector | 
**org_id** | **str** | Unique identifier | 
**max_number_connections** | **int** | The maximum number of connections to maintain to the cluster when stable. Note that this value may be exceeded during times of reconfiguration. A value of zero means that the connector is effectively unused by this Secure Agent.  | [optional] 
**connection_uri** | **str** | Overrides the default URI used to connect to this connector. This can be used to point the Secure Agent somewhere other than the default.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


