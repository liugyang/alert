#!/usr/bin/env python
# coding=utf-8

import uuid
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.request import RpcRequest
import json

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

# 注意：更改为自己的参数，参数从上面的教程找
sign_name = "股票策略监控告警签名" # 短信签名
template_code = "SMS_465620395" # 模板CODE
ACCESS_KEY_ID = "LTAI5t6SpUF9KaUDSHYV7fYb" # ACCESS_KEY_ID
ACCESS_KEY_SECRET = "qzAuGFMGrjAJjJtllwpEJjlNJxHQtb" # ACCESS_KEY_ID


acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

class SendSmsRequest(RpcRequest):
    def __init__(self):
        RpcRequest.__init__(self, 'Dysmsapi', '2017-05-25', 'SendSms')

    def get_TemplateCode(self):
        return self.get_query_params().get('TemplateCode')

    def set_TemplateCode(self,TemplateCode):
        self.add_query_param('TemplateCode',TemplateCode)

    def get_PhoneNumbers(self):
        return self.get_query_params().get('PhoneNumbers')

    def set_PhoneNumbers(self,PhoneNumbers):
        self.add_query_param('PhoneNumbers',PhoneNumbers)

    def get_SignName(self):
        return self.get_query_params().get('SignName')

    def set_SignName(self,SignName):
        self.add_query_param('SignName',SignName)

    def get_ResourceOwnerAccount(self):
        return self.get_query_params().get('ResourceOwnerAccount')

    def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
        self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

    def get_TemplateParam(self):
        return self.get_query_params().get('TemplateParam')

    def set_TemplateParam(self,TemplateParam):
        self.add_query_param('TemplateParam',TemplateParam)

    def get_ResourceOwnerId(self):
        return self.get_query_params().get('ResourceOwnerId')

    def set_ResourceOwnerId(self,ResourceOwnerId):
        self.add_query_param('ResourceOwnerId',ResourceOwnerId)

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self,OwnerId):
        self.add_query_param('OwnerId',OwnerId)

    def get_SmsUpExtendCode(self):
        return self.get_query_params().get('SmsUpExtendCode')

    def set_SmsUpExtendCode(self,SmsUpExtendCode):
        self.add_query_param('SmsUpExtendCode',SmsUpExtendCode)

    def get_OutId(self):
        return self.get_query_params().get('OutId')

    def set_OutId(self,OutId):
        self.add_query_param('OutId',OutId)



def send_sms(phone_numbers, template_param=None):
    business_id = uuid.uuid4()
    sms_request = SendSmsRequest()
    sms_request.set_TemplateCode(template_code)  # 短信模板变量参数
    if template_param is not None:
        sms_request.set_TemplateParam(template_param)
    sms_request.set_OutId(business_id)  # 设置业务请求流水号，必填。
    sms_request.set_SignName(sign_name)  # 短信签名
    sms_request.set_PhoneNumbers(phone_numbers)  # 短信发送的号码列表，必填。
    sms_response = acs_client.do_action_with_exception(sms_request)  # 调用短信发送接口，返回json

    return sms_response

def query():
    url='http://47.121.26.177:5001/api/public/futures_zh_realtime?symbol=黄金'
    # 发送HTTP GET请求
    response = requests.get(url)

    # 确保请求成功
    if response.status_code == 200:
        # 解析JSON数组
        data_array = response.json()
        print(data_array)
        element = data_array[0]
        value = element['trade']
        return value
    else:
        print("请求失败，状态码:", response.status_code)
        return -1;

def load_json():
    with open("data.json", 'r') as file:
        data = json.load(file)
        return data
def update_json():
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    data = load_json()
    highest_value = data['highest']
    cut_off_value = data['cutoff']
    last_value = query()
    try:
        if last_value < float(cut_off_value):
            print("现价低于退出价格,发送提示短信")
            # result = send_sms("15910696951", "{'name':'黄金(卖）'}")
            # print(str(result, encoding='utf-8'))
            data['cutoff']=last_value*0.95

        else:
            if last_value > float(highest_value):
                print("突破最高历史最高价格，更新最高价格记录")
                data['highest']=last_value
                data['cutoff']=last_value * 0.95

            else:
                print("价格正常")
    except:
        print("没有反弹数据")

    finally:
        update_json()
        print(data)
