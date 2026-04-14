import os
import requests
import gspread
from google.oauth2.service_account import Credentials
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
client = Anthropic()

def connect_to_sheet():
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    gc = gspread.authorize(creds)
    return gc.open("Lead Enrichment Agent").sheet1

def enrich_company(company_name):
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "company": company_name,
        "api_key": HUNTER_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json().get("data", {})
    return {
        "industry": data.get("industry", "Unknown"),
        "size": str(data.get("size", "Unknown")),
        "location": f"{data.get('city', '')} {data.get('country', '')}".strip(),
    }

def summarize_lead(company_name, enrichment):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""You are a sales assistant. Summarize this lead in 2 sentences and rate fit for an AI data platform (Good/Maybe/Poor).
            
Company: {company_name}
Industry: {enrichment['industry']}
Size: {enrichment['size']}
Location: {enrichment['location']}"""
        }]
    )
    return message.content[0].text

def run():
    sheet = connect_to_sheet()
    rows = sheet.get_all_values()
    
    for i, row in enumerate(rows[1:], start=2):
        company_name = row[0]
        if not company_name or row[1].strip() != "":
            continue
            
        print(f"Enriching {company_name}...")
        enrichment = enrich_company(company_name)
        summary = summarize_lead(company_name, enrichment)
        
        sheet.update(f"B{i}:F{i}", [[
            enrichment["industry"],
            enrichment["size"],
            enrichment["location"],
            "",
            summary
        ]])
        print(f"Done: {company_name}")

if __name__ == "__main__":
    run()