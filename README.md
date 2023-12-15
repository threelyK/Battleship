# Battleship Project

### Introduction
In ECM1400, we were given the task to recreate the popular 2-player board game "Battleship" using Python. This game is played between 2 players, who place their ships on a grid and take alternating turns trying to guess the location of the opponent's ships in order to sink them. The first person to have their entire fleet sunk loses.

### Features
- **Single-player mode without an opponent** -  In command-line interface (CLI).
- **Single-player mode with an AI opponent** - In the CLI or on a web server.
- **Random ship placement** - Ships are placed randomly on the board.
- **Interactive grid** - Players can input coordinates of their attack.
- **User Interface** - Game displayed using a web server.

### Prerequisites
- Python 3.11

### Installation
Install numpy:
```
pip install numpy
```
Install flask for the web server:
```
pip install flask
```

### Getting started tutorial
- Install this package
- Open the terminal
- Find the directory of the package
```
cd {installation-directory-of-package}
```
Type the corresponding code into the CLI depending on which version of the game you want to run.
1. Game in the CLI **without an AI** opponent
```
python game_engine.py
```
2. Game in the CLI **with an AI** opponent
```
python mp_game_engine.py
```
3. Game on **web server** against the AI opponent
```
python main.py
```
- Output: "Running on http://{address}:{port}"
In a web browser type the following:
- "http://{address}:{port}/placement", replace "{address}" and "{port}" with your corresponding address and port.

### Testing
Install pytest and pytest-depends, to run tests on the code
```
pip install pytest
pip install pytest-depends
```
Using pytest in the terminal execute all the files in the "tests" folder
```
pytest ./tests
```
### Developer documentation
4 Separate python files: main.py, mp_game_engine.py, game_engine.py, and components.py

- Having separate python files which we import certain functions from allow, each file to contain less code as we are not importing redundant code.
- The components.py is used in all of the other python files so it's important that you could import it into other files to reduce repetition of code.

### Details
- Author - Lego Yoda
- License - [MIT License](https://opensource.org/license/mit/)
- GitHub Repository - https://github.com/threelyK/Battleship
