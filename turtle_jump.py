#! /usr/bin/env python



from copy import deepcopy
import pygame
from pygame.locals import *
from sys import exit

##############################################################################################

turn = 'white'
selected = (0, 1)
board = 0
move_limit = [150, 0]


best_move = ()
black, white = (), ()

window_size = (533, 600)
background_image_filename = 'board.png'
title = 'Turtle Jump'
board_size = 8
left = 1
fps = 5
pause = 5
start = True

##############################################################################################

class Piece(object):
    def __init__(self, color, king):
        self.color = color
        self.king = king


class Player(object):
    def __init__(self, type, color, strategy, ply_depth):
        self.type = type
        self.color = color
        self.strategy = strategy
        self.ply_depth = ply_depth



def init_board():
    global move_limit
    move_limit[1] = 0

    result = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1]
    ]  # initial board setting
    for m in range(9):
        for n in range(8):
            if (result[m][n] == 1):
                piece = Piece('black', False)
                result[m][n] = piece
            elif (result[m][n] == -1):
                piece = Piece('white', False)
                result[m][n] = piece
    return result


def init_player(type, color, strategy, ply_depth):
    return Player(type, color, strategy, ply_depth)



def avail_moves(board, player):
    moves = []

    for m in range(9):
        for n in range(8):
            if board[m][n] != 0 and board[m][n].color == player:
                if can_jump([m, n], [m + 1, n ], [m + 2, n ], board) == True: moves.append([m, n, m + 2, n ])
                if can_jump([m, n], [m - 1, n ], [m - 2, n ], board) == True: moves.append([m, n, m - 2, n ])
                if can_jump([m, n], [m , n - 1], [m , n - 2], board) == True: moves.append([m, n, m , n - 2])
                if can_jump([m, n], [m , n + 1], [m , n + 2], board) == True: moves.append([m, n, m , n + 2])
                if can_jump([m, n], [m + 1, n + 1], [m + 2, n + 2], board) == True: moves.append([m, n, m + 2, n + 2])
                if can_jump([m, n], [m - 1, n + 1], [m - 2, n + 2], board) == True: moves.append([m, n, m - 2, n + 2])
                if can_jump([m, n], [m + 1, n - 1], [m + 2, n - 2], board) == True: moves.append([m, n, m + 2, n - 2])
                if can_jump([m, n], [m - 1, n - 1], [m - 2, n - 2], board) == True: moves.append([m, n, m - 2, n - 2])
    if 1==1:
    #if len(moves)==0 or player=='white':
    #if len(moves) == 0:  # if there are no jumps in the list (no jumps available)
        for m in range(9):
            for n in range(8):
                if board[m][n] != 0 and board[m][n].color == player:
                    if can_move([m, n], [m + 1, n ], board) == True: moves.append([m, n, m + 1, n ])
                    if can_move([m, n], [m - 1, n ], board) == True: moves.append([m, n, m - 1, n ])
                    if can_move([m, n], [m , n - 1], board) == True: moves.append([m, n, m , n - 1])
                    if can_move([m, n], [m , n + 1], board) == True: moves.append([m, n, m , n + 1])
                    if can_move([m, n], [m + 1, n + 1], board) == True: moves.append([m, n, m + 1, n + 1])
                    if can_move([m, n], [m - 1, n + 1], board) == True: moves.append([m, n, m - 1, n + 1])
                    if can_move([m, n], [m + 1, n - 1], board) == True: moves.append([m, n, m + 1, n - 1])
                    if can_move([m, n], [m - 1, n - 1], board) == True: moves.append([m, n, m - 1, n - 1])

    return moves

def can_jump(a, via, b, board):
    if b[0] < 0 or b[0] > 8 or b[1] < 0 or b[1] > 7:
        return False
    if board[b[0]][b[1]] != 0: return False
    if board[via[0]][via[1]] == 0: return False
    if board[a[0]][a[1]].color == 'white':
        if board[via[0]][via[1]].color != 'black': return False
        return True
    if board[a[0]][a[1]].color == 'black':
        if board[via[0]][via[1]].color != 'white': return False
        return True


