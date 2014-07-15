from datetime import timedelta
from collections import OrderedDict
import who_did_i_see_question as wdisq
import json
from bson import json_util

#http://raman.imm.dtu.dk:8086/magda/sensible-dtu/connectors/connector_answer/v1/how_many_people_did_i_see_question/how_many_people_did_i_see_answer/?bearer_token=c9af1c97a08500ba33635cf2568ce1&username=331f9e3859ae7f3c457498d423d29d&type=week
#http://raman.imm.dtu.dk:8086/magda/sensible-dtu/connectors/connector_answer/v1/how_many_people_did_i_see_question/how_many_people_did_i_see_answer/?bearer_token=f3b4144993be90bd3e701c716dd1de&time=today

NAME = "how_many_people_did_i_see_question"

def run():
    """This question does not populate the database since it uses data calculated by who_did_i_see_question"""
    pass

def how_many_people_did_i_see_answer(request, user, scopes, users_to_return, user_roles, own_data):
    """The response for how_many_people_did_i_see request. Returns the number of people seen within a given time"""
    [collection, user, from_date, end_date, output_type] = wdisq.prepare_to_answer(request, users_to_return, user_roles, user)    
    result = {}
    for single_user in user:
        users_list = wdisq.get_users_list(collection, single_user, from_date, end_date)
        result[single_user] = _get_users_number(users_list, from_date, end_date)
    return json.dumps(result, default=json_util.default)

def _get_users_number(users_list, from_date, end_date):
    """Returns the number of poeple seen computer either hourly or daily (depending on the time range)"""
    if(end_date - from_date <= timedelta(days = 1)): # then we have to compute it hourly
        return _get_users_number_hourly(users_list, from_date, end_date)
    else: # we compute it daily
        return _get_users_number_daily(users_list, from_date, end_date)

def _get_users_number_daily(users_list, from_date, end_date):
    """Returns the number of people seen computed daily"""
    result = OrderedDict()
    start_range = from_date
    end_range = start_range + timedelta(days = 1)
    i = 0
    while(start_range < end_date):
        count = 0
        while(users_list[i]['timestamp'] > start_range and users_list[i]['timestamp'] < end_range):
            count += 1
            i += 1
        if(count > 0):
            result[str(start_range)] = count
        start_range = end_range
        end_range = start_range + timedelta(days = 1)
    return result

def _get_users_number_hourly(users_list, from_date, end_date):
    """Returns the number of people seen computed hourly"""
    result = OrderedDict()
    start_range = from_date
    end_range = start_range + timedelta(hours = 1)
    i = 0
    while(start_range < end_date):
        count = 0
        while(users_list[i]['timestamp'] > start_range and users_list[i]['timestamp'] < end_range):
            count += 1
            i += 1
        if(count > 0):
            result[str(start_range)] = count
        start_range = end_range
        end_range = start_range + timedelta(hours = 1)
    return result