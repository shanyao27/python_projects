#python3 -m streamlit run app.py
import streamlit as st
import chess
import chess.svg
from llm_chess import analyze_chess_llm
from stockfish_analyzer import analyze_chess_stockfish
from streamlit.components.v1 import html

st.set_page_config(page_title="Chess Assistant", layout="wide")
st.title("Chess Assistant")

if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "moves" not in st.session_state:
    st.session_state.moves = []
if "move_index" not in st.session_state:
    st.session_state.move_index = 0


def make_move(move_san):
    try:
        st.session_state.board.push_san(move_san)
        st.session_state.moves.append(move_san)
        st.session_state.move_index += 1
        return True, ""
    except Exception as e:
        return False, str(e)

def undo_move():
    if st.session_state.moves:
        st.session_state.board.pop()
        st.session_state.moves.pop()
        st.session_state.move_index -= 1

def reset_board():
    st.session_state.board = chess.Board()
    st.session_state.moves = []
    st.session_state.move_index = 0

def format_move_history(moves):
    formatted = ""
    for i in range(0, len(moves), 2):
        white = moves[i]
        black = moves[i+1] if i+1 < len(moves) else ""
        formatted += f"{i//2 + 1}. {white} {black}\n"
    return formatted

move_input = st.text_input("Введите ход")

col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("Сделать ход") and move_input:
        success, error = make_move(move_input)
        if not success:
            st.warning(f"Ошибка хода: {error}")
with col_btn2:
    if st.button("Отменить ход"):
        undo_move()
with col_btn3:
    if st.button("Сбросить партию"):
        reset_board()
        st.stop()

col_board, col_sidebar = st.columns([2, 1])

with col_board:
    st.subheader("Текущая позиция")
    svg_board = chess.svg.board(st.session_state.board)
    html(svg_board, height=400, width=400)

    if st.button("Анализировать позицию"):
        if st.session_state.moves:
            moves_str = " ".join(st.session_state.moves)
            
            with st.spinner("LLM анализирует"):
                llm_result = analyze_chess_llm(moves_str)
            
            with st.spinner("Stockfish анализирует"):
                best_move = analyze_chess_stockfish(moves_str)
            
            st.write("LLM анализ:")
            st.write(llm_result)
            
            st.write(f"Stockfish анализ:")
            st.write(f"Лучший следующий ход: {best_move}")
            
        else:
            st.info("Нужен хотя бы 1 ход")
