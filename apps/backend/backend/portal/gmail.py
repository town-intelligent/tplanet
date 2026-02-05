import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_gmail(subject, to, cont):
    content = MIMEMultipart()
    content["subject"] = subject
    content["from"] = "townintelligent@gmail.com" # 寄件者
    content["to"] = to # 收件者
    content.attach(MIMEText(cont)) # 郵件內容
    
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定 SMTP 伺服器
        try:
            smtp.ehlo()  # 驗證 SMTP 伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("townintelligent@gmail.com", "lvvgpkxfmcgynhpw")  # 登入寄件者gmail
            smtp.sendmail("townintelligent@gmail.com", to, cont)
            return True
        except Exception as e:
            print("Error message: ", e)
            return False

# send_gmail("hello title", "yillkid@gmail.com", "hello content")
