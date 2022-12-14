from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import pygame, sys, time
pygame.init()

# global variables
WIDTH, HEIGHT = 512, 512
MESSAGE_MARGIN = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (112,128,144)

COLORS = [
    (60, 32, 16), # brown
    (16, 144, 85), # green
    (199, 69, 50), # red
    (229, 201, 33), # yellow
    (217, 121, 170), # pink
    (103, 55, 134), # purple
    (5, 107, 173), # blue
    (214, 116, 33) # orange
]
BOARD = [
    [ 7, 6, 5, 4, 3, 2, 1, 0 ],
    [ 2, 7, 4, 1, 6, 3, 0, 5 ],
    [ 1, 4, 7, 2, 5, 0, 3, 6 ],
    [ 4, 5, 6, 7, 0, 1, 2, 3 ],
    [ 3, 2, 1, 0, 7, 6, 5, 4 ],
    [ 6, 3, 0, 5, 2, 7, 4, 1 ],
    [ 5, 0, 3, 6, 1, 4, 7, 2 ],
    [ 0, 1, 2, 3, 4, 5, 6, 7 ]
]

PLAYERCOLOR = [ BLACK, WHITE ]
BLOCK_DELAY = 5

# set pygame
font = pygame.font.SysFont("comicsans",20)
screen = pygame.display.set_mode((WIDTH, HEIGHT + MESSAGE_MARGIN))
pygame.display.set_caption("KAMISADO")

