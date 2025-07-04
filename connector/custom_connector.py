# %%
import requests
import re
import json
import time


def get_url_path(url: str, use_remote_url: bool = False) -> [str, str]:
    res = list(re.finditer(r"^https?://", url))
    if len(res) == 1:
        end_http_idx = res[0].end(0)
        url_path_idx = url.find("/", end_http_idx)

        if url_path_idx > 0:
            if use_remote_url:
                return url[:url_path_idx], url[url_path_idx:]
            else:
                return "https://localhost", url[url_path_idx:]
    
    assert False, f"Input url: {url} does not have correct url string eg: `https://url:port/`"


def is_status_completed(status: str) -> bool:
    if status == "finished" or status == "failed" or status == "terminated" or status == "finished+with+error":
        return True
    return False


class CustomConnector:
    def __init__(self):
        pass

    def check_health(self, config: dict, params: dict = None) -> dict:
        c_api_key = config.get("api_key")
        c_verify_ssl = config.get("verify_ssl")

        url = "https://localhost"
        # this connector is ment to be used for localhost calls only

        resp = requests.get(url, verify=c_verify_ssl)
        if resp.status_code != 200:
            raise Exception("not authorized, perhaps API key is wrong")

    def custom_api_endpoint_sync_call(self, config: dict, params: dict) -> dict:
        c_api_key = config.get("api_key")
        c_verify_ssl = config.get("verify_ssl", False)
        c_use_remote_url = config.get("use_remote_url", False)

        p_api_endpoint = params.get("api_endpoint")
        p_headers = {
            "authorization": f"API-KEY {c_api_key}",
            "content-type": "application/json;charset=UTF-8",
            "accept": "application/json, text/plain, */*",
        }
        p_data = params.get("data", "")  # dict or None
        p_retry_count = params.get("retry_count", 60)
        p_retry_wait_seconds = params.get("retry_wait_seconds", 1)
        p_time_limit_seconds = params.get("time_limit_seconds", 60)
        p_return_output_only = params.get("return_output_only", False)

        local_remote_url, api_url = get_url_path(p_api_endpoint, c_use_remote_url)
        url = local_remote_url + api_url
        # this connector is ment to be used for localhost calls only but, debugging purpose

        resp = requests.post(url, headers=p_headers, data=json.dumps(p_data), verify=c_verify_ssl)
        task_id = resp.json().get("task_id")
        if not task_id:
            raise Exception("possible authentication error check API KEY or Permission")
        # return task_id

        time_limit = time.time() + p_time_limit_seconds
        for _idx in range(p_retry_count):
            if time_limit < time.time():
                raise Exception("timeout due to time_limit_seconds")

            url = local_remote_url + f"/api/wf/api/workflows/?task_id={task_id}"
            resp = requests.get(url, headers=p_headers, verify=c_verify_ssl)
            # return playbook workflow_id

            workflow = resp.json().get("hydra:member")
            if len(workflow) == 0:
                time.sleep(p_retry_wait_seconds)
                continue
            # task might not have been created due to resource usage

            if len(workflow) != 1:
                raise Exception(resp.json())
            # critical error in system?

            status = workflow[0].get("status", "")
            if is_status_completed(status):
                workflow_id = workflow[0].get("@id")
                workflow_id = list(filter(None, workflow_id.split("/")))[-1]

                for _r_idx in range(p_retry_count - _idx):
                    url = local_remote_url + f"/api/wf/api/workflows/{workflow_id}/?format=json"
                    resp = requests.get(url, headers=p_headers, verify=c_verify_ssl)

                    final_resp = resp.json()
                    # step_iri = retval.get("@id", "")
                    step_status = final_resp.get("status", "")
                    step_result = final_resp.get("result", {})

                    # print(f"keys: {retval.keys()}")
                    # print(f"step_status: {step_status} step_result: {step_result}")
                    if is_status_completed(step_status) and step_result:
                        if p_return_output_only:
                            return step_result
                        return final_resp
                    else:
                        print(f"coud not fetch status workflow_id: {workflow_id} step_status: {step_status}\nreturn: {final_resp}")
                    # debug for unknown error!

                    time.sleep(p_retry_wait_seconds)
                # give buffer time to let FSR save the result into the database

                raise Exception(f"coud not fetch final result workflow_id: {workflow_id} step_status: {step_status}")
            else:
                time.sleep(p_retry_wait_seconds)
                continue

        raise Exception(f"exited due retry_count: {p_retry_count}")


# # %%
# conn = CustomConnector()
# config = {
#     "api_key": "a",
#     "use_remote_url": True
# }
# params = {
#     "api_endpoint": "https://a:5443/api/triggers/1/a",
#     "data": {"url": "www.cisco.com"},
#     "return_output_only": True
# }

# asd = conn.custom_api_endpoint_sync_call(config, params)

# # %%

# %%
