import requests
from bs4 import BeautifulSoup
import pytextnow
import time
from datetime import datetime

cookies = {
    'ASP.NET_SessionId': 'x04ablumklzvxepkb45pzu2z',
    '__AntiXsrfToken': 'f6b0e0c6518d47d5bb48c6c084f7ae59',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://helpdesk.gal.fl.gov',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4697.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://helpdesk.gal.fl.gov/logon.aspx?ReturnUrl=%2fPagesForAdmin%2fAdminTicketDetail.aspx%3fid%3d7519&id=7519',
    'Accept-Language': 'en-US,en;q=0.9',
    'sec-gpc': '1',
}

ticket_number = 7519

params = (
    ('ReturnUrl', f'/PagesForAdmin/AdminTicketDetail.aspx?id={ticket_number}'),
    ('id', f'{ticket_number}'),
)

data = {
    '_TSM_HiddenField_': 'ZaMfZ6yYhPPHZ1NeEf8j6-t902-6pHpn2MehV0eep-I1',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': 'ylh4oj1pCru9vVIcQjxvBSEWM6IcCpgLmI7eX9qkb28REJPzMJfxrwstqyLW01sbde+DQKi1AakVG/2jrgdkybdJVGHoUTeApJKwCoqVc7M=',
    '__VIEWSTATEGENERATOR': '5A2128B1',
    '__EVENTVALIDATION': '65hPjzD7NxCvCZ/XvZkmUzXSQ5LPmH6W+sUjrg1FGGerbeVFrPtw6ErDA59LiFEayaMYzsJJOI4Bpf6a+ysEbfNyVovRY8UTDV5IpClMI/B6h1VibPc72uOEu4ZJQWF2P6fdAnTkV7s7G344yr1uhLQx8AZXtQaPptK071VJ1ok=',
    'ctl00$ContentPlaceHolder1$txtUsername': 'malik.butler',
    'ctl00$ContentPlaceHolder1$txtPassword': 'xxxxxxxxxxxxxx',
    'ctl00$ContentPlaceHolder1$btnLogin': 'Login'
}

mobile = pytextnow.Client("username", sid_cookie="check dev tools", csrf_cookie="leave network tab open while logging in")

response = requests.post('http://helpdesk.gal.fl.gov/logon.aspx', headers=headers, params=params, cookies=cookies, data=data, verify=False)

soup = BeautifulSoup(response.content, "html.parser")

assignments = soup.find(id="ContentPlaceHolder1_ddlTech")
tix_date = soup.find(id="ContentPlaceHolder1_tbxCreationDate").get('value')
current_time = datetime.now()
if tix_date and current_time.weekday() < 5 and 17 > current_time.hour > 8:
    assignment = assignments.find('option', selected=True).text
    print(f"Ticket #{ticket_number} is unassigned") if assignment == "Not Assigned" else print(f"Ticket #{ticket_number} is assigned to {assignment}")
    mobile.send_sms("urmomscell", f"Ticket #{ticket_number} is unassigned" if assignment == "Not Assigned" else f"Ticket #{ticket_number} is assigned to {assignment}")
    ticket_number = ticket_number + 1
    print(ticket_number)
else:
    print(f"Ticket #{ticket_number} has no \"Creation Date\"")
    time.sleep(900)
