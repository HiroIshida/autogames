# -*- coding: utf-8 -

import autogames
import glob
import os


def get_game_titles():
    game_titles = []
    package_path = autogames.__file__
    games_path = os.path.join(
        os.path.dirname(package_path), 'scripts', 'games') + '/*'
    file_names = glob.glob(games_path)
    for file_name in file_names:
        file_name = os.path.basename(file_name)
        # pick up only python files
        if file_name.endswith('.py') and \
           file_name != '__init__.py' and \
                        file_name != 'game_manager.py':
            game_titles.append(os.path.splitext(file_name)[0])
    return game_titles
