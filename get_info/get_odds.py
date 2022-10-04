from urllib import response
import requests
from bs4 import BeautifulSoup
import re

request_parameters = {"rno": "01", "jcd": "01", "hd": "20220920"}
url_odds = "https://www.boatrace.jp/owpc/pc/race/odds"

def tf(func_request_parameters: str) -> list:
    # getする
    response_oddstf = requests.get(url_odds+"tf", func_request_parameters)
    soup_oddstf = BeautifulSoup(response_oddstf.text, "html.parser")
    soup_oddstf_oddsPoint = soup_oddstf.find_all("td", class_="oddsPoint")
    # list化する
    list_odds_single = [ int( re.sub(r"\.", "", soup_oddstf_oddsPoint[i].text ) ) / 10 for i in range(6)]
    raw_list_odds_multiple = [soup_oddstf_oddsPoint[i + 6].text for i in range(6)]
    return list_odds_single, raw_list_odds_multiple

def three_t(func_request_parameters: str) -> list:
    # get する
    response_odds3t = requests.get(url_odds+"3t", func_request_parameters)
    soup_odds3t = BeautifulSoup(response_odds3t.text, "html.parser")
    soup_odds3t_oddsPoint = soup_odds3t.find_all("td", class_="oddsPoint")
    # listする
    list_odds_3_single = []
    for i in range(20):
        tmp_list_odds_3_single = []
        for j in range(6):
            if re.search("\.", soup_odds3t_oddsPoint[ ( i*6 ) + j ].text):
                tmp_list_odds_3_single.append( int( re.sub( "\.", "", soup_odds3t_oddsPoint[i].text ) ) / 10 )
            else:
                tmp_list_odds_3_single.append( int( soup_odds3t_oddsPoint[ ( i*6 ) + j ].text ) )
        list_odds_3_single.append(tmp_list_odds_3_single)
    return list_odds_3_single
    
    
if __name__ == "__main__":
    ls = three_t(request_parameters)
    print(ls)