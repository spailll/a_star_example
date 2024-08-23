# a_star_example
This is a simple program to demonstrate how the A* algorithm works and how it can be used to avoid predefined obstacles.

## Setup
Run the following commands on linux 
(should be similar on windows or mac, just look up how to set up a virtual environment)
```
$ python3 -m venv .venv
$ source ./.venv/bin/activate
$ pip3 install -r requirements.txt
```

## Usage
To use this program, run 
```
$ python3 main.py
```
After the program is running, the first square clicked will be the start position. The second square clicked will be the end node. every square clicked after that will be turned into a wall. 

To run the program, right click.

This program was only made to run once. To run the simulation again or to change any miss-clicks, close the window and restart the program.

## Options
Any of the variables at the top of the main.py file can easily be changed to change the simulation. 
    - WIDTH
    - ROWS
    - COLUMNS