def can_move(a, b, board):
    if b[0] < 0 or b[0] > 8 or b[1] < 0 or b[1] > 7:
        return False
    if board[b[0]][b[1]] != 0: return False
    return True


def make_move(a, b, board):
    board[b[0]][b[1]] = board[a[0]][a[1]]
    board[a[0]][a[1]] = 0
    if abs(a[0]-b[0])==2 or abs(b[1]-a[1])==2:
        if board[(a[0] + b[0]) / 2][(a[1] + b[1]) / 2].color=='white': board[(a[0] + b[0]) / 2][(a[1] + b[1]) / 2].color='black'
        else: board[(a[0] + b[0]) / 2][(a[1] + b[1]) / 2].color='white'


def evaluate(game, player):

    def simple_score(game, player):
        black, white = 0, 0
        for m in range(9):
            for n in range(8):
                if (game[m][n] != 0 and game[m][n].color == 'black'):
                    black+=100
                elif (game[m][n] != 0 and game[m][n].color == 'white'):
                    white+=100
        if player != 'black':
            return white - black
        else:
            return black - white

    def piece_safety(game, player):
        black,white=0,0
        for m in range(9):
            for n in range(8):
                if (game[m][n] != 0 and game[m][n].color == 'black'):
                    if m-1>=0 and m-1<=8 and n-1>=0 and n-1<=7 and board[m-1][n-1]!=0 and board[m-1][n-1].color=='white':
                        black+=10
                    if m+1>=0 and m+1<=8 and n+1>=0 and n+1<=7 and board[m+1][n+1]!=0 and board[m+1][n+1].color=='white':
                        black+=10
                    if m+1>=0 and m+1<=8 and n-1>=0 and n-1<=7 and board[m+1][n-1]!=0 and board[m+1][n-1].color=='white':
                        black+=10
                    if m-1>=0 and m-1<=8 and n+1>=0 and n+1<=7 and board[m-1][n+1]!=0 and board[m-1][n+1].color=='white':
                        black+=10
                    if m-1>=0 and m-1<=8 and n>=0 and n<=7 and board[m-1][n]!=0 and board[m-1][n].color=='white':
                        black+=10
                    if m>=0 and m<=8 and n+1>=0 and n+1<=7 and board[m][n+1]!=0 and board[m][n+1].color=='white':
                        black+=10
                    if m+1>=0 and m+1<=8 and n>=0 and n<=7 and board[m+1][n]!=0 and board[m+1][n].color=='white':
                        black+=10
                    if m>=0 and m<=8 and n-1>=0 and n-1<=7 and board[m][n-1]!=0 and board[m][n-1].color=='white':
                        black+=10
                elif (game[m][n] != 0 and game[m][n].color == 'white'):
                    if m-1>=0 and m-1<=8 and n-1>=0 and n-1<=7 and board[m-1][n-1]!=0 and board[m-1][n-1].color=='black':
                        white+=10
                    if m+1>=0 and m+1<=8 and n+1>=0 and n+1<=7 and board[m+1][n+1]!=0 and board[m+1][n+1].color=='black':
                        white+=10
                    if m+1>=0 and m+1<=8 and n-1>=0 and n-1<=7 and board[m+1][n-1]!=0 and board[m+1][n-1].color=='black':
                        white+=10
                    if m-1>=0 and m-1<=8 and n+1>=0 and n+1<=7 and board[m-1][n+1]!=0 and board[m-1][n+1].color=='black':
                        white+=10
                    if m-1>=0 and m-1<=8 and n>=0 and n<=7 and board[m-1][n]!=0 and board[m-1][n].color=='black':
                        white+=10
                    if m>=0 and m<=8 and n+1>=0 and n+1<=7 and board[m][n+1]!=0 and board[m][n+1].color=='black':
                        white+=10
                    if m+1>=0 and m+1<=8 and n>=0 and n<=7 and board[m+1][n]!=0 and board[m+1][n].color=='black':
                        white+=10
                    if m>=0 and m<=8 and n-1>=0 and n-1<=7 and board[m][n-1]!=0 and board[m][n-1].color=='black':
                        white+=10
        if player != 'black':
            return white - black
        else:
            return black - white


    return (simple_score(game, player) + piece_safety(game,player) )


