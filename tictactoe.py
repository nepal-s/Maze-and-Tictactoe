import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (255, 255, 255)
PLAYER_X = 'X'
PLAYER_O = 'O'

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Function to draw the Tic-Tac-Toe board
def draw_board():
    line_width = 15
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // 3, 0), (i * WIDTH // 3, HEIGHT), line_width)
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // 3), (WIDTH, i * HEIGHT // 3), line_width)

# Function to draw X or O on the board
def draw_symbol(player, row, col):
    font_size = 60
    font = pygame.font.Font(None, font_size)

    if player == PLAYER_X:
        text = font.render("X", True, LINE_COLOR)
    else:
        text = font.render("O", True, LINE_COLOR)

    text_rect = text.get_rect(center=(col * WIDTH // 3 + WIDTH // 6, row * HEIGHT // 3 + HEIGHT // 6))
    screen.blit(text, text_rect)

# Function to check for a winner
def check_winner(board, player):
    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Function to check if the board is full
def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

# Minimax algorithm
def minimax(board, depth, maximizing_player):
    scores = {'X': -1, 'O': 1, 'tie': 0}

    winner = check_winner(board, PLAYER_X)
    if winner:
        return scores['X']

    winner = check_winner(board, PLAYER_O)
    if winner:
        return scores['O']

    if is_board_full(board):
        return scores['tie']

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = PLAYER_O
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = PLAYER_X
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
        return min_eval

# Function to find the best move for the computer using Minimax
def find_best_move(board):
    best_val = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = PLAYER_O
                move_val = minimax(board, 0, False)
                board[i][j] = " "
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

# Main game loop
def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    turn = PLAYER_X

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // (HEIGHT // 3)
                clicked_col = mouseX // (WIDTH // 3)

                if board[clicked_row][clicked_col] == " ":
                    board[clicked_row][clicked_col] = turn
                    draw_symbol(turn, clicked_row, clicked_col)

                    if check_winner(board, turn):
                        print(f"{turn} wins!")
                        pygame.quit()
                        sys.exit()

                    if is_board_full(board):
                        print("It's a tie!")
                        pygame.quit()
                        sys.exit()

                    turn = PLAYER_O if turn == PLAYER_X else PLAYER_X

        if turn == PLAYER_O and not is_board_full(board) and not check_winner(board, PLAYER_O):
            # Computer's move
            print("Computer's move:")
            computer_move = find_best_move(board)
            board[computer_move[0]][computer_move[1]] = PLAYER_O
            draw_symbol(PLAYER_O, computer_move[0], computer_move[1])

            if check_winner(board, PLAYER_O):
                print("Computer wins!")
                pygame.quit()
                sys.exit()

            if is_board_full(board):
                print("It's a tie!")
                pygame.quit()
                sys.exit()

            turn = PLAYER_X

        draw_board()
        pygame.display.flip()

if __name__ == "__main__":
    main()
