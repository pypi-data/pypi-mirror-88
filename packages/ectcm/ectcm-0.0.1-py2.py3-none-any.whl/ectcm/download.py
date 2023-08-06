import requests


def get_clinics(pageno=1, pagesize=2000):
    url = "https://api.ectcm.com:8070/api/clinic/searchClinic"

    payload = f"{{\"pageno\":{pageno},\"pagesize\":{pagesize}}}"
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'sourceType': 'F',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.ectcm.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.ectcm.com/',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    return response.json()


def get_doctors(pageno=1, pagesize=2000):
    url = "https://api.ectcm.com:8070/api/doctorclinic/searchDoctor"

    payload = f"{{\"pageno\":{pageno},\"pagesize\":{pagesize},\"sortdesc\":\"DESC\"}}"
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'sourceType': 'F',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.ectcm.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.ectcm.com/',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    return response.json()


def extract_data_list(res_obj):
    """
    extract the data list (e.g. doctors or clinics) from the response json
    """
    return res_obj['data']['list']

def extract_total_count(res_obj):
    """
    extract the total count from the response json
    """
    return res_obj['data']['total']