def end_game(board):
    black, white = 0, 0
    for m in range(9):
        for n in range(8):
            if board[m][n] != 0:
                if board[m][n].color == 'black':
                    black += 1
                else:
                    white += 1

    return black, white

def minimax(board, player, ply):
    global best_move

    if player != 'black':
        ply_depth = white.ply_depth
    else:
        ply_depth = black.ply_depth

    end = end_game(board)

    if ply >= ply_depth or end[0] == 0 or end[1] == 0:
        score = evaluate(board, player)
        return score

    if player != turn:

        beta = +10000

        moves = avail_moves(board, player)
        for i in range(len(moves)):
            new_board = deepcopy(board)
            make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board)

            if player == 'black':
                player = 'white'
            else:
                player = 'black'

            temp_beta = minimax(new_board, player, ply + 1)
            if temp_beta < beta:
                beta = temp_beta

        return beta

    else:
        alpha = -10000

        moves = avail_moves(board, player)
        for i in range(len(moves)):
            new_board = deepcopy(board)
            make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board)

            if player == 'black':
                player = 'white'
            else:
                player = 'black'

            temp_alpha = minimax(new_board, player, ply + 1)
            if temp_alpha > alpha:
                alpha = temp_alpha
                if ply == 0: best_move = (moves[i][0], moves[i][1]), (
                moves[i][2], moves[i][3])

        return alpha





def alpha_beta(player, board, ply, alpha, beta):
    global best_move

    if player != 'black':
        ply_depth = white.ply_depth
    else:
        ply_depth = black.ply_depth

    end = end_game(board)

    if ply >= ply_depth or end[0] == 0 or end[1] == 0:
        score = evaluate(board, player)
        return score

    moves = avail_moves(board, player)

    if player == turn:
        for i in range(len(moves)):
            new_board = deepcopy(board)
            make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board)

            if player == 'black':
                player = 'white'
            else:
                player = 'black'

            score = alpha_beta(player, new_board, ply + 1, alpha, beta)

            if score > alpha:
                if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3])
                alpha = score
            if alpha >= beta:
                return alpha

        return alpha

    else:
        for i in range(len(moves)):
            new_board = deepcopy(board)
            make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board)

            if player == 'black':
                player = 'white'
            else:
                player = 'black'

            score = alpha_beta(player, new_board, ply + 1, alpha, beta)

            if score < beta: beta = score
            if alpha >= beta: return beta
        return beta


def end_turn():
    global turn

    if turn != 'black':
        turn = 'black'
    else:
        turn = 'white'


def cpu_play(player):
    global board, move_limit
    if player.strategy == 'minimax':
        alpha = minimax(board, player.color, 0)
    elif player.strategy == 'alpha-beta':
        alpha = alpha_beta(player.color, board, 0, -10000, +10000)

    if alpha == -10000:
        if player.color == white:
            show_winner("black")
        else:
            show_winner("white")

    make_move(best_move[0], best_move[1], board)
    move_limit[1] += 1

    end_turn()


def ply_check():
    global black, white

    if black.type != 'cpu':
        black.ply_depth = white.ply_depth
    elif white.type != 'cpu':
        white.ply_depth = black.ply_depth


def player_check():
    global black, white

    if black.type != 'cpu' or black.type != 'human': black.type = 'cpu'
    if white.type != 'cpu' or white.type != 'human': white.type = 'cpu'

    if black.ply_depth < 0: black.ply_depth = 1
    if white.ply_depth < 0: white.ply_depth = 1

    if black.color != 'black': black.color = 'black'
    if white.color != 'white': white.color = 'white'

    if black.strategy != 'minimax'  or black.strategy != 'alpha-beta': black.strategy = 'alpha-beta'
    if white.strategy != 'minimax'  or white.strategy != 'alpha-beta': white.strategy = 'alpha-beta'


def game_init():
    global black, white
    black = init_player('cpu', 'black', 'alpha-beta', 2)
    white = init_player('human', 'white', 'alpha-beta', 2)
    board = init_board()

    return board



def draw_piece(row, column, color):
    posX = ((window_size[0] / 8) * column) - (window_size[0] / 8) / 2
    posY = ((window_size[1] / 9) * row) - (window_size[1] / 9) / 2

    if color == 'black':
        x = pygame.image.load('green.png').convert_alpha()

    elif color == 'white':
        x = pygame.image.load('red.png').convert_alpha()

    y = x.get_rect()
    y.centerx = posX
    y.centery = posY
    screen.blit(x, y)



def show_message(message):
    text = font.render(' ' + message + ' ', True, (255, 255, 255), (120, 195, 46))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery
    screen.blit(text, textRect)


def show_countdown(i):
    while i >= 0:
        tim = font_big.render(' ' + repr(i) + ' ', True, (255, 255, 255), (20, 160, 210))
        timRect = tim.get_rect()
        timRect.centerx = screen.get_rect().centerx
        timRect.centery = screen.get_rect().centery + 50
        screen.blit(tim, timRect)
        pygame.display.flip()
        i -= 1
        pygame.time.wait(1000)


def show_winner(winner):
    global board

    if winner == 'draw':
        show_message("draw, press 'F1' for a new game")
    else:
        show_message(winner + " wins, press 'F1' for a new game")
    pygame.display.flip()
    show_countdown(pause)
    board = init_board()


def mouse_click(pos):
    global selected, move_limit

    if (turn != 'black' and white.type != 'cpu') or (turn != 'white' and black.type != 'cpu'):
        column = pos[0] / (window_size[0] / 8)
        row = pos[1] / (window_size[1] / 9)

        if board[row][column] != 0 and board[row][column].color == turn:
            selected = row, column
        else:
            moves = avail_moves(board, turn)
            for i in range(len(moves)):
                if selected[0] == moves[i][0] and selected[1] == moves[i][1]:
                    if row == moves[i][2] and column == moves[i][3]:
                        make_move(selected, (row, column), board)
                        move_limit[1] += 1
                        end_turn()



pygame.init()

board = game_init()

ply_check()

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(title)
clock = pygame.time.Clock()

background = pygame.image.load(background_image_filename).convert()
font = pygame.font.Font('freesansbold.ttf', 11)
font_big = pygame.font.Font('freesansbold.ttf', 13)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
            mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                board = game_init('easy')


    screen.blit(background, (0, 0))


    if (turn != 'black' and white.type == 'human') or (turn != 'white' and black.type == 'human'):
        show_message('YOUR TURN')
    else:
        show_message('CPU THINKING...')

    for m in range(9):
        for n in range(8):
            if board[m][n] != 0:
                draw_piece(m + 1, n + 1, board[m][n].color)

    if start == True:
        show_message('Welcome to ' + title)
        start = False

    end = end_game(board)
    if end[1] == 0:
        show_winner("black")
    elif end[0] == 0:
        show_winner("white")

    elif move_limit[0] == move_limit[1]:
        show_winner("draw")

    else:
        pygame.display.flip()

    # cpu play
    if turn != 'black' and white.type == 'cpu':
        cpu_play(white)
    elif turn != 'white' and black.type == 'cpu':
        cpu_play(black)


    clock.tick(fps)