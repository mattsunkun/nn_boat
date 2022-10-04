import requests
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import sys

from http_boat import create_data

list_first_argv = list( sys.argv[1] ) # yyyymmdd
list_second_argv = list( sys.argv[2] ) # yyyymmdd
list_third_argv = list( sys.argv[3] ) # rno,jcd,hd(DD)


target_path = "train-data/raw/http_" + sys.argv[1] + "_" + sys.argv[2] + ".csv"
error_path = "train-data/raw/error/error" + sys.argv[1] + "_" + sys.argv[2] + ".txt"
# warn_path = "http_csv/warn_path.txt"

d1_year = int( "".join( list_first_argv[0:4] ) )
d1_month = int( "".join( list_first_argv[4:6] ) )
d1_date = int( "".join( list_third_argv[4:6] ) )

d2_year = int( "".join( list_second_argv[0:4] ) )
d2_month = int( "".join( list_second_argv[4:6] ) )
d2_date = int( "".join( list_second_argv[6:8] ) )

d1 = date(d1_year, d1_month, d1_date)
d2 = date(d2_year, d2_month, d2_date)
# """requesting with parameters of {'rno': '10', 'jcd': '10', 'hd': '20220215'}"""
abort_begin_rno = str( "".join( list_third_argv[0:2] ) )
abort_begin_jcd = str( "".join( list_third_argv[2:4] ) )
# print(sys.argv)
# d1 = date(2022, 2, 4)
# d2 = date(2022, 2, 28)
before_startline_bool_jcd = True
before_startline_bool_rno = True

with open(target_path, "a") as fp, open(error_path, "a") as fp_error:
    for i in range((d2 - d1).days + 1): # date(hd)
        tmp_date = d1 + timedelta(i)
        str_tmp_date = tmp_date.strftime("%Y%m%d")
        for j in range(24): # race_area(jcd)
            str_tmp_area = str( j + 1 ).zfill(2)
            if before_startline_bool_jcd:
                if str_tmp_area == abort_begin_jcd:
                    before_startline_bool_jcd = False
                else:
                    continue
            for k in range(12): # nthrace(rno)
                str_tmp_nthrace = str( k + 1 ).zfill(2)
                if before_startline_bool_rno:
                    if str_tmp_nthrace == abort_begin_rno:
                        before_startline_bool_rno = False
                    else:
                        continue 
                request_parameters = {"rno": str_tmp_nthrace, "jcd": str_tmp_area, "hd": str_tmp_date}
                write_line = ""
                print(f"requesting with parameters of {request_parameters}\n")
                data = create_data(request_parameters, 3)
                if data == 0:
                    print(f"{request_parameters} does NOT exists\nsearch for the NEXT game")
                    fp_error.write(f"0_{request_parameters}\n")
                    fp_error.flush()
                    break # ここでは開催されていないと思われるから．
                elif ( type( data ) is int ) and ( 0 < data ):
                    print(f"{request_parameters} is NOT 6 players\n")
                    fp_error.write(f"{data}_{request_parameters}\n")
                    fp_error.flush()
                    continue
                elif ( type( data ) is int ) and ( data < 0 ):
                    print(f"{data}_{request_parameters}\n")
                    fp_error.write(f"{data}_{request_parameters}\n")
                    fp_error.flush()
                    continue
                for val in data.values():
                    if ( type( val ) is int ) or ( type( val ) is float ):
                        write_line += str( val ) + ","
                    else:
                        print(f"{data} has non-numeric number")
                        write_line += "!" + str( val ) + ","
                write_line += "\n"
                fp.write(write_line)
                fp.flush()
    

print("スクレイピング終わったぜXD")