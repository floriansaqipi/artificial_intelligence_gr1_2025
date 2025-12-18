import chess

PIECE_VALUES = {
    chess.KNIGHT: 30,
    chess.QUEEN: 90,
    chess.KING: 0
}

pruned_count = 0

def terminal_condition(board):
    white_pieces = len(board.piece_map(mask=board.occupied_co[chess.WHITE]))
    black_pieces = len(board.piece_map(mask=board.occupied_co[chess.BLACK]))
    return white_pieces <= 1 or black_pieces <= 1 or board.is_game_over()

def evaluate(board):
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score

def max_value(board, alpha, beta, depth):
    global pruned_count
    if depth == 0 or terminal_condition(board):
        return evaluate(board)
    
    v = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        v_prime = min_value(board, alpha, beta, depth - 1)
        board.pop()
        
        if v_prime > v:
            v = v_prime
        if v >= beta: # Pruning
            pruned_count += 1
            return v
        if v > alpha:
            alpha = v
    return v

def min_value(board, alpha, beta, depth):
    global pruned_count
    if depth == 0 or terminal_condition(board):
        return evaluate(board)
    
    v = float('inf')
    for move in board.legal_moves:
        board.push(move)
        v_prime = max_value(board, alpha, beta, depth - 1)
        board.pop()
        
        if v_prime < v:
            v = v_prime
        if v <= alpha: # Pruning
            pruned_count += 1
            return v
        if v < beta:
            beta = v
    return v

def play_chess():
    fen = "2n1k3/8/3q4/8/2N2Q2/8/8/4K3 w - - 0 1"
    board = chess.Board(fen)
    
    print("Configuration loaded:")
    print(board)
    
    choice = input("Choose player (1 for white, 2 for black): ")
    turn = chess.WHITE if choice == '1' else chess.BLACK
    board.turn = turn

    depth = 4
    
    while not terminal_condition(board):
        best_move = None
        
        if board.turn == chess.WHITE:
            val = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                res = min_value(board, float('-inf'), float('inf'), depth - 1)
                board.pop()
                if res > val:
                    val = res
                    best_move = move
        else:
            val = float('inf')
            for move in board.legal_moves:
                board.push(move)
                res = max_value(board, float('-inf'), float('inf'), depth - 1)
                board.pop()
                if res < val:
                    val = res
                    best_move = move
        
        print(f"Player {('white' if board.turn else 'black')} plays: {best_move}")
        board.push(best_move)
        print(board)
        
    print("\nEnd game!")
    print(f"Number of pruned branches: {pruned_count}")

if __name__ == "__main__":
    play_chess()