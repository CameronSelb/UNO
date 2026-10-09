# UNO Card Game 🃏

A command-line UNO game built with Python. Play against friends or challenge a computer opponent in this terminal-based version of the classic card game.

## Features
- Supports 1–8 players.
- Play against a computer opponent.
- Classic UNO cards, including Skip, Reverse, Draw Two, Wild, and Wild Draw Four.
- Choose colours when playing Wild cards.
- Automatic card shuffling and turn management.
- Win by being the first player to get rid of all your cards.

## Requirements
- Python 3.x

## Getting Started

Clone the repository:

```bash
git clone git@github.com:CameronSelb/UNO.git
```

Navigate to the project directory:

```bash
cd <pathto/UNO>
```

Run the game:

```bash
python uno.py
```

## How to Play
1. Enter the number of players (1–8). Selecting 1 enables the computer opponent.
2. Match the top discard card by colour or face, or play a Wild card.
3. Choose whether to pick up a card or play a card from your hand.
4. Follow the prompts for action cards and colour changes.
5. Be the first player to play all your cards to win!

## Project Structure

- `uno.py` – Main game loop, player turns, and gameplay.
- `logic.py` – Card deck creation, dealing, game rules, action cards, and computer opponent.

