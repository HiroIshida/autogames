## install
```bash
git clone https://github.com/HiroIshida/autogames.git
cd autogames
pip install --user .
```

## Usage
### Where should I write ?
The function for main game algorithm is `think` function in `autogames/sciripts/games/tictactoe.py`.
Example implementation is like below.
```python
def think(self):
    return random.choice(self.available_positions())
```

### Use in localhost
To fight clients in localhost, type the commands below:
```bash
autogames_server --game tictactoe_game &
sleep 1
autogames_client --game tictactoe_game &
sleep 1
autogames_client --game tictactoe_game &
sleep 1
```
You can also call these commands in different terminals.

## Available games
 - tictactoe
   - この辺にゲームの画像貼る
   - （言語間で名前が統一された）変数や関数の用途を説明する
   - どういう情報をsocket通信したらよいかを分かりやすくまとめる

## Available environments
### OS
 - Linux:
   - Ubuntu 16.04
 - Windows
   - No data
 - Mac
   - No data

### Lauguages
 - Python 2.x
 - Python 3.x
