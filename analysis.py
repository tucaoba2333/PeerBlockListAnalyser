import json, time
from tqdm import tqdm


def get_key_count(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)

    keys = sorted(data.keys(), key=int)

    return len(keys)


def get_group(file_name, number, keys):
    t1 = time.time()

    t2 = time.time()

    if number < len(keys):
        key = keys[number]
        group = {key: data[key]}
        t3 = time.time()
        return group


def list_all_peer_id(i_group_number, key_count):
    pbar = tqdm(total=key_count)  # 初始化进度条

    while i_group_number < key_count:
        current_dict = next(iter(get_group(filename, i_group_number, keys).values()))
        current_peer_id = current_dict.get("peer_id")
        if current_peer_id in peer_id_stat_dict:
            peer_id_stat_dict[current_peer_id] += 1
        else:
            peer_id_stat_dict[current_peer_id] = 1
        i_group_number += 1
        pbar.update(1)
    pbar.close()

    return peer_id_stat_dict


filename = 'temp.json'

i_group_number = 1

key_count = get_key_count('temp.json')

peer_id_stat_dict = {}

with open('temp.json', 'r') as file:
    data = json.load(file)

keys = sorted(data.keys(), key=int)

peer_id_stat = list_all_peer_id(i_group_number, key_count)
peer_id_stat['Unknown '] = peer_id_stat['']
del peer_id_stat['']
sorted_peer_id = sorted(peer_id_stat.items(), key=lambda x: x[1], reverse=True)
print(f"{key_count} lists of data checked:")
for key, value in sorted_peer_id:
    print(f"{key}: {value}({(value / key_count) * 100:.4f}%)")
