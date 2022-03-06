from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Form
from fastapi.responses import RedirectResponse
import requests

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

templates = Jinja2Templates(directory="templates")


@app.get("/")
def main(request: Request):
    '''
    Create Stock dashboard for analysis
    '''
    ticker = request.query_params.get('search', False)
    if ticker == False:
        ticker = 'TCS'

    base_url = f"https://stockanalysisapi-xyy5p4vcpa-ew.a.run.app"

    stock_url = f"{base_url}/stock"
    params={"ticker":ticker}
    response = requests.get(stock_url,params=params)
    stock = response.json()
    stock_id = stock['ID']

    stock_list_url = f"{base_url}/stocklist"
    response = requests.get(stock_list_url)
    stock_list = response.json()


    api_endpoints = {
        "technical": "/technical",
        "news": "/newslist",
        "twitter": "/twitter",
        "recommendation": "/recommendation"
    }

    fundamental_data =[1,2,3]
    data_api = {"technical":[],"news":[],"twitter":[],"recommendation":[]}
    for key,post_url in api_endpoints.items():
        new_url = f"{base_url}{post_url}"
        params={"ticker":ticker}
        response = requests.get(new_url,params=params)
        data_api[key] = response.json()

    return templates.TemplateResponse(
        "home.html", {
            "request": request,
            "stock": stock,
            "stock_list": stock_list,
            "news_list": data_api['news'],
            "recommendation_list": data_api['recommendation'],
            "technical_data": data_api['technical'],
            "list_revenue_chart": fundamental_data
        })
