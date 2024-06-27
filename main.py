import os, time, tempfile, re, openpyxl, json
import pandas as pd
from tqdm import tqdm

def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize, 2)
def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)


def analyze_log_folder(folder_path):
    global total_lines
    total_lines = 0
    anal_start_time = time.time()
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            start_time = time.time()
            file_path = os.path.join(folder_path, file_name)
            lines_in_file = count_lines_in_file(file_path)
            total_lines += lines_in_file
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            print(f"{file_name} has: {lines_in_file} lines, this step took {elapsed_time} ms.")
    end_time = time.time()
    anal_time = (end_time - anal_start_time) * 1000
    print(f"Total lines in all log files: {total_lines}, this step took {anal_time} ms")


def merge_log_files(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')
    print(f"All log files have been merged into {output_file}")

def analyze_log_info(Current_line_Info):
    pattern = re.compile(r'\[(.*?)]\[(.*?)] (.*?):(.*?) "(.*?)"\|"(.*?)" \(TorrentInfoHash: (.*?)\)')

    match = pattern.match(Current_line_Info)

    if match and "CheckPeer_AddBlockPeer" in Current_line_Info:
        log_info = {
            'timestamp': match.group(1),
            'event': match.group(2),
            'ip': match.group(3),
            'port': match.group(4),
            'peer_id': match.group(5),
            'client': match.group(6),
            'torrent_info_hash': match.group(7)
        }
        return log_info
    else:
        return None


#----------------------------------------------#

log_folder_path = "./logs"
print(analyze_log_folder(log_folder_path))

with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_file:
    temp_file_path = temp_file.name
merge_log_files(log_folder_path, temp_file_path)
print(f"Temporary merged log file created at: {temp_file_path}")

open("temp.json", 'w', encoding='utf-8')
with open(temp_file_path, 'r', encoding='utf-8') as input_file:
    with open("./temp.json", 'w', encoding='utf-8') as json_file:
        data_list = []
        i = 0
        for line in tqdm(input_file, total=total_lines, unit="lines", desc="Processing lines"):
            analyzed_data = analyze_log_info(line)
            if analyzed_data is None:
                continue
            data_list.append((i, analyzed_data))
            i += 1

        json_data = {str(index): data for index, data in data_list}
        json.dump(json_data, json_file, indent=2)


TempFileSize = get_FileSize(temp_file_path)



print("Temp.json successfully generated.")
print(f"Here is where the temp file just generated:{temp_file_path}, size is:{TempFileSize}MiB. It will be removed.")
os.remove(temp_file_path)
pdObj = pd.read_json('temp.json', orient='index')
pdObj.to_csv('Export.csv', index=False)
print("Export.csv has been generated.")
print("Attention! Every time generate Temp.json will over write the old one, do backup before run this script!!!!!!")
print("Attention! Every time generate Temp.json will over write the old one, do backup before run this script!!!!!!")
print("Attention! Every time generate Temp.json will over write the old one, do backup before run this script!!!!!!")