from socket import timeout
import requests
from bs4 import BeautifulSoup
import re
import sys

def weather_info(func_soup_beforeinfo_weather1):
    dict_weather_info = {}

    soup_weather1_bodyUnitLabelData = func_soup_beforeinfo_weather1.find_all( "span", class_="weather1_bodyUnitLabelData" )
    soup_weather1_bodyUnitLabelTitle = func_soup_beforeinfo_weather1.find_all( "span", class_="weather1_bodyUnitLabelTitle" )
    
    # air_temperature
    dict_weather_info["air_temperature"] = int( re.sub( r"\.|℃", "", soup_weather1_bodyUnitLabelData[0].get_text() ) )
    
    # weather
    weather_list = ["晴", "曇り", "雨", "雪", "霧"]
    dict_weather_info["weather"] = int( weather_list.index( soup_weather1_bodyUnitLabelTitle[1].get_text() ) )
    
    # wind_speed
    dict_weather_info["wind_speed"] = int( re.sub( r"\.|m", "", soup_weather1_bodyUnitLabelData[1].get_text() ) )
    
    # wind_direction
    dict_weather_info["wind_direction"] = int( re.search( r"\d", re.sub( r"weather1", "", str( func_soup_beforeinfo_weather1.find( "div", class_="weather1_bodyUnit is-windDirection" ) ) ) ).group() )
    
    # water_temperature
    dict_weather_info["water_temperature"] = int( re.sub( r"\.|℃", "", soup_weather1_bodyUnitLabelData[2].get_text() ) )
    
    # wave_height
    dict_weather_info["wave_height"] = int( re.sub( r"\.|cm", "", soup_weather1_bodyUnitLabelData[3].get_text() ) )
    
    return dict_weather_info


