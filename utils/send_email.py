from django.conf import settings
from django.core.mail import send_mail
import random

sms_type = {
    "verify":"验证",
    "register":"注册",
    "update_pwd":"修改密码",
    "warning":"告警"
}

def create_sms_code():
    return '%06d' % random.randint(0, 999999)



def send_sms_code(sms_code,type,to_email):
    """
    发送邮箱验证码
    :param to_mail: 发到这个邮箱
    :return: 成功：0 失败 -1
    """
    if type==1:
        email_title = '新用户注册'
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为一分钟，请及时进行验证。".format(sms_code)

    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, to_email)

    return send_status