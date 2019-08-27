# Autogames

[![Build Status](https://travis-ci.com/HiroIshida/autogames.svg?token=9fpkKj6dzfmzwRd4k3Gq&branch=master)](https://travis-ci.com/HiroIshida/autogames/)

 - [Overview](#overview)
 - [Install](#install)
 - [Example](#example)
 - [Usage](#usage)
   - [Where should I write](#where-should-i-write)
   - [Fight in localhost](#fight-in-localhost)
    - [Python](#python)
    - [C](#c)
    - [Human mode](#human-mode)
 - [Available games](#available-games)
   - [tictactoe](#tictactoe)
   - [Othello](#othello)
 - [Available environments](#available-environments)
   - [OS](#os)
   - [Languages](#languages)

# Overview

You can try your own game AI program with a lot of boardgames and programming languages.

# Install
```bash
git clone https://github.com/HiroIshida/autogames.git
cd autogames
pip install --user .
```

# Example
For example, you can try othello demo. Two computer agents automatically fight against each other.
```bash
# server of othello game
autogames_server --game othello_game --port 65432 &
# computer player1 with Python
python autogames/client/python/client.py --port 65432 --agent-file example_agent_othello &
# player2 with Python
python autogames/client/python/client.py --port 65432 --agent-file example_agent_othello &
```
You can fight against computer agents as a player.
```bash
# server of othello game
autogames_server --game othello_game --port 65432 &
# computer player with Python
python autogames/client/python/client.py --port 65432 --agent-file example_agent_othello &
# human player (you)
python autogames/client/python/client.py --port 65432 --agent-file human_agent --timeout 30 &
```

# Usage
### Where should I write
You can use `think` function in autogames/client/(LANGUAGE)/agents/(AGENT_FLIE) for the main function of game algorithm

Example implementation of othello agent is like below. (`autogames/client/python/agents/example_agent_tictactoe.py`)
```python
def think(self):
    return (random.randint(0, 2), random.randint(0, 2))
```

### Fight in localhost
To fight clients in localhost, you can create your opponents. You can also call these commands in different terminals.
```bash
# game server. you can list up game types (GAME_TYPE) by autogames_server --list
autogames_server --game (GAME_TYPE) --port 65432 &
# computer player. AGENT_FLIE is the file name in agents dir (e.g. example_agent_othello)
python autogames/client/python/client.py --port 65432 --agent-file (AGENT_FLIE) --timeout 3 &
```

Then, you can create your agent.
##### Python
```bash
# your agent
python autogames/client/python/client.py --port 65432 --agent-file (AGENT_FLIE) --timeout 3 &
```
##### C
```bash
# compile C program
cd autogames/client/c/;
# AGENT_FLIE: e.g. example_agent_tictactoe.c
make client_c AGENT_FILE=(AGENT_FLIE);
cd -;
# your agent
./autogames/client/c/client_c 65432 &
```

##### Human mode
```bash
# human mode. You can play game interactively.
python autogames/client/python/client.py --port 65432 --agent-file human_agent --timeout 30 &
```

# Available games
### tictactoe
   - 三目並べ(sanmoku narabe) in japanese　（この辺にゲームの画像貼る）
   ```
      0 1 2
    0|X|O|X|
    1|O|X|O|
    2|X|O|X|
   ```
   - （言語間で名前が統一された）変数や関数の用途を説明する
   - 通信するjsonの中身を貼り、どういう情報をsocket通信したらよいかを説明する。(jsonは全ゲーム共通か？)

### Othello
   - オセロ、リバーシ(othello game)
   ```
      0 1 2 3 4 5 6 7
    0| | | | | | | | |
    1| | | | | | | | |
    2| | | | | | | | |
    3| | | |X|O| | | |
    4| | | |O|X| | | |
    5| | | | | | | | |
    6| | | | | | | | |
    7| | | | | | | | |
   ```

# Available environments
### OS
 - Linux:
   - Ubuntu 16.04
 - Windows
   - No data
 - Mac
   - No data

### Languages
 - Python 2.7
 - Python 3.6
 - C (gcc 5.4.0)
