import os
from collections import defaultdict

result_list = defaultdict(list)
list_pointer = 0



def log_request(path, complete_flag):
    global list_pointer


    box = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:  # open in readonly mode
            i = 0
            j = 0
            local_result_list = []
            searchlines = f.readlines()
            last_line = searchlines[-1]
            image_path = searchlines[0].split(':')[0]
            print(image_path)

            if searchlines[1] != 0:
                predictions_num = int(searchlines[1]) - 1
                for i in range(predictions_num):
                    box = searchlines[1 + 1 + i].split(',')
                    i += 1
                for j in range(predictions_num):
                    local_result_list.append(str(searchlines[2 + i + 1 + j].split(':')[0]))
                    if complete_flag:
                        if local_result_list[j] == 'fedex':
                            result_list[image_path].append("fedex")
                        elif local_result_list[j] == 'dhl':
                            result_list[image_path].append("dhl")
                        elif local_result_list[j] == 'ups':
                            result_list[image_path].append("ups")
                        elif local_result_list[j] == 'food delivery':
                            result_list[image_path].append("food")
                        list_pointer += 1
                    else:

                        print(box)
                    if searchlines[2 + i + 1 + j] is last_line:
                        break
                    j += 1

        list_pointer += 1
        print(result_list)

            
    f.close()



log_request("/home/pi/PiImage/OutTxt",1)