class Kamisado(TwoPlayerGame):
    # First of all, the definition of what a game needs.
    def __init__(self, players):
        self.players = players
        self.current_player = 1

        self.first_move = True
        self.tower = [
            [ (0, 7), (0, 6), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (2, 2) ],
            [ (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7) ]
        ]
        self.turn = 1
        self.tower_to_move = -1
        self.tower_to_move_coord = None

        self.blocked_coord_list = None

        self.is_win = False


    # Defines all possible movements on the board.
    # The calculation method of possible_moves is different depending on the turn.
    # The direction of movement of ai turn and my turn is opposite.
    def possible_moves(self):
        result = []
        # ----------------------FILL BELOW--------------------------
        if self.is_blocked():
            result.append(self.tower_to_move_coord)
            return result
        else:
            result = []
            towers = self.tower[0] + self.tower[1]
            if self.turn == 1:
                # vertical
                for r in range(self.tower_to_move_coord[0]-1,-1,-1):
                    if (r, self.tower_to_move_coord[1]) in towers:
                        break
                    result.append((r, self.tower_to_move_coord[1]))

                # left diagonal
                rs = range(self.tower_to_move_coord[0]-1, -1, -1)
                cs = range(self.tower_to_move_coord[1]-1, -1, -1)
                for r, c in zip(rs, cs):
                    if (r, c) in towers:
                        break
                    result.append((r, c))

                # right diagonal
                rs = range(self.tower_to_move_coord[0] - 1, -1, -1)
                cs = range(self.tower_to_move_coord[1] + 1, 8)
                for r, c in zip(rs, cs):
                    if (r, c) in towers:
                        break
                    result.append((r, c))

            else:
                # vertical
                for r in range(self.tower_to_move_coord[0]+1, 8):
                    if (r, self.tower_to_move_coord[1]) in towers:
                        break
                    result.append((r, self.tower_to_move_coord[1]))

                # left diagonal
                rs = range(self.tower_to_move_coord[0]+1, 8)
                cs = range(self.tower_to_move_coord[1]-1, -1, -1)
                for r, c in zip(rs, cs):
                    if (r, c) in towers:
                        break
                    result.append((r, c))

                # right diagonal
                rs = range(self.tower_to_move_coord[0]+1, 8)
                cs = range(self.tower_to_move_coord[1]+1, 8)
                for r, c in zip(rs, cs):
                    if (r, c) in towers:
                        break
                    result.append((r, c))
        # ----------------------------------------------------------
        return result


    # Define how to update the board after the player moves.
    def make_move(self, move):
        # ----------------------FILL BELOW--------------------------
        # move the tower(tower update)
        self.tower[self.turn][self.tower_to_move] = move
        # ----------------------------------------------------------

        # check if any player win
        if not self.is_over():
            # Set turns, position and coordinates
            self.set_next_turn(move)
        # check if next player is blocked

        if self.is_blocked():
            # check for deadlock
            if self.is_deadlock(self.turn, self.tower_to_move, self.tower_to_move_coord):
                # the oppoenet player is winner
                self.is_win = True



    def is_blocked(self, coord=None, turn=None):
        # ----------------------FILL BELOW--------------------------
        # block check
        forward = 1 if self.turn == 0 else -1
        towers = self.tower[0] + self.tower[1]
        if self.tower_to_move_coord == None:
            return False
        else:
            if self.tower_to_move_coord[1] == 0:  # left most column
                t1 = (self.tower_to_move_coord[0] + forward, self.tower_to_move_coord[1])
                t2 = (self.tower_to_move_coord[0] + forward, self.tower_to_move_coord[1] + 1)
                if (t1 in towers) and (t2 in towers):
                    return True
            elif self.tower_to_move_coord[1] == 7:  # right most column
                t1 = (self.tower_to_move_coord[0] + forward, self.tower_to_move_coord[1])
                t2 = (self.tower_to_move_coord[0] + forward, self.tower_to_move_coord[1] - 1)
                if (t1 in towers) and (t2 in towers):
                    return True
            else:
                t1 = (self.tower_to_move_coord[0] + forward, self.tower_to_move_coord[1])
                t2 = (self.tower_to_move_coord[0] + forward, self.tower_to_move_coord[1] - 1)
                t3 = (self.tower_to_move_coord[0] + forward, self.tower_to_move_coord[1] + 1)
                if (t1 in towers) and (t2 in towers) and (t3 in towers):
                    return True
        # ----------------------------------------------------------
        return False

    def is_deadlock(self, turn, tower_to_move, tower_to_move_coord):
        turn = 1 if turn == 0 else 0
        tower_to_move = BOARD[self.tower_to_move_coord[0]][self.tower_to_move_coord[1]]
        tower_to_move_coord = self.tower[turn][tower_to_move]
        if self.is_blocked_for_deadlock(tower_to_move_coord, turn):
            # ----------------------MODIFY BELOW--------------------------
            if tower_to_move_coord == self.next_move_for_blocked()[0]:
                return True
            else:
                return False
            # ----------------------------------------------------------
        else:
            return False

    def next_move_for_blocked(self):
        temp_turn, temp_tower_to_move, temp_tower_to_move_pos, temp_tower, board = self.turn, self.tower_to_move, self.tower_to_move_coord, self.tower, BOARD
        temp_turn = 1 if temp_turn == 0 else 0
        temp_tower_to_move = board[temp_tower_to_move_pos[0]][temp_tower_to_move_pos[1]]
        temp_tower_to_move_pos = temp_tower[temp_turn][temp_tower_to_move]
        return temp_tower_to_move_pos, temp_turn

    def is_blocked_for_deadlock(self, coord, turn):
        # ----------------------FILL BELOW--------------------------
        # block check
        forward = 1 if turn == 0 else -1
        towers = self.tower[0] + self.tower[1]
        tower_coord = coord
        if tower_coord[1] == 0:  # left most column
            t1 = (tower_coord[0] + forward, tower_coord[1])
            t2 = (tower_coord[0] + forward, tower_coord[1] + 1)
            if (t1 in towers) and (t2 in towers):
                return True
        elif tower_coord[1] == 7:  # right most column
            t1 = (tower_coord[0] + forward, tower_coord[1])
            t2 = (tower_coord[0] + forward, tower_coord[1] - 1)
            if (t1 in towers) and (t2 in towers):
                return True
        else:
            t1 = (tower_coord[0] + forward, tower_coord[1])
            t2 = (tower_coord[0] + forward, tower_coord[1] - 1)
            t3 = (tower_coord[0] + forward, tower_coord[1] + 1)
            if (t1 in towers) and (t2 in towers) and (t3 in towers):
                return True
        return False

    def set_next_turn(self, coord):
        # ----------------------FILL BELOW--------------------------

        # store block coord list for checking deadlock
        self.blocked_coord_list = coord

        # switch turn
        self.turn = 1 if self.turn == 0 else 0

        # set next tower and its coordinate to move
        self.tower_to_move = BOARD[coord[0]][coord[1]]
        self.tower_to_move_coord = self.tower[self.turn][self.tower_to_move]

        # ----------------------------------------------------------
        self.first_move = False

    # check if the game is over
    def is_over(self):
        return (
            self.is_win
            or self.win(self.current_player - 1)
            or self.win(self.opponent_index - 1)
        )

    def scoring(self):
        opp_won = self.win(self.opponent_index - 1)
        i_won = self.win(self.current_player - 1)
        # modify score according to conditions
        # ----------------------MODIFY BELOW--------------------------
        if opp_won and not i_won:
            score = 100
        elif i_won and not opp_won:
            score = -100
        else:
            score = 0
        # ------------------------------------------------------------
        return score

    def win(self, who):
        end_line_index = 7 if who == 0 else 0
        for i in self.tower[who]:
            if i[0] == end_line_index:
                return True
        return False

    def select_tower_to_move_first(self, coord):
        for i, t in enumerate(self.tower[self.turn]):
            if coord == t:
                self.tower_to_move = i
                self.tower_to_move_coord = coord

    def reset_tower_to_move_first(self):
        self.tower_to_move = -1

def draw_grid():
    for i in range(8): # index of row
        for j in range(8): # index of col
            # locate a rect at i-th row and j-th col
            rect = pygame.Rect(
                (j * WIDTH/8, i * HEIGHT/8), (WIDTH/8, HEIGHT/8))
            pygame.draw.rect(screen, COLORS[BOARD[i][j]], rect, width=0)

def draw_tower(game):
    for p in range(2): # player (0 or 1)
        for i in range(8): # each tower
            center = (game.tower[p][i][1] * WIDTH/8 + WIDTH/16,
                        game.tower[p][i][0] * HEIGHT/8 + HEIGHT/16)
            pygame.draw.circle(screen, COLORS[i], center, WIDTH/16, width=0)
            pygame.draw.circle(screen, PLAYERCOLOR[p], center, WIDTH/16, width=2)

def _message_margin(txt, backgr, textcol):
    rect = pygame.Rect( (0, HEIGHT), (WIDTH, MESSAGE_MARGIN) )
    pygame.draw.rect(screen, backgr, rect)
    pos_text = font.render(txt, True, textcol)
    pos_rect = pos_text.get_rect()
    pos_rect.center = ( WIDTH/2, HEIGHT + MESSAGE_MARGIN/2 )
    screen.blit(pos_text, pos_rect)

def msg_turn(game):
    title = "Win" if game.is_over() else "Turn"

    if game.turn == 0: # turn of blacks
        txt = "{}: {}".format(title, 'black')
        _message_margin(txt, BLACK, WHITE)
    else:
        txt = "{}: {}".format(title, 'white')
        _message_margin(txt, WHITE, BLACK)

def msg_blocked(game):
    BLOCK_MSG = 'Please click your position.'
    BLOCK_DELAY = 3
    if game.is_blocked():
        if game.turn == 0: # turn of blacks
            txt = "Blocked: next turn -> {} in {} sec.".format('white', BLOCK_DELAY)
            _message_margin(txt, BLACK, WHITE)
        else:
            txt = "Blocked: next turn -> {}, {}".format('black', BLOCK_MSG)
            _message_margin(txt, WHITE, BLACK)

def highlight_cell(game):
    if game.tower_to_move >= 0:
        rect = pygame.Rect(
                    (game.tower_to_move_coord[1] * WIDTH/8,
                    game.tower_to_move_coord[0] * HEIGHT/8),
                    (WIDTH/8, HEIGHT/8))
        pygame.draw.rect(screen, PLAYERCOLOR[game.turn], rect, width=2)

def calc_coord(pos):
    return (int(pos[1] / (HEIGHT/8)), int(pos[0] / (WIDTH/8)))

def draw_board(game):
    draw_grid()
    draw_tower(game)
    msg_turn(game)
    highlight_cell(game)
    msg_blocked(game)
    pygame.display.update()

def test():
    return ("!!")

if __name__ == '__main__':
    kamisado = Kamisado([Human_Player(), AI_Player(Negamax(5))])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                coord = calc_coord(pygame.mouse.get_pos())

                if kamisado.tower_to_move < 0:
                    kamisado.select_tower_to_move_first(coord) # set the tower to move
                    continue

                if kamisado.first_move and kamisado.tower_to_move_coord == coord: # reset the chosen tower
                    kamisado.reset_tower_to_move_first()

                # MY TURN
                elif coord in kamisado.possible_moves():
                    kamisado.play_move(coord)

                    if kamisado.is_over():
                        kamisado.tower_to_move_coord = coord


                    # AI TURN
                    else:
                        draw_board(kamisado)

                        if kamisado.is_blocked():
                            pygame.time.delay(3000)

                        pygame.time.delay(500)
                        ai_move = kamisado.get_move()
                        kamisado.play_move(ai_move)

                        if kamisado.is_over():
                            kamisado.tower_to_move_coord = ai_move

        draw_board(kamisado)
