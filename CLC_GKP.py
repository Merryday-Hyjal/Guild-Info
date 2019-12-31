import re
import csv
def format_unit(unit):
    if unit == 'M':
        return 1000000
    elif unit == 'K':
        return 1000
def regex_output(file_name):
    with open(file_name) as ff:
        record = ff.read()
    lines = re.findall(r'([^\.+|^\s]+).+?(\d+)(\S)', record, re.S|re.M)
    name_attr = []
    for name,output,unit in lines:
        output_data = int(output) * format_unit(unit) 
        name_attr.append({'name':name, 'data':output_data})
    return name_attr
def regex_disperse(file_name, scale):
    with open(file_name) as ff:
        record = ff.read()
    lines = re.findall(r'([^\.+|^\s]+).+?(\d+)', record, re.S|re.M)
    name_attr = {}
    for name,output in lines:
        output_data = int(output) * scale
        name_attr[name] = output_data
    return name_attr   
def merge_data(data_list, disperse_dct):
    for name_attrs in data_list:
        player = name_attrs['name']
        player_data = name_attrs['data']
        if player in disperse_data_dct:
            name_attrs['extra_data'] = disperse_data_dct.get(player) 
    return data_list

def GetDdScale(dps_list, dps_total_gold):
    total_data = 0
    # Calculate the sum of the total output
    for attrs in dps_list:
        player_data = attrs['data']
        if 'extra_data' in attrs:
            player_data = player_data + attrs['extra_data']
        total_data += player_data
    # Calculate the scale
    with open('Hyjal.csv','w', encoding= 'utf-8', newline = '') as ff:
        csv_write = csv.writer(ff)
        csv_head = ['Player', 'Output Data', 'Extra Data', 'Total Data/Base Data', 'Scale', 'Gold']
        csv_write.writerow(csv_head)
        gold = 0
        for attrs in dps_list:
            player = attrs['name']
            player_data = attrs['data']
            if 'extra_data' in attrs:
                extra_data = attrs['extra_data']
                player_total_data = player_data + extra_data
            else:
                extra_data = 0
                player_total_data = player_data
            player_scale = round(player_total_data/total_data, 6)
            player_gold = int(dps_total_gold * player_scale)
            csv_write.writerow([player, "{}K".format(player_data/1000), "{}K".format(extra_data/1000), "{}K".format(total_data/1000), player_scale, player_gold])
            gold += player_gold
    

def GetHeScale(healer_list, healer_total_gold):
    healer_num = len(healer_list)
    baseGold = int(healer_total_gold * 0.8)
    leftGold = int(healer_total_gold * 0.2)


    healer_data_list = []
    for attrs in healer_list:
        if 'extra_data' in attrs:
            player_data = attrs['data'] + attrs['extra_data']
        else:
            player_data = attrs['data']
        healer_data_list.append(player_data)
    base_healer_data = int(0.6 * max(healer_data_list))
    talent_healer_num = len([x for x in healer_data_list if x >= base_healer_data])
    extra_gold = int(leftGold / talent_healer_num)
    base_gold = int(baseGold / healer_num)
    with open('Hyjal.csv','a', encoding= 'utf-8', newline = '') as ff:
        csv_write = csv.writer(ff)
        csv_write.writerow(["****","****","****","****","****","****"])
        x = 0
        for attrs in healer_list:
            if 'extra_data' in attrs:
                player_data = attrs['data'] + attrs['extra_data']
            else:
                player_data = attrs['data']
                attrs['extra_data'] = 0
            if player_data >= base_healer_data:
                player_gold = base_gold + extra_gold
                scale = 'Tier 0'
            else:
                player_gold = base_gold
                scale = ''
            x += player_gold
            csv_write.writerow([attrs['name'], '{}K'.format(attrs['data']/1000), '{}K'.format(attrs['extra_data']/1000), \
                '{}K'.format(base_healer_data/1000), scale, player_gold])


        

if __name__ == '__main__':
    dps_total_gold = 8797
    healer_total_gold = 2778
    disperse_scale = 1000
    disperse_data_dct = regex_disperse('details_disperse_record.txt', disperse_scale)
    dps_data_list = merge_data(regex_output('details_dps_record.txt'),disperse_data_dct)
    healer_data_list = merge_data(regex_output('details_healer_record.txt'),disperse_data_dct)
    GetDdScale(dps_data_list, dps_total_gold)
    GetHeScale(healer_data_list, healer_total_gold)
