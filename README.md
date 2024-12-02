# River Crossing Puzzle Game 🚣‍♂️

An interactive Python implementation of the classic river crossing puzzle with emoji graphics and a hint system.

## Game Rules 📋

- A farmer must transport a fox, chicken, and grain across a river
- The boat can only carry the farmer and one item at a time
- If left unsupervised:
  - The fox will eat the chicken
  - The chicken will eat the grain

## Features ✨

- Interactive command-line interface with emoji graphics
- Built-in hint system
- Solution validator
- Move counter
- Automated solver using depth-first search
- Game state history tracking

## Requirements 🛠️

- Python 3.7+
- No additional dependencies required

## Installation 📥

```bash
git clone https://github.com/AllAboutAI-YT/river-crossing-puzzle.git
cd river-crossing-puzzle
python river_crossing.py
```

## How to Play 🎮

1. Run the game: `python river_crossing.py`
2. Type commands to move items:
   - `fox`, `chicken`, `grain`: Move with specific item
   - `none`: Move farmer alone
   - `hint`: Get a suggestion
   - `help`: Show commands
   - `quit`: Exit game

## Solution Strategy 🧩

The puzzle can be solved in 7 moves. Use the hint system if you get stuck!

## Contributing 🤝

Feel free to open issues or submit pull requests with improvements.