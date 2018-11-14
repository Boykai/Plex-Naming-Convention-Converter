import os
import re
import time

#CHANGE THIS TO FOLDER WITH MEDIA FOLDERS
main_path = 'I:\Media\Video\TV Shows'


def get_saved_folders(dir):
    with open(os.path.join(dir, 'skips.txt'), 'r') as f:
        skip = f.readlines()
    return [x.strip() for x in skip]


def update_saved_folders(dir, folder):
    with open(os.path.join(dir, 'skips.txt'), 'a') as f:
        f.write(folder + '\n')


def create_dict(files):
    dict = {}

    for file in files:
        dict.update({file: file})

    return dict


def remove_underscores(s):
    return s.replace('_', ' ')


def remove_periods(s):
    return (' ').join(s.split('.')[:-1]) + '.' + s.split('.')[-1]


def remove_brackets(s):
    return re.sub(r'\[.*?\]', '', s).strip()


def remove_parens(s):
    s2 = re.sub(r'\(.*?\)', '', s).strip()
    return s2.replace(')', '')


def remove_braces(s):
    return re.sub(r'\{.*?\}', '', s).strip()


def change_num_to_season_episode(s):
    return (' ').join(['s01e' + x if x.replace('.', '', 1).isdigit() else x for x in s.split(' ')])


def remove_trailing_hypens(s):
    arr = s.split('.')
    try:
        if arr[0][-1] == '-':
            arr[0] = arr[0][:-1]
            return ('.').join(arr)
        else:
            return s
    except:
        return s


def remove_trailing_spaces(s):
    return ('.').join([x.rstrip() for x in s.split('.')])


def remove_multi_spaces(s):
    return re.sub(r'\s+\s+', ' ', s).strip()


def remove_hypens(s):
    return (' - ').join([x.replace('-', ' ') for x in s.split(' - ')])


def remove_quotes(s):
    return s.replace("'", "")


def remove_special_phrases(s):
    special_phrases = ['480p',
                       '720p',
                       '1080p',
                       'H.264',
                       'H265',
                       'Ac3',
                       'Aac2',
                       'Dl',
                       'Sa89',
                       'Web',
                       'Amzn',
                       'D1',
                       'Dd',
                       'Dd5',
                       'Dvdrip',
                       'Dvdrip.xvid',
                       'Ep',
                       'Episode',
                       'Xvid',
                       'Ffndvd',
                       'X264',
                       'X265',
                       'Trollhd',
                       'B3 bomber',
                       'Rs2',
                       'Vk007',
                       'Bluray',
                       'Bluray+web',
                       'BlueRay.x264',
                       'D1x265',
                       'Hevc',
                       'D3g',
                       'Ntb',
                       'Shortbrehd',
                       'Deimos',
                       'D3fil3r',
                       'Dhd',
                       'Ositv',
                       'D3g']

    for phrase in special_phrases:
        pattern = r'\s+' + re.escape(phrase) + r'\s+'
        s = re.sub(pattern, ' ', s).strip()

    return s


def convert_x_season_ep(s):
    try:
        x = re.findall(r'[\d]+x[\d]+', s)[0]
        season_ep = 's0' + x.split('x')[0] + 'e' + x.split('x')[1]

        return s.replace(x, season_ep)
    except:
        return s


def format_episodes(s):
    if re.findall(r'[^-]\s+s01\w+\s+[^-]', s):
        old = re.findall(r'\s+s01\w+\s+', s)[0]
        new = ' -' + old + '- '
        return re.sub(r'\s+s01\w+\s+', new, s).strip()
    elif re.findall(r'[^-]\s+s01\w+\s+-', s):
        old = re.findall(r'\s+s01\w+\s+', s)[0]
        new = ' -' + old
        return re.sub(r'\s+s01\w+\s+', new, s).strip()
    elif re.findall(r'-\s+s01\w+\s+[^-]', s):
        old = re.findall(r'\s+s01\w+\s+', s)[0]
        new = old + '- '
        return re.sub(r'\s+s01\w+\s+', new, s).strip()
    else:
        return s


def capilze_letters(s):
    return (' ').join([x.capitalize() if x[:2] != 's0' else x for x in s.split(' ')])


def update_files(dir):
    dict = preview_files(dir)

    print('\nDo these conversions look good? (y/n): ')
    process = input()

    if process == 'y':
        print('\nProcessing...')

        for filename in os.listdir(dir):
            try:
                os.rename(os.path.join(dir, filename), os.path.join(dir, dict[filename]))
            except:
                pass

        # Return a list of all files in dir
        file_list = os.listdir(dir)

        # Print list of files
        print('\nChecking files in {} directory...\n'.format(dir))

        for file in file_list:
            print(file)

    else:
        print('\nEnding Program...')

def preview_files(dir):
    # Return a list of all files in dir
    file_list = os.listdir(dir)

    # Print list of files
    print('Getting files in {} directory...\n'.format(dir))
    for file in file_list:
        print(file)

    dict = create_dict(file_list)

    for key in dict.keys():
        dict[key] = remove_periods(dict[key])
        dict[key] = remove_underscores(dict[key])
        dict[key] = remove_brackets(dict[key])
        dict[key] = remove_braces(dict[key])
        dict[key] = remove_parens(dict[key])
        dict[key] = remove_hypens(dict[key])
        dict[key] = change_num_to_season_episode(dict[key])

        dict[key] = remove_quotes(dict[key])
        dict[key] = convert_x_season_ep(dict[key])
        dict[key] = capilze_letters(dict[key])
        dict[key] = format_episodes(dict[key])
        dict[key] = remove_special_phrases(dict[key])
        dict[key] = remove_multi_spaces(dict[key])
        dict[key] = remove_trailing_spaces(dict[key])
        dict[key] = remove_trailing_hypens(dict[key])
        dict[key] = remove_trailing_spaces(dict[key])

    [print('{} : {}'.format(key, dict[key])) for key in dict.keys()]

    return dict

def update_preview_pass(dir):
    print('\nWould you like to update {}? (y/n/p)'.format(folder))
    update = str(input())

    if update == 'y':
        update_files(os.path.join(main_path, folder))
        update_saved_folders(main_path, folder)
    elif update == 'p':
        preview_files(os.path.join(main_path, folder))
        update_preview_pass(dir)
    else:
        update_saved_folders(main_path, folder)
        pass

# START
print('Please enter folder: (ex. C:\TV Shows)')
#main_path = str(input())
print('\nStarting at main path {}'.format(main_path))
folders = [x for x in os.listdir(main_path) if os.path.isdir(os.path.join(main_path, x))]

print('\nHere is a list of all folders in {} folder...'.format(main_path))
time.sleep(2)
for folder in folders:
    print(folder)

skips = get_saved_folders(main_path)

for folder in folders:
    if folder not in skips:
        update_preview_pass(folder)
    else:
        pass