
import copy

class TicTacToe:
    def _init_(self):  
        self.initial_state = [' '] * 9

    def to_move(self, state):
        x_count = state.count('X')
        o_count = state.count('O')
        return 'X' if x_count == o_count else 'O'

    def actions(self, state):
        return [i for i, cell in enumerate(state) if cell == ' ']

    def result(self, state, action):
        new_state = copy.deepcopy(state)
        new_state[action] = self.to_move(state)
        return new_state

    def is_terminal(self, state):
        return self.utility(state, 'X') != 0 or self.utility(state, 'O') != 0 or ' ' not in state

    def utility(self, state, player):
        wins = [(0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)]
        for a,b,c in wins:
            if state[a] == state[b] == state[c] != ' ':
                return 1 if state[a] == player else -1
        return 0

    def display(self, state):
        for i in range(0, 9, 3):
            print('|'.join(state[i:i+3]))
            if i < 6:
                print('-'*5)

def minimax_search(game, state):
    player = game.to_move(state)
    value, move = max_value(game, state) if player == 'X' else min_value(game, state)
    return move

def max_value(game, state):
    if game.is_terminal(state):
        return game.utility(state, 'X'), None
    v = float('-inf')
    best_action = None
    for action in game.actions(state):
        min_v, _ = min_value(game, game.result(state, action))
        if min_v > v:
            v = min_v
            best_action = action
    return v, best_action

def min_value(game, state):
    if game.is_terminal(state):
        return game.utility(state, 'X'), None
    v = float('inf')
    best_action = None
    for action in game.actions(state):
        max_v, _ = max_value(game, game.result(state, action))
        if max_v < v:
            v = max_v
            best_action = action
    return v, best_action

def play():
    game = TicTacToe()
    state = game.initial_state
    human_player = input("Do you want to play as X or O? (X - you start, O - AI starts): ").upper()
    ai_player = 'O' if human_player == 'X' else 'X'

    while not game.is_terminal(state):
        game.display(state)
        if game.to_move(state) == ai_player:
            print(f"AI ({ai_player}) is thinking...")
            move = minimax_search(game, state)
        else:
            move = int(input("Enter your move (0-8): "))
            while move not in game.actions(state):
                move = int(input("Invalid move. Try again (0-8): "))
        state = game.result(state, move)

    game.display(state)
    score = game.utility(state, ai_player)
    if score == 1:
        print(f"{ai_player} wins!")
    elif score == -1:
        print(f"{human_player} wins!")
    else:
        print("It's a draw!")

play()
