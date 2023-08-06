from os import environ


def correct_dir(user):
    if user == 'root':
        dir_user = '/root'
    else:
        dir_user = '/home/{}'.format(user)

    return dir_user


current_user = environ.get('USER')

project_base_dir = '/home/{}/.nonaybay'.format(current_user)
project_temp_dir = '{}/temp_files'.format(project_base_dir)
