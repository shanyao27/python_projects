from stockfish import Stockfish
import chess


def analyze_chess_stockfish(moves_str: str) -> str:

    stockfish = Stockfish()
        
    board = chess.Board()
    moves = moves_str.split()
        
    for move_san in moves:
        move = board.parse_san(move_san) #SAN->MOVE
        board.push(move)#MOVE->FEN текстовое описание доски
        
        stockfish.set_fen_position(board.fen())

    best_move = stockfish.get_best_move()#UCI
        
    if best_move:
        move = chess.Move.from_uci(best_move)#UCI->SAN
        return board.san(move)
        
    return "Нет хода"