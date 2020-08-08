# Minesweeper

This project implements an AI using Python to play the classical minesweeper game. 

It uses inference rules to decide what safe move it could take and if none is found, it choses a random one.

## Getting satrted
run `pip3 install -r requirements.txt` to install the required Python package (pygame) for this project if you don’t already have it installed.

## Usage
run `python runner.py` to start the game. 
You can either play yourslef or click on AI move for the AI to decide and take the current move. In the console you could see the moves that the AI is choosing between. <br>
The default size of the grid is **8 * 8** and the default number of mines is **8** which are distributed **randomly**. If you wish to change any of these values, alter them in `runner.py` file.