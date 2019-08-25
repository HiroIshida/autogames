import autogames
import glob
import json
import os
import pkg_resources

__version__ = pkg_resources.get_distribution(
    'autogames').version


def get_game_titles():
    game_titles = []
    package_path = autogames.__file__
    games_path = os.path.join(
        os.path.dirname(package_path), 'server', 'games') + '/*'
    file_names = glob.glob(games_path)
    for file_name in file_names:
        file_name = os.path.basename(file_name)
        # pick up only python files
        if file_name.endswith('.py') and \
           file_name != '__init__.py' and \
                        file_name != 'game_manager.py':
            game_titles.append(os.path.splitext(file_name)[0])
    return game_titles


# create empty json file used in socket communication
def create_message_json(field=None, move=None):
    message = {
        'field': field,  # current field state
        'move': move,  # next move by player
    }
    message_json = json.dumps(message)
    return message_json


# read json file used in socket communication
def read_message_json(message_json):
    dict_data = json.loads(message_json)
    return dict_data
