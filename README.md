# Tic-Tac-Toe Game

A fun and interactive Tic-Tac-Toe game built with Streamlit Python.

## Features

- 🎮 Interactive game board with clickable cells
- 🔄 New game functionality 
- 📊 Real-time game statistics
- 🎯 Win detection (rows, columns, diagonals)
- 🤝 Tie game detection
- 📋 Built-in game instructions
- ✨ Clean and responsive UI

## Setup Instructions

### 1. Clone or Navigate to Project Directory
```bash
cd /path/to/tic-tac-toe
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
streamlit run app.py
```

The application will open automatically in your default browser at `http://localhost:8501`

## How to Play

1. **Starting the Game**: Player X always goes first
2. **Making Moves**: Click on any empty cell to place your symbol
3. **Winning**: Get three of your symbols in a row (horizontally, vertically, or diagonally)
4. **Tie Game**: If all 9 cells are filled with no winner, it's a tie
5. **New Game**: Click the "🔄 New Game" button to start over

## Game Rules

- The game is played on a 3x3 grid
- Players alternate turns (X goes first, then O)
- The first player to get 3 symbols in a row wins
- If the board fills up with no winner, the game is a tie

## Project Structure

```
tic-tac-toe/
├── venv/                 # Virtual environment
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technologies Used

- **Python 3.13+**
- **Streamlit** - Web application framework
- **NumPy** - Array operations for the game board

## Development

To modify the game:

1. Edit `app.py` to add new features
2. The game logic is contained in functions like `check_winner()`, `make_move()`, etc.
3. UI components are built using Streamlit widgets and layout functions

Enjoy playing Tic-Tac-Toe! 🎉