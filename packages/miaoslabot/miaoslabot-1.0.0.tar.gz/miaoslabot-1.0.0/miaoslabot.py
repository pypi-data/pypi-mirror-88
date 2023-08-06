import requests, time ,os

def sla(url, status, node_name, bot_token, chat_id):
    def get_error(error_num):
        print("\033[31m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：{}".format(str(error_num)))
        data = {
            "chat_id":chat_id,
            "text":"{}：{}".format(node_name,str(error_num.replace(' ','%20'))),
            "reply_markup":'{"inline_keyboard": [[{"text": "問題已解決", "callback_data": "ok"}, {"text": "忽略問題", "callback_data": "pass"}]]}'
        }
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bot_token), timeout=5, params=data)
        open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：{}".format(str(error_num)+"\n"))


    try:
        miao = requests.get(url,timeout=5)
        
        if str(miao) == "<Response [{}]>".format(status):
            print("\033[34m" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "\033[0m：400 OK")
            open(os.getcwd() + "/{}-sla.log".format(node_name),'a+',encoding="utf-8").write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + "：400 OK" + "\n")
        elif str(miao) == "<Response [404]>":
            get_error("404 ERROR")
        elif str(miao) == "<Response [403]>":
            get_error("403 ERROR")
        elif str(miao) == "<Response [503]>":
            get_error("503 ERROR")
        elif str(miao) == "<Response [502]>":
            get_error("502 ERROR")
        else:
            get_error(miao)

    except requests.exceptions.ConnectionError:
        get_error("ConnectionError")

    except requests.exceptions.ReadTimeout:
        get_error("Timeout")

    except:
        get_error("未知錯誤")