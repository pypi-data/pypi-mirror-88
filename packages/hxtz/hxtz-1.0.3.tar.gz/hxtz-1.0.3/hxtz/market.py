import requests,json
import pandas as pd

#获取可转债列表，按涨幅排序
def get_code_list():
    url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market'+\
            '_Center.getHQNodeDataSimple?page=1&num=600&sort=symbol&asc=1&node=hskzz_z&_s_r_a=sort'
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
    response = requests.get(url,headers=headers)
    res_dict = json.loads(response.text)
    a_list=[];b_list=[];c_list=[];d_list=[];e_list=[];f_list=[];g_list=[];h_list=[];i_list=[];j_list=[];k_list=[];l_list=[]
    stock_list={'symbol' : a_list,'名称' : b_list,'代码' : c_list,'现价' : d_list,'昨收' : e_list,'涨跌幅' : f_list,
                '今开' : g_list,'最高价' : h_list,'最低价' : i_list,'成交量' : j_list,'成交额' : k_list,'时间' : l_list}
    for item in res_dict:
        a_list.append(item['symbol']);b_list.append(item['name']);c_list.append(item['code'])
        d_list.append(item['trade']);e_list.append(item['settlement']);f_list.append(item['changepercent'])
        g_list.append(item['open']);h_list.append(item['high']);i_list.append(item['low'])
        j_list.append(item['volume']);k_list.append(item['amount']);l_list.append(item['ticktime'])
    data=pd.DataFrame(stock_list)
    data[['现价','昨收','涨跌幅','今开','最高价','最低价','成交量','成交额']]=data[['现价',
        '昨收','涨跌幅','今开','最高价','最低价','成交量','成交额']].astype('float')
    data['时间'] = pd.to_datetime(data['时间'])
    return data
