import streamlit as st
import numpy as np
from typing import Optional, List, Tuple

# Page configuration
st.set_page_config(
    page_title="Tic-Tac-Toe Game",
    page_icon="🎮",
    layout="centered"
)

# Initialize session state
def initialize_game():
    """Initialize the game state"""
    if 'board' not in st.session_state:
        st.session_state.board = np.full((3, 3), '', dtype=str)
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 'X'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'moves_count' not in st.session_state:
        st.session_state.moves_count = 0
    # Player names initialization
    if 'player_x_name' not in st.session_state:
        st.session_state.player_x_name = 'Player X'
    if 'player_o_name' not in st.session_state:
        st.session_state.player_o_name = 'Player O'

def check_winner(board: np.ndarray) -> Optional[str]:
    """Check if there's a winner on the board"""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    
    return None

def is_board_full(board: np.ndarray) -> bool:
    """Check if the board is full"""
    return not np.any(board == '')

def make_move(row: int, col: int):
    """Make a move on the board"""
    if st.session_state.board[row][col] == '' and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        st.session_state.moves_count += 1
        
        # Check for winner
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.game_over = True
        elif is_board_full(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = 'Tie'
        else:
            # Switch player
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

def reset_game():
    """Reset the game to initial state"""
    st.session_state.board = np.full((3, 3), '', dtype=str)
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.moves_count = 0

def get_player_name(symbol: str) -> str:
    """Get player name based on symbol"""
    return st.session_state.player_x_name if symbol == 'X' else st.session_state.player_o_name

def get_current_player_name() -> str:
    """Get current player's name based on turn"""
    return get_player_name(st.session_state.current_player)

def setup_players():
    """Handle player name input and validation"""
    st.markdown("### 👥 Player Setup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        temp_x_name = st.text_input(
            "Player 1 Name (X)",
            value=st.session_state.player_x_name if st.session_state.player_x_name != 'Player X' else '',
            placeholder="Enter Player 1 Name",
            key="input_player_x"
        )
    
    with col2:
        temp_o_name = st.text_input(
            "Player 2 Name (O)",
            value=st.session_state.player_o_name if st.session_state.player_o_name != 'Player O' else '',
            placeholder="Enter Player 2 Name",
            key="input_player_o"
        )
    
    # Validation and confirmation
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("✅ Set Names", key="set_names"):
            # Validation
            x_name = temp_x_name.strip() if temp_x_name.strip() else 'Player X'
            o_name = temp_o_name.strip() if temp_o_name.strip() else 'Player O'
            
            # Check for identical names
            if x_name.lower() == o_name.lower() and x_name != 'Player X':
                st.error("❌ Player names cannot be identical!")
                return False
            
            # Check for very long names
            if len(x_name) > 20 or len(o_name) > 20:
                st.error("❌ Player names must be 20 characters or less!")
                return False
            
            # Set names
            st.session_state.player_x_name = x_name
            st.session_state.player_o_name = o_name
            st.success(f"✅ Players set: {x_name} vs {o_name}")
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 Reset Names", key="reset_names"):
            st.session_state.player_x_name = 'Player X'
            st.session_state.player_o_name = 'Player O'
            st.rerun()
    
    with col_btn3:
        if st.button("🎮 Start Game", key="start_game"):
            # Set names if they were entered
            if temp_x_name.strip():
                st.session_state.player_x_name = temp_x_name.strip()
            if temp_o_name.strip():
                st.session_state.player_o_name = temp_o_name.strip()
            st.rerun()
    
    return True

def get_winning_cells() -> List[Tuple[int, int]]:
    """Get the positions of winning cells"""
    board = st.session_state.board
    
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return [(i, 0), (i, 1), (i, 2)]
    
    # Check columns  
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != '':
            return [(0, j), (1, j), (2, j)]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return [(0, 2), (1, 1), (2, 0)]
    
    return []

def create_game_board():
    """Create a proper game board with enhanced styling"""
    winning_cells = get_winning_cells() if st.session_state.winner and st.session_state.winner != 'Tie' else []
    
    # Enhanced CSS for better grid appearance  
    board_css = """
    <style>
    /* Enhanced button styling */
    div[data-testid="column"] > div > div > div > button {
        width: 110px !important;
        height: 110px !important;
        font-size: 42px !important;
        font-weight: bold !important;
        border: 4px solid #34495e !important;
        border-radius: 15px !important;
        margin: 3px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
        background: linear-gradient(145deg, #ffffff, #e8e8e8) !important;
        position: relative !important;
    }
        border-radius: 15px !important;
        margin: 3px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
        background: linear-gradient(145deg, #ffffff, #e8e8e8) !important;
        position: relative !important;
    }
    
    div[data-testid="column"] > div > div > div > button:hover:not(:disabled) {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3) !important;
        border-color: #2980b9 !important;
        background: linear-gradient(145deg, #f8f9fa, #e9ecef) !important;
    }
    
    /* X symbol styling */
    div[data-testid="column"] > div > div > div > button[title*="X"],
    div[data-testid="column"] > div > div > div > button:contains("✖") {
        color: #e74c3c !important;
        text-shadow: 3px 3px 6px rgba(231, 76, 60, 0.4) !important;
        border-color: #c0392b !important;
    }
    
    /* O symbol styling */
    div[data-testid="column"] > div > div > div > button[title*="O"],
    div[data-testid="column"] > div > div > div > button:contains("⭕") {
        color: #3498db !important;
        text-shadow: 3px 3px 6px rgba(52, 152, 219, 0.4) !important;
        border-color: #2980b9 !important;
    }
    
    /* Empty cell styling */
    div[data-testid="column"] > div > div > div > button:contains("+") {
        color: #95a5a6 !important;
        font-size: 28px !important;
        opacity: 0.6 !important;
    }
    
    /* Disabled button styling */
    div[data-testid="column"] > div > div > div > button:disabled {
        opacity: 0.9 !important;
        cursor: default !important;
        transform: none !important;
    }
    
    /* Winning cell animation */
    .winning-pulse {
        animation: winning-glow 1.5s ease-in-out infinite !important;
    }
    
    @keyframes winning-glow {
        0%, 100% { 
            box-shadow: 0 0 10px #f1c40f, 0 0 20px #f1c40f, 0 0 30px #f1c40f !important;
            border-color: #f39c12 !important;
        }
        50% { 
            box-shadow: 0 0 20px #f39c12, 0 0 30px #f39c12, 0 0 40px #f39c12 !important;
            border-color: #e67e22 !important;
        }
    }
    </style>
    """
    
    st.markdown(board_css, unsafe_allow_html=True)
    
    # Create 3x3 grid using Streamlit columns with enhanced spacing
    for row in range(3):
        cols = st.columns([1, 1, 1], gap="small")
        for col in range(3):
            with cols[col]:
                cell_value = st.session_state.board[row][col]
                is_winning = (row, col) in winning_cells
                is_empty = cell_value == ''
                
                # Determine display value
                if cell_value == 'X':
                    display_value = "✖"
                elif cell_value == 'O':
                    display_value = "⭕"
                else:
                    display_value = "+"
                
                # Create button with enhanced interaction
                button_key = f"cell_{row}_{col}"
                
                # Set up help text
                help_text = None
                if not st.session_state.game_over and is_empty:
                    current_player_name = get_current_player_name()
                    help_text = f"Click here, {current_player_name}! Place {st.session_state.current_player}"
                elif is_winning:
                    winner_name = get_player_name(st.session_state.winner)
                    help_text = f"Winning move by {winner_name}!"
                elif not is_empty:
                    cell_player_name = get_player_name(cell_value)
                    help_text = f"Cell occupied by {cell_player_name}"
                
                # Create the button
                if st.button(
                    display_value,
                    key=button_key,
                    help=help_text,
                    disabled=st.session_state.game_over or not is_empty,
                    use_container_width=True
                ):
                    make_move(row, col)
                    st.rerun()
                
                # Add winning cell effect with JavaScript if needed
                if is_winning:
                    st.markdown(
                        f"""
                        <script>
                        // Add winning class to button
                        setTimeout(function() {{
                            const button = document.querySelector('[data-testid="baseButton-secondary"][data-testid*="{button_key}"]');
                            if (button) {{
                                button.classList.add('winning-pulse');
                            }}
                        }}, 100);
                        </script>
                        """, 
                        unsafe_allow_html=True
                    )

def main():
    """Main application function"""
    # Initialize game
    initialize_game()
    
    # Title and header with enhanced styling
    st.markdown(
        """
        <style>
        .main-title {
            text-align: center;
            color: #2c3e50;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            font-size: 18px;
            margin-bottom: 30px;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown('<h1 class="main-title">🎮 Tic-Tac-Toe Game</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Challenge a friend to the classic strategy game!</p>', unsafe_allow_html=True)
    
    # Player setup section (collapsible)
    with st.expander("👥 Player Setup", expanded=False):
        setup_players()
    
    st.markdown("---")
    
    # Game status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not st.session_state.game_over:
            current_player_name = get_current_player_name()
            st.info(f"Current Player: **{current_player_name} ({st.session_state.current_player})**")
        else:
            if st.session_state.winner == 'Tie':
                st.warning("**It's a Tie!** 🤝")
            else:
                winner_name = get_player_name(st.session_state.winner)
                st.success(f"**{winner_name} Wins!** 🎉")
    
    with col2:
        st.metric("Moves", st.session_state.moves_count)
    
    with col3:
        if st.button("🔄 New Game", key="reset_button"):
            reset_game()
            st.rerun()
    
    st.markdown("---")
    
    # Game board
    st.markdown("### 🎯 Game Board")
    create_game_board()
    
    # Game instructions
    st.markdown("---")
    with st.expander("📋 How to Play"):
        st.markdown("""
        **Rules:**
        1. The game is played on a 3x3 grid
        2. Player X goes first, then Player O
        3. Click on an empty cell to place your symbol
        4. The first player to get 3 of their symbols in a row (horizontally, vertically, or diagonally) wins
        5. If all 9 cells are filled and no player has 3 in a row, the game is a tie
        
        **Tips:**
        - Try to get three in a row while blocking your opponent
        - Control the center square when possible
        - Watch for opportunities to create multiple winning threats
        """)
    
    # Statistics (optional enhancement)
    if st.session_state.moves_count > 0:
        st.markdown("---")
        st.markdown("### Game Statistics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            x_count = np.count_nonzero(st.session_state.board == 'X')
            x_player_name = get_player_name('X')
            st.metric(f"{x_player_name} (X) Moves", x_count)
        
        with col2:
            o_count = np.count_nonzero(st.session_state.board == 'O')
            o_player_name = get_player_name('O')
            st.metric(f"{o_player_name} (O) Moves", o_count)
        
        with col3:
            empty_count = np.count_nonzero(st.session_state.board == '')
            st.metric("Empty Cells", empty_count)

if __name__ == "__main__":
    main()