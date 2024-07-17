import uuid
import requests
import datetime,time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.request import RpcRequest
import json
from sqlalchemy import create_engine, text, Table, Column, MetaData, Integer, String, Double, DateTime, DECIMAL, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

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

class  Operator(object):

    engine = None

    def __init__(self):
        engine = create_engine('mysql+pymysql://root:root@localhost:3306/quant',echo=True)

        Base.metadata.create_all(engine,checkfirst=True)

        self.Session = sessionmaker(bind=engine)

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

class Position(Base):
    __tablename__='position'

    id = Column(Integer,primary_key=True)
    trading_date = Column(DateTime)
    code = Column(String(40))
    quantity = Column(Integer)
    price = Column(DECIMAL(10,4))

    def __repr__(self):
        return "Stock(id:{},code:{},quantity:{},price:{},trading_date:{}"\
            .format(self.id,self.code,self.quantity,self.price,self.trading_date)

if __name__ == "__main__":
    openTime = datetime.datetime.now().replace(hour=9,minute=30,second=0)
    closeTime = datetime.datetime.now().replace(hour=15,minute=0,second=0)
    while True:
        now = datetime.datetime.now()
        if now < openTime:
            time.sleep(5)

        if now > closeTime:
            break

        if (now > openTime and now < closeTime) :

def process():
    session = Operator().Session()
    prositions = session.query(Position.id, Position.trading_date, Position.code, Position.quantity,
                               Position.price).all()
    cache = dict()
    for pos in prositions:
        print(pos)
        # exPos = ExPosition()
        # exPos.id = pos.id
        # exPos.code = str(pos.code).zfill(6)
        # exPos.price = pos.price
        # exPos.quantity = pos.quantity
        # last_stock_daily_quote = session.query(Stock_Daily_Quote).filter(
        #     Stock_Daily_Quote.code == str(pos.code).zfill(6)).order_by(Stock_Daily_Quote.id.desc()).first()
        # exPos.cur_price = last_stock_daily_quote.closing_price
        # exPos.trading_date = pos.trading_date
        # exPos.benefits = pos.quantity * (last_stock_daily_quote.closing_price - pos.price)
        # exPositions.append(exPos)

        url = 'http://47.121.26.177:5001/api/public/stock_bid_ask_em?symbol='+pos.code
        # 发送HTTP GET请求
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)

            if cache.get(pos.code) == None:
                cache[pos.code] = data

            # for d in data_array:
            #     if d["代码"] == pos.code:


        else:
            print("请求失败，状态码:", response.status_code)

    # url = 'http://47.121.26.177:5001/api/public/stock_bid_ask_em?symbol=000001'
    # # 发送HTTP GET请求
    # response = requests.get(url)
    # if response.status_code == 200:
    #     # 解析JSON数组
    #     data_array = response.json()
    #     print(data_array)
    #
    #     with open('temp.json', 'w') as file:
    #         json.dump(data_array, file, indent=4)
    #
    #     # for d in data_array:
    #     #     if d["代码"] == pos.code:
    #
    #
    # else:
    #     print("请求失败，状态码:", response.status_code)

