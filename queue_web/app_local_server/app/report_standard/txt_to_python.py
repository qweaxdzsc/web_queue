# Organize txt data to a matrix


def process_data(txt_name):
    def txt_in(filename):
        """process txt file into readable list"""
        f = open(filename, encoding='utf-8')    # open
        txt = f.readlines()                     # read
        row_count = len(txt)
        for i in range(row_count):
            txt[i] = txt[i].strip()             # strip blanks before and after
            txt[i] = txt[i].split()             # form lines into list

        return txt

    def partitioning(txt, type_name):
        """
        what is it:
        1. Partitioning txt and extract 4 types:
        volume, static_pressure, total_pressure, uniformity
        2. then split them into two list: string and data
        how to realize:
        1. Traversal all line to locate type name
        2. under type name, find two divide_line "----" to isolate needed part
        3. make it two list: string and data
        """
        divide_index = []
        txt_string = []
        txt_data = []

        for line in txt:
            if type_name in line:               # find type
                title_index = txt.index(line)
                txt_rest = txt[title_index:]    # new txt start from title line

                for line in txt_rest:
                    if '--' in line[0]:                                    # use "---" to determine data location
                        divide_index.append(txt_rest.index(line))          # get index of top and bottom

                    if len(divide_index) > 1:                                        # data isolate success
                        txt_target = txt_rest[divide_index[0]+1:divide_index[1]]     # isolate type
                        txt_string = []
                        txt_data = []
                        for i in txt_target:
                            txt_string.append(i[0])
                            txt_data.append(float(i[1]))
                        break
                break
        return txt_string, txt_data

    def unit_convert(data_list):
        """ transfer unit from m3/s to L/s"""
        return [data*1000 for data in data_list]

    def total_volume(data_list):
        """eliminate negative number, then sum it to total volume"""
        total_volume = sum([max(data, 0) for data in data_list])
        return total_volume

    def decimal(raw_data, number):
        """function to round data without round()
         because round() doesn't leave 0 and not precise"""
        if number == 1:
            return ['%.1f' % i for i in raw_data]
        elif number == 2:
            return ['%.2f' % i for i in raw_data]
        elif number == 3:
            return ['%.3f' % i for i in raw_data]

    def percent_convert(raw_data, total_volume):
        """make data array percentage of total volume"""
        percent_array = ['{:.1%}'.format(data/total_volume) for data in raw_data]
        return percent_array

    def find_moment(txt):
        exist = False
        for line in txt:                                    # find moment
            if 'Moment' and 'Axis' in line:                 # get that line
                part_index = txt.index(line)
                exist = True
                break
        if exist:  # check existence
            moment_raw = txt[part_index + 3][3]             # locate torque value
            try:
                moment = '%.3f' % abs(float(moment_raw))    # in case wrong location
            except Exception as e:
                error = "Wrong, Error:%s" % e
                return error
            else:
                return moment
        else:
            return 'not-exist'

    # main process start
    txt = txt_in(txt_name)                                     # read txt in

    # Partitioning txt to raw data
    volume_string, volume_data = partitioning(txt, 'Volumetric')
    sp_string, sp_data = partitioning(txt, 'Static')
    tp_string, tp_data = partitioning(txt, 'Total')
    uni_string, uni_data = partitioning(txt, 'Uniformity')
    fan_moment = [find_moment(txt)]

    """if exist, convert L/S, calculate total number, create percent array"""
    if volume_string:                                          # determine volume part existence
        l_p_s = unit_convert(volume_data)                      # convert to L/S
        total_volume = total_volume(l_p_s)                     # get total volume
        l_p_s.append(total_volume)                             # add total volume to data array
        data_round = decimal(l_p_s, 1)                         # round data to 1 decimal place
        percent_array = percent_convert(l_p_s, total_volume)   # get percentage_array
        volume_string.append('Total')                          # add name "total" to string array
    else:
        # if not exist
        volume_string, data_round, percent_array = ['not-exist'], ['not-exist'], ['not-exist']

    if sp_string:
        sp_data_de = decimal(sp_data, 1)
    else:
        sp_data_de = ['not-exist']

    if tp_string:
        tp_data_de = decimal(tp_data, 1)
    else:
        tp_data_de = ['not-exist']

    if uni_string:
        uni_data_de = decimal(uni_data, 3)
    else:
        uni_data_de = ['not-exist']

    # save all string and data into list(matrix)
    matrix = (
                volume_string,
                data_round,
                percent_array,
                sp_string,
                sp_data_de,
                tp_string,
                tp_data_de,
                uni_string,
                uni_data_de,
                fan_moment
             )
    print(matrix)
    return matrix


