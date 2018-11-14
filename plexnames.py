import os
import re
import time
import pandas as pd

# CHANGE THIS TO FOLDER WITH MEDIA FOLDERS
main_path = 'I:\Media\Video\TV Shows'


def remove_underscores(s):
    """

    :param s:
    :return:
    """
    return s.replace('_', ' ')


def remove_periods(s):
    """

    :param s:
    :return:
    """
    return ' '.join(s.split('.')[:-1]) + '.' + s.split('.')[-1]


def remove_brackets(s):
    """

    :param s:
    :return:
    """
    return re.sub(r'\[.*?\]', '', s).strip()


def remove_parens(s):
    """

    :param s:
    :return:
    """
    s2 = re.sub(r'\(.*?\)', '', s).strip()
    return s2.replace(')', '')


def remove_braces(s):
    """

    :param s:
    :return:
    """
    return re.sub(r'\{.*?\}', '', s).strip()


def change_num_to_season_episode(s):
    """

    :param s:
    :return:
    """
    return ' '.join(['s01e' + x if x.replace('.', '', 1).isdigit() else x for x in s.split(' ')])


def remove_trailing_hyphens(s):
    """

    :param s:
    :return:
    """
    arr = s.split('.')
    try:
        if arr[0][-1] == '-':
            arr[0] = arr[0][:-1]
            return '.'.join(arr)
        else:
            return s
    except:
        return s


def remove_trailing_spaces(s):
    """

    :param s:
    :return:
    """
    return '.'.join([x.rstrip() for x in s.split('.')])


def remove_multi_spaces(s):
    """

    :param s:
    :return:
    """
    return re.sub(r'\s+\s+', ' ', s).strip()


def remove_hyphens(s):
    """

    :param s:
    :return:
    """
    return ' - '.join([x.replace('-', ' ') for x in s.split(' - ')])


def remove_quotes(s):
    """

    :param s:
    :return:
    """
    return s.replace("'", "")


def remove_special_phrases(s):
    """

    :param s:
    :return:
    """
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
    """

    :param s:
    :return:
    """
    try:
        x = re.findall(r'[\d]+x[\d]+', s)[0]
        season_ep = 's0' + x.split('x')[0] + 'e' + x.split('x')[1]

        return s.replace(x, season_ep)
    except:
        return s


def format_episodes(s):
    """

    :param s:
    :return:
    """
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
    """

    :param s:
    :return:
    """
    return ' '.join([x.capitalize() if x[:2] != 's0' else x for x in s.split(' ')])


def get_saved_folders(path):
    """

    :param path:
    :return:
    """
    with open(os.path.join(path, 'skips.txt'), 'r') as f:
        skip = f.readlines()
    return [x.strip() for x in skip]


def update_saved_folders(path, folder):
    """

    :param path:
    :param folder:
    :return:
    """
    with open(os.path.join(path, 'skips.txt'), 'a') as f:
        f.write(folder + '\n')


def create_dict(files):
    """

    :param files:
    :return:
    """
    dic = {}

    for file in files:
        dic.update({file: file})

    return dic


def preview_files(path):
    """

    :param dir:
    :return:
    """
    # Return a list of all files in dir
    file_list = os.listdir(path)

    # Print list of files
    print('Getting files in {} directory...\n'.format(dir))
    for file in file_list:
        print(file)

    dic = create_dict(file_list)

    for key in dic.keys():
        dic[key] = remove_periods(dic[key])
        dic[key] = remove_underscores(dic[key])
        dic[key] = remove_brackets(dic[key])
        dic[key] = remove_braces(dic[key])
        dic[key] = remove_parens(dic[key])
        dic[key] = remove_hypens(dic[key])
        dic[key] = change_num_to_season_episode(dic[key])
        dic[key] = remove_quotes(dic[key])
        dic[key] = convert_x_season_ep(dic[key])
        dic[key] = capilze_letters(dic[key])
        dic[key] = format_episodes(dic[key])
        dic[key] = remove_special_phrases(dic[key])
        dic[key] = remove_multi_spaces(dic[key])
        dic[key] = remove_trailing_spaces(dic[key])
        dic[key] = remove_trailing_hypens(dic[key])
        dic[key] = remove_trailing_spaces(dic[key])

    [print('{} : {}'.format(key, dic[key])) for key in dic.keys()]

    return dic


def update_files(path):
    """

    :param path:
    :return:
    """
    dic = preview_files(path)

    print('\nDo these conversions look good? (y/n): ')
    process = input()

    if process == 'y':
        print('\nProcessing...')

        for filename in os.listdir(path):
            try:
                os.rename(os.path.join(path, filename), os.path.join(path, dic[filename]))
            except:
                pass

        # Save dirty and clean names to CSV for later use in ML
        df = pd.DataFrame([[key, dic[key]] for key in dic.keys()])
        df.to_csv('samples.csv', mode='a', header=False)

        # Return a list of all files in path
        file_list = os.listdir(path)

        # Print list of files
        print('\nChecking files in {} directory...\n'.format(dir))

        for file in file_list:
            print(file)

    else:
        print('\nEnding Program...')


def update_preview_pass(path):
    """

    :param path:
    :return:
    """
    print('\nWould you like to update {}? (y/n/p)'.format(folder))
    update = str(input())

    if update == 'y':
        update_files(os.path.join(main_path, folder))
        update_saved_folders(main_path, folder)
    elif update == 'p':
        preview_files(os.path.join(main_path, folder))
        update_preview_pass(path)
    else:
        update_saved_folders(main_path, folder)
        pass


if __name__ == '__main__':
    # Get media directory from user
    print('Please enter folder: (ex. C:\TV Shows)')
    # main_path = str(input())

    # Get folders in media directory
    print('\nStarting at main path {}'.format(main_path))
    folders = [x for x in os.listdir(main_path) if os.path.isdir(os.path.join(main_path, x))]

    # Display folders in media directory
    print('\nHere is a list of all folders in {} folder...'.format(main_path))
    time.sleep(2)
    [print(folder) for folder in folders]

    # Get previously skipped and stored folders
    skips = get_saved_folders(main_path)

    # Go through Update/Preview/No prompt for each folder in media directory
    for folder in folders:
        # If folder is in skips.txt, then the folder is skipped
        if folder not in skips:
            update_preview_pass(folder)
        else:
            pass
