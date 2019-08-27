# Autogames

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
```
autogames_server --game othello_game --port 65432 & # server
python autogames/client/python/client.py --port 65432 --agent-file example_agent_othello --timeout 3 & # player1 with Python
python autogames/client/python/client.py --port 65432 --agent-file example_agent_othello --timeout 3 & # player2 with Python
```
You can fight against computer agents as a player.
```bash
autogames_server --game othello_game --port 65432 & # server
python autogames/client/python/client.py --port 65432 --agent-file example_agent_othello --timeout 3 & # player1 with Python
python autogames/client/python/client.py --port 65432 --agent-file human_agent --timeout 30 & # player you
```

# Usage
### Where should I write
For the main function of game algorithm, you can use `think` function in `autogames/client/(YOUR_LANGUAGE)/agents/(YOUR_AGENT_FLIE)`.
Example implementation is like below. (`autogames/client/python/agents/example_agent_tictactoe.py`)
```python
def think(self):
    return (random.randint(0, 2), random.randint(0, 2))
```

### Fight in localhost
To fight clients in localhost, you can create your opponents:
(You can also call these commands in different terminals.)
```bash
autogames_server --game (GAME_TYPE) --port 65432 & # you can list up game types by autogames_server --list
python autogames/client/python/client.py --port 65432 --agent-file (DEFAULT_AGENT_FLIE) --timeout 3 & # DEFAULT_AGENT_FLIE: e.g. example_agent_othello
```

Then, you can create your agent.
##### Python
```bash
python autogames/client/python/client.py --port 65432 --agent-file (YOUR_AGENT_FLIE) --timeout 3 & # your agent
```
##### C
```bash
cd autogames/client/c/; make client_c AGENT_FILE=(YOUR_AGENT_FLIE); cd -; ./autogames/client/c/client_c 65432 & # YOUR_AGENT_FLIE: e.g. example_agent_tictactoe.c
```

##### Human mode
```bash
python autogames/client/python/client.py --port 65432 --agent-file human_agent --timeout 30 & # human mode
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
   - どういう情報をsocket通信したらよいかを分かりやすくまとめる

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
 - Python 2.x
 - Python 3.x
 - C
