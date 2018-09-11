# MIT 6.034 Lab 3: Games
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff
import pdb
from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    if board.count_pieces()>=board.num_cols*board.num_rows:
        return True
    for element in board.get_all_chains():
        if len(element)>=4:
            return True
    return False

def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    boardList=[]
    if is_game_over_connectfour(board)==False:
        for i in xrange(board.num_cols):
            if not board.is_column_full(i):
                boardList.append(board.add_piece(i))
    return boardList
                
        

def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    if is_game_over_connectfour(board):
        if board.count_pieces()>=board.num_cols*board.num_rows:
            return 0
        elif is_current_player_maximizer:
            return -1000
        else:
            return 1000
    
def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    if is_game_over_connectfour(board):
        if board.count_pieces()>=board.num_cols*board.num_rows:
            score=0
        elif is_current_player_maximizer:
            score=-1000
        else:
            score=1000
        return score*(board.num_cols*board.num_rows-board.count_pieces())

def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    score1=0
    score2=0
    for chain in board.get_all_chains(current_player=True):
        score1+=len(chain)*10
    for chain in board.get_all_chains(current_player=False):
        score2+=len(chain)*10
    if is_current_player_maximizer:
        return score1-score2-1
    else:
        return score2-score1+1
    
# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.
calcs=0
def dfs_maximizing(state, calcs=0) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    if state.is_game_over():
        calcs+=1
        return([state], state.get_endgame_score(is_current_player_maximizer=True),calcs)
    else:
        best_path=None
        best_leaf=0
        for neighbor in state.generate_next_states():
            path,value, calcs =dfs_maximizing(neighbor,calcs)
            if value>best_leaf:
                best_path=path
                best_leaf=value
        return ([state]+best_path, best_leaf,calcs)

        
#pretty_print_dfs_type(dfs_maximizing(state_NEARLY_OVER))

def minimax_endgame_search(state, maximize=True, calcs=0) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    if state.is_game_over():
        calcs+=1
        return([state], state.get_endgame_score(is_current_player_maximizer=maximize),calcs)
    else:
        best_path=None
        best_leaf=None
        if maximize==True:
            for neighbor in state.generate_next_states():
                path,value, calcs =minimax_endgame_search(neighbor, not maximize, calcs)
                if value>=best_leaf:
                    best_path=path
                    best_leaf=value
        else:
            best_leaf=10000
            for neighbor in state.generate_next_states():
                path,value, calcs =minimax_endgame_search(neighbor, not maximize, calcs)
                if value<=best_leaf:
                    best_path=path
                    best_leaf=value

        return ([state]+best_path, best_leaf,calcs)
calcs=0                
# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))

calcs=0

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True, calcs=0) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."
    if state.is_game_over():
        calcs+=1
        return([state], state.get_endgame_score(is_current_player_maximizer=maximize),calcs)
    elif depth_limit==0:
        calcs+=1
        return([state], heuristic_fn(state.get_snapshot(), maximize),calcs)
    else:
        best_path=None
        best_leaf=None
        if maximize==True:
            for neighbor in state.generate_next_states():
                path,value, calcs =minimax_search(neighbor, heuristic_fn, depth_limit-1, not maximize, calcs)
                if value>best_leaf:
                    best_path=path
                    best_leaf=value
        else:
            best_leaf=INF
            for neighbor in state.generate_next_states():
                path,value, calcs =minimax_search(neighbor, heuristic_fn, depth_limit-1, not maximize, calcs)
                if value<best_leaf:
                    best_path=path
                    best_leaf=value
        return ([state]+best_path, best_leaf,calcs)
    
    

        


# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1.  Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True, calcs=0) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    if state.is_game_over():
        calcs+=1
        return([state], state.get_endgame_score(is_current_player_maximizer=maximize),calcs)
    elif depth_limit==0:
        calcs+=1
        return([state], heuristic_fn(state.get_snapshot(), maximize),calcs)
    else:
        best_path=[]
        if maximize==True:
            for neighbor in state.generate_next_states():
                path,value, calcs =minimax_search_alphabeta(neighbor,alpha, beta, heuristic_fn, depth_limit-1, not maximize, calcs)
                if value>alpha:
                    best_path=path
                    alpha=value
                if alpha>=beta:
                    return (best_path, alpha, calcs)
            return ([state]+best_path, alpha,calcs)

        else:
            for neighbor in state.generate_next_states():
                path,value, calcs =minimax_search_alphabeta(neighbor,alpha, beta, heuristic_fn, depth_limit-1, not maximize, calcs)
                if value<beta:
                    best_path=path
                    beta=value
                if alpha>=beta:
                    return path, beta, calcs
            return ([state]+best_path, beta,calcs)
        
# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.
    depth = 1
    while depth_limit >= depth:
        newVals = minimax_search_alphabeta(state, -(INF), INF, heuristic_fn, depth, maximize)
        depth += 1
        anytime_value.set_value(newVals)
    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#print progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4)


##### PART 3: Multiple Choice ##################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = "Dimitris Koutentakis"
COLLABORATORS = "Carl Unger, Luana Lopes Lara"
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = "scoring"
WHAT_I_FOUND_BORING = 'recursion'
SUGGESTIONS = None
