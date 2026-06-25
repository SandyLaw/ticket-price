import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========== 邮件配置 ==========
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# ========== 读取航线 ==========
with open("routes.json", "r", encoding="utf-8") as f:
    routes = json.load(f)["routes"]

# ========== 模拟价格数据（后面可接真实API） ==========
def get_mock_price(route):
    import random
    base = random.randint(1200, 9000)
    return base

# ========== 生成报告 ==========
results = []

for r in routes:
    price = get_mock_price(r)

    results.append({
        "route": f"广州 → {r['city']}",
        "price": price,
        "airline": "推荐航司",
        "transit": "1次中转（模拟）",
        "baggage": "行李直挂",
        "visa": "无需过境签"
    })

# ========== HTML ==========
today = datetime.now().strftime("%Y-%m-%d")

html = f"""
<h2>Weekly Flight Monitor Report</h2>
<p>Date: {today}</p>

<table border="1" cellpadding="5">
<tr>
<th>航线</th>
<th>价格</th>
<th>航司</th>
<th>中转</th>
<th>行李</th>
<th>签证</th>
</tr>
"""

for r in results:
    html += f"""
    <tr>
        <td>{r['route']}</td>
        <td>{r['price']}</td>
        <td>{r['airline']}</td>
        <td>{r['transit']}</td>
        <td>{r['baggage']}</td>
        <td>{r['visa']}</td>
    </tr>
    """

html += "</table>"

# ========== 发邮件 ==========
msg = MIMEMultipart()
msg["Subject"] = "Weekly Flight Monitor"
msg["From"] = EMAIL_USER
msg["To"] = RECEIVER_EMAIL

msg.attach(MIMEText(html, "html"))

try:
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("邮件发送成功")
except Exception as e:
    print("邮件发送失败:", e)
