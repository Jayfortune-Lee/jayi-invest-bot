import gspread
from google.oauth2.service_account import Credentials
import json
import os

def get_portfolio_data():
    # GitHub Secrets에 저장한 JSON 문자열을 가져옴
    service_account_info = json.loads(os.getenv('GCP_SERVICE_ACCOUNT_KEY'))
    
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 아까 복사해둔 시트 ID (URL에 있는 긴 문자열)
    sheet_id = os.getenv('GOOGLE_SHEET_ID') 
    sheet = client.open_by_key(sheet_id).sheet1
    
    return sheet.get_all_records()
