


def hot_vector_nth(func_nth: int, func_input_path: str, func_output_path: str):
    with open(func_input_path, "r") as rfp, open(func_output_path, "w") as wfp:
        while(1):
            raw_line = rfp.readline()
            if not raw_line:
                break
            list_raw_line = list( raw_line.split(",") )
            order = int( list_raw_line[ (-5) + (func_nth) ] )
            list_target = ["0" for i in range(6 - 1)]
            list_target.insert( order - 1, "1")
            list_write_line = list_raw_line[:-4] + list_target
            str_write_line = ",".join(list_write_line)
            wfp.write(str_write_line + "\n")
            wfp.flush()
            
def hot_vector_nth_list(func_nth: int, func_raw_list: list) -> list:
    list_raw_line = func_raw_list
    order = int( list_raw_line[ (-4) + (func_nth) ] )
    list_target = [int( 0 ) for i in range(6 - 1)]
    list_target.insert( order - 1, int( 1 ))
    list_write_line = list_raw_line[:-3] + list_target
    return list_write_line

if __name__ == "__main__":
    nth = int( 3 )
    startYYYYMMDD_endYYYYMMDD = "2018_2022-9" # "20200101_20220923" # .csv 拡張子は記入しない．
    
    input_path = "train-data/cat/" + startYYYYMMDD_endYYYYMMDD + ".csv"
    output_path = "train-data/hot-" + str(nth) + "/" + startYYYYMMDD_endYYYYMMDD + ".csv"
    hot_vector_nth(nth, input_path, output_path)