import uuid
import requests
import datetime,time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.request import RpcRequest
import json
from sqlalchemy import create_engine, text, Table, Column, MetaData, Integer, String, DateTime, DECIMAL, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

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
        engine = create_engine('mysql+pymysql://root:123456@10.0.0.200:11306/quant',echo=False)

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

class  Stock_Daily_Quote(Base):
    __tablename__='stock_daily_quote'

    id = Column(Integer,primary_key=True)
    trading_date = Column(DateTime)
    code = Column(String(40))
    closing_price = Column(DECIMAL(10,2))
    highest_price = Column(DECIMAL(10,2))
    lowest_price = Column(DECIMAL(10,2))
    opening_price = Column(DECIMAL(10,2))
    last_closing_price = Column(DECIMAL(10,2))
    diff_pice = Column(DECIMAL(10,2))
    diff_rate = Column(DECIMAL(10,2))
    turnover_rate = Column(DECIMAL(20,2))
    turnover_quantity = Column(Integer)
    turnover_amount = Column(DECIMAL(20,2))
    total_market_value = Column(DECIMAL(20,2))
    circulation_market_value = Column(DECIMAL(20,2))
    deal_count = Column(Integer)
    date_count = Column(Integer)
    unique_code = Column(Integer)

    def __repr__(self):
        return ("Stock_Daily_Quote(id:{},trading_date:{},code:{},closing_price:{},highest_price:{},lowest_price:{},opening_price:{},"
                "last_closing_price:{},diff_pice:{},diff_rate:{},turnover_rate:{},turnover_quantity:{},turnover_amount:{},"
                "total_market_value:{},circulation_market_value:{},deal_count:{},date_count:{},unique_code::{})"
                .format(self.id,self.trading_date,self.code,self.closing_price,self.highest_price,self.lowest_price,
                        self.opening_price,self.last_closing_price,self.diff_pice,self.diff_rate,self.turnover_rate,
                        self.turnover_quantity,self.turnover_amount,self.total_market_value,self.circulation_market_value,
                        self.deal_count,self.date_count,self.unique_code))

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

def process(cache, quotes):
    global lowest_value
    session = Operator().Session()
    positions = session.query(Position.id, Position.trading_date, Position.code, Position.quantity,
                               Position.price).all()
    for pos in positions:
        print(pos)
        if pos.code not in quotes :
            last_stock_daily_quote = session.query(Stock_Daily_Quote).filter(
                Stock_Daily_Quote.code == str(pos.code).zfill(6)).order_by(Stock_Daily_Quote.id.desc()).first()
            quotes[pos.code] = last_stock_daily_quote

        quote = quotes[pos.code]

        result = downloadQuote(pos.code)
        if result:
            info = dict()
            for d in result:
                info[d['item']] = d['value']

            # if cache.get(pos.code) is None:
            #     cache[pos.code] = []
            #
            # cache[pos.code].append(info)
            # q = [d for d in result if d['code'] == pos.code]

            #
            # if cache.get(pos.code) == None:
            #     cache[pos.code] = []
            # cache[pos.code].append(info)
            # flag = judge(cache[pos.code],quote)
            flag = judge(info, quote)
            if flag:
                # result = send_sms("15910696951", "{'name':'股票["+pos.code+"](V字形)'}")
                print("--------------SEND MESSAGE----------------")
                print("<突破>：当前价格：{:.2f}，最低价格:{:.2f}，昨日价格：{:.2f}".format(info['buy_1'],lowest_value,float(quote.closing_price)))
                print("------------------------------------------")

index = 0
is_low = False
lowest_value = 10000
# def loadCache():
#     global _cache
#     with open("cache.json", 'r') as file:
#         _cache = json.load(file)

# def downloadQuote(code):
#     global index
#     global _cache
#     if not _cache:
#         loadCache()
#
#     try:
#         if len(_cache) <= index:
#             return None
#         else:
#             r = _cache[index]
#             index = index + 1
#             return r
#     except IndexError:
#         print("********index:"+index+"*******")



def downloadQuote(code):
    url = 'http://47.121.26.177:5001/api/public/stock_bid_ask_em?symbol=' + code
    # 发送HTTP GET请求
    response = requests.get(url)
    if response.status_code == 200:
        datas = response.json()
        print(datas)
        return datas
    else:
        print("请求失败，状态码:", response.status_code)
        return None

def judge(info,quote):
    print(info['buy_1'])
    global is_low
    global lowest_value

    last_closing_price = float(quote.closing_price)

    try:
        buy_1 = float(info['buy_1'])
        if not is_low:
            if buy_1 < last_closing_price:
                print("=====价格低于昨日价格======")
                if buy_1 < lowest_value:
                    print("=====价格进一步下探======")
                    lowest_value = buy_1
                    if (last_closing_price - lowest_value) / last_closing_price > 0.03:
                        is_low = True
                        print("=====价格降低到阈值======")
        elif (buy_1 - last_closing_price) / last_closing_price > 0.005:
            is_low = False
            print("=====价格升高超过昨日价格======")
            return True
    except Exception as e:
        print(f"###############:{e}")

    return False

if __name__ == "__main__":
    openTime = datetime.datetime.now().replace(hour=9,minute=30,second=0)
    closeTime = datetime.datetime.now().replace(hour=15,minute=0,second=0)
    quotes = dict()
    while True:
        now = datetime.datetime.now()

        if now > closeTime:
            break

        if (now > openTime and now < closeTime) :
            process(quotes)

        time.sleep(5)