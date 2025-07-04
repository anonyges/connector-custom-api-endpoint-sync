# connector-custom-api-endpoint-sync

FortiSOAR connector to get synchonous Custom Api Endpoint

## How to use

1. Copy and paste the custom_api_endpoint_url by button
2. Set the API Key
3. Call the connector with the below curl command

```shell
curl -X POST 'https://{your_domain_here}:{port}/api/integration/execute/?format=json' \
-H "Authorization: API-KEY {API_KEY}" \
-H "Content-Type: application/json;charset=UTF-8" \
-H "Accept: application/json, text/plain, */*" \
--insecure \
--data-raw '{
    "connector": "custom-api-endpoint-sync",
    "version": "1.0.0",
    "operation": "custom_api_endpoint_sync_call",
    "params": {
        "api_endpoint": "custom_api_endpoint_url",
        "data": {
            "value": "1.1.1.1"
        }
    }
}'
```

or

```shell
curl -X POST 'https://{your_domain_here}:{port}/api/integration/execute/?format=json' \
-H "Authorization: API-KEY {API_KEY}" \
-H "Content-Type: application/json;charset=UTF-8" \
-H "Accept: application/json, text/plain, */*" \
--insecure \
--data-raw '{
    "connector": "custom-api-endpoint-sync",
    "version": "1.0.0",
    "operation": "custom_api_endpoint_sync_call",
    "params": {
        "api_endpoint": "custom_api_endpoint_url",
        "data": {
            "value": "1.1.1.1"
        }
    }
}' | python -m json.tool
```
