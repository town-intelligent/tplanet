import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_gmail(subject, to, cont):
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = subject#"Learn Code With Mike"  #郵件標題
    content["from"] = "townintelligent@gmail.com"  #寄件者
    content["to"] = to #"yillkid@gmail.com" #收件者
    content.attach(MIMEText(cont))# "Demo python send email"))  #郵件內容
    
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("townintelligent@gmail.com", "lvvgpkxfmcgynhpw")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("Complete!")
            return True
        except Exception as e:
            print("Error message: ", e)
            return False

# send_gmail("hello title", "yillkid@gmail.com", "hello content")
