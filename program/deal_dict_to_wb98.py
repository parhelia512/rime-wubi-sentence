import os

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def update_missing_encodings(file_path, write_file_path, dict_data):
    file_content = read_file(file_path)
    lines = file_content.split('\n')
    updated_content = ''

    char_map = {}
    for line in lines:
        if '\t' not in line or line.startswith("#"):
            updated_content += line + '\n'
            continue
        
        char_list = line.split('\t')[0]
        if char_list in char_map:
            continue

        lack_flag = False
        for char in char_list:
            if char not in dict_data:
                lack_flag = True
                continue
        if lack_flag:
            continue

        word_encode_list = []
        for char in char_list:
            if char not in dict_data:
                print("缺失"+char)
                continue
            dict_encode_list = dict_data[char]
            dict_encode = ';'.join(dict_encode_list)
            word_encode_list.append(dict_encode)

        word_encode = ' '.join(word_encode_list)
        if char_list in word_freq:
            freq = word_freq[char_list]
        else:
            freq = 0
        updated_line = f"{char_list}\t{word_encode}\t{freq}"
        updated_content += updated_line + '\n'
        char_map[char_list] = ''

    write_file(write_file_path, updated_content)

freq_file = open(r"D:\vscode\rime-frost\others\知频.txt", 'r', encoding='utf-8')
word_freq = {}
for line in freq_file:
    line = line.strip()
    params = line.split("\t")
    word = params[0]
    freq = int(params[1])

    if word in word_freq:
        word_freq[word] += freq
    else:
        word_freq[word] = freq

dict_data = {}
wb_98_dict_list = ['wubi98.dict.yaml']
for wb_98_dict in wb_98_dict_list:
    with open('program/'+wb_98_dict, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            if "\t" in line and not line.startswith("#"):
                
                params = line.strip().split('\t')
                if wb_98_dict == 'wubi98.dict.yaml' and len(params) != 4:
                    continue
                character = params[0]
                if len(character) !=1:
                    continue
                
                encoding = params[3]

                encode_left = encoding[0:2]
                encode_right = encoding[2:]
                if len(encode_right) == 1:
                    encode_right = encode_right + '0'

                encoding = encode_left + ',' + encode_right
                
                if character not in dict_data:
                    dict_data[character] = [encoding]
                else:
                    if encoding not in dict_data[character]:
                        dict_data[character].append(encoding)

print(dict_data['一'])
print(dict_data['不'])
print(dict_data['的'])

file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
for file_name in file_list:
    cn_dicts_path = r"D:\vscode\rime-frost\cn_dicts"
    yaml_file_path = os.path.join(cn_dicts_path, file_name)
    write_file_path = os.path.join('cn_dicts_wb98', file_name)

    print(yaml_file_path)
    update_missing_encodings(yaml_file_path, write_file_path, dict_data)
