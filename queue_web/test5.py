# from app_queue import models


def key_exist(string_key, condition_dict):
    try:
        real_key = int(string_key)
    except Exception as e:
        return False
    else:
        if real_key in condition_dict.keys():
            return condition_dict[real_key]
        else:
            return False


def check_keyword(keyword, condition_dict):
    error_info = ''
    keyword_dict = {}
    filter_dict = {}
    if keyword:
        keyword_list = keyword.split(',')
    else:
        return filter_dict, error_info

    for i in keyword_list:
        split = i.split(':')
        if len(split) == 2:
            keyword_dict[split[0]] = split[1]
            string_key = split[0]
            value = split[1]
            split_key = string_key.split('__')
            real_key = split_key[0]
            field = key_exist(real_key, condition_dict)
            if (len(split_key) == 2) and field:
                filter_method = split_key[1]
                field = '%s__%s' % (condition_dict[int(real_key)], filter_method)
                filter_dict[field] = value
            elif len(split_key) == 1 and field:
                field = '%s__icontains' % field
                filter_dict[field] = value
            else:
                error_info = 'key error, has incorrect key'
                break
        else:
            error_info = 'misuse of "," or ":"'
            break

    return filter_dict, error_info


condition_dict = {
    0: None,
    1: 'order_id',
    2: 'account_email',
    3: 'mission_name',
    4: 'sender_address',
    5: 'register_time',
    6: 'start_time',
    7: 'used_time',
    8: 'id',
    9: 'mission_data',
}
keyword = ''

field_dict, error_info = check_keyword(keyword, condition_dict)

if error_info:
    print(error_info)
else:
    print(field_dict)