def player_info(func_soup_racelist_is_fs12, func_soup_beforeinfo, func_player_starting_point, func_player_number):
    # とりあえず一つだけ
    dict_player_info = {}
    soup_is_lineH2 = func_soup_racelist_is_fs12.find_all("td", class_="is-lineH2")
    soup_beforeinfo_is_p10_0 = func_soup_beforeinfo.find("tbody", class_="is-p10-0")
    soup_beforeinfo_is_fs12 = func_soup_beforeinfo.find_all("tbody", class_="is-fs12")[func_player_starting_point - 1]
    
    # rank
    rank_list = ["A1", "A2", "B1", "B2"]
    soup_racelist_is_fs12_is_fs11 = func_soup_racelist_is_fs12.find_all("div", class_="is-fs11")[0]
    dict_player_info[str(func_player_starting_point)+"_"+"rank"] = int( rank_list.index( soup_racelist_is_fs12_is_fs11.find("span").get_text() ) )

    # age 
    re_age = re.search(".{2}歳", func_soup_racelist_is_fs12.get_text())
    dict_player_info[str(func_player_starting_point)+"_"+"age"] = int( re.sub(r"歳", "", re_age.group()) )

    # weight*10
    re_weight = re.search(r"/.*kg", func_soup_racelist_is_fs12.get_text())
    dict_player_info[str(func_player_starting_point)+"_"+"weight*10"] = int( ( re.sub(r"/|\.|kg", "", re_weight.group() ) ) )

    # F
    re_F = re.search(r"F.", soup_is_lineH2[0].get_text() )
    dict_player_info[str(func_player_starting_point)+"_"+"F"] = int( re.sub( r"F", "", re_F.group()) )

    # L
    re_L = re.search(r"L.", soup_is_lineH2[0].get_text() )
    dict_player_info[str(func_player_starting_point)+"_"+"L"] = int( re.sub( r"L", "", re_L.group() ) )

    # avg_st*100
    re_avg_st = re.search( r"L.*", re.sub( r"\s", "", soup_is_lineH2[0].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"avg_st*100"] = int( re.sub( r"L.|\.", "", re_avg_st.group() ) )

    # jp_first
    re_jp_first = re.search( r".*\..*\n", re.sub( r" |\t|　", "", soup_is_lineH2[1].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"jp_first"] = int( re.sub( r"\s|\.", "", re_jp_first.group()) )

    # jp_second
    re_jp_second = re.search( r"\n.*\..*\n", re.sub( r" |\t|　", "", soup_is_lineH2[1].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"jp_second"] = int( re.sub( r"\s|\.", "", re_jp_second.group()) )

    # jp_third
    re_jp_third = re.search( r"\n.*\..*\n.*\..*", re.sub( r" |\t|　", "", soup_is_lineH2[1].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"jp_third"] = int( re.sub( r"\n.*\..*\n|\s|\.", "", re_jp_third.group()) )

    # local_first
    re_local_first = re.search( r".*\..*\n", re.sub( r" |\t|　", "", soup_is_lineH2[2].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"local_first"] = int( re.sub( r"\s|\.", "", re_local_first.group()) )

    # local_second
    re_local_second = re.search( r"\n.*\..*\n", re.sub( r" |\t|　", "", soup_is_lineH2[2].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"local_second"] = int( re.sub( r"\s|\.", "", re_local_second.group()) )

    # local_third
    re_local_third = re.search( r"\n.*\..*\n.*\..*", re.sub( r" |\t|　", "", soup_is_lineH2[2].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"local_third"] = int( re.sub( r"\n.*\..*\n|\s|\.", "", re_local_third.group()) )

    # motor_second
    re_motor_second = re.search( r"\n.*\..*\n", re.sub( r" |\t|　", "", soup_is_lineH2[3].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"motor_second"] = int( re.sub( r"\s|\.", "", re_motor_second.group()) )
    
    # motor_third
    re_motor_third = re.search( r"\n.*\..*\n.*\..*", re.sub( r" |\t|　", "", soup_is_lineH2[3].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"motor_third"] = int( re.sub( r"\n.*\..*\n|\s|\.", "", re_motor_third.group()) )

    # boat_second
    re_boat_second = re.search( r"\n.*\..*\n", re.sub( r" |\t|　", "", soup_is_lineH2[4].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"boat_second"] = int( re.sub( r"\s|\.", "", re_boat_second.group()) )

    # boat_third
    re_boat_third = re.search( r"\n.*\..*\n.*\..*", re.sub( r" |\t|　", "", soup_is_lineH2[4].get_text() ) )
    dict_player_info[str(func_player_starting_point)+"_"+"boat_third"] = int( re.sub( r"\n.*\..*\n|\s|\.", "", re_boat_third.group()) )
    
    
    # display_time
    soup_4 = soup_beforeinfo_is_fs12.find_all("td", rowspan="4")
    dict_player_info[str(func_player_starting_point)+"_"+"display_time"] = int( re.sub( r"\.", "", soup_4[3].get_text() ) )
    
    # tilt
    soup_4 = soup_beforeinfo_is_fs12.find_all("td", rowspan="4")
    dict_player_info[str(func_player_starting_point)+"_"+"tilt"] = int( re.sub( r"\.", "", soup_4[4].get_text() ) )
    
    # steal_place, fsl_timing, and display_start_timing
    list_raw_beta_place = soup_beforeinfo_is_p10_0.find_all("tr")
    end_number = func_player_number
    for i in range(end_number):
        raw_display_info = re.sub(r"\s", ",", list_raw_beta_place[i].get_text())
        list_display_info = [j for j in raw_display_info.split(",") if j != ""]
        # スタートの差が1秒以上のときは考慮していない．
        if ( int( list_display_info[0] ) == func_player_starting_point ):
            dict_player_info[str(func_player_starting_point)+"_"+"steal_place"] = int( i + 1 )
            if re.search( r"F", list_display_info[1] ):
                int_fsl = -1
            elif re.search( r"L", list_display_info[1] ):
                int_fsl = 1
            else:
                int_fsl = 0
            dict_player_info[str(func_player_starting_point)+"_"+"fsl_timing"] = int_fsl
            if re.sub( r"F|L|\.", "", list_display_info[1] ) == "":
                dict_player_info[str(func_player_starting_point)+"_"+"display_start_timing"] = 100
            else:
                dict_player_info[str(func_player_starting_point)+"_"+"display_start_timing"] = int( re.sub( r"F|L|\.", "", list_display_info[1] ) )
    
    return dict_player_info

def player_order(func_soup_raceresult, func_order_amt, func_player_number):
    list_player_order = [ int( re.sub( r"is-fs14 is-fBold is-boatColor", "", raw_order) ) for raw_order in re.findall( r"is-fs14 is-fBold is-boatColor.", str( func_soup_raceresult ) ) ]
    dict_player_order = {}
    end_number = min( func_order_amt, func_player_number )
    for i in range(end_number):
        dict_player_order["order_" + str( i + 1 )] = list_player_order[i]
    return dict_player_order

def create_data(func_parameters, func_order_amt):
    parameters = func_parameters
    url_racelist = "get_info/padding_html/racelist.html"
    url_beforeinfo = "get_info/padding_html/beforeinfo.html"
    url_raceresult = "get_info/padding_html/raceresult.html"
    response_timeout = (3.0, 7.5)

    soup_racelist = BeautifulSoup(open("get_info/padding_html/racelist.html", encoding="utf-8"), "html.parser")
    soup_racelist_heading1_mainLabel = soup_racelist.find( "span", class_="heading1_mainLabel" )
    if soup_racelist_heading1_mainLabel != None: # error_code=0:そもそもデータが存在しない．
        return 0 # {}
    if len( re.findall(r"-", soup_racelist.get_text() ) ) >= 2:
        return -2 # error_code=-2:データに"-"が存在する．
    # str_soup_racelist = re.sub(r"-", "0", str( soup_racelist ) )
    # soup_racelist = BeautifulSoup(str_soup_racelist, "html.parser")

    soup_beforeinfo = BeautifulSoup(open("get_info/padding_html/beforeinfo.html", encoding="utf-8"), "html.parser")
    soup_beforeinfo_is_fs12_is_miss = soup_beforeinfo.find_all("tbody", class_="is-fs12 is-miss")
    soup_beforeinfo_weather1_bodyUnitLabelData = soup_beforeinfo.find_all("span", class_="weather1_bodyUnitLabelData")
    player_number = 6 - len( soup_beforeinfo_is_fs12_is_miss )
    if player_number != 6:
        return player_number # error_code=1~6:プレイヤーが一人足りない．
    for i in range(4): # 四つ情報があるから．
        tmp_str = str( soup_beforeinfo_weather1_bodyUnitLabelData[i].get_text() )
        if tmp_str == "\xa0":
            return -3 # error_code=-3:天気データが存在しない．
    
    soup_beforeinfo_table1_boatImage1Number = soup_beforeinfo.find_all("span", class_="table1_boatImage1Number")
    soup_beforeinfo_table1_boatImage1Time = soup_beforeinfo.find_all("span", class_="table1_boatImage1Time")
    if len( soup_beforeinfo_table1_boatImage1Number ) == 0:
        return -4 # error_code=-4:
    if len( soup_beforeinfo_table1_boatImage1Number ) < 6:
        return 1
    for i in range(6): # 上のところで6人未満は外してあるから
        if str( soup_beforeinfo_table1_boatImage1Number[i].get_text() ).isnumeric() == False or re.search( r"\.", str( soup_beforeinfo_table1_boatImage1Time[i].get_text() ) ) == None:
            return -5 # error_code=-5:
        
    soup_raceresult = BeautifulSoup(open("get_info/padding_html/raceresult.html", encoding="utf-8"), "html.parser")
    a = soup_raceresult.find_all("div", class_="table1")
    if len( soup_raceresult.find_all("div", class_="table1") ) < 2:
        return -6 # error_code=-6:レース中止
    
    soup_racelist_is_fs12 = soup_racelist.find_all("tbody", class_="is-fs12")
    soup_beforeinfo_weather1 = soup_beforeinfo.find("div", class_="weather1" )

    dict_target = weather_info(soup_beforeinfo_weather1)
    for i in range(player_number):
        dict_append = player_info(soup_racelist_is_fs12[i], soup_beforeinfo, i + 1, player_number)
        dict_target.update( dict_append )

    dict_target.update( player_order(soup_raceresult, func_order_amt, player_number) ) 

    return dict_target

def get_html(func_parameters: dict):
    url_racelist = "https://www.boatrace.jp/owpc/pc/race/racelist"
    url_beforeinfo = "https://www.boatrace.jp/owpc/pc/race/beforeinfo"
    url_raceresult = "https://www.boatrace.jp/owpc/pc/race/raceresult"
    with open("get_info/padding_html/racelist.html", "w") as fp:    
        response_racelist = requests.get(url_racelist, func_parameters)
        fp.write(response_racelist.text)
    with open("get_info/padding_html/beforeinfo.html", "w") as fp:
        response_beforeinfo = requests.get(url_beforeinfo, func_parameters)
        fp.write(response_beforeinfo.text)
    with open("get_info/padding_html/raceresult.html", "w") as fp:
        response_raceresult = requests.get(url_raceresult, func_parameters)
        fp.write(response_raceresult.text)

if __name__ == "__main__":
    params = {'rno': '01', 'jcd': '01', 'hd': '20221001'}
    get_html(params)
    print( create_data(params, 3) )