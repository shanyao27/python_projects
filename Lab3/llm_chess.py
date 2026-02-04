#python3 -m streamlit run app.py
from openai import OpenAI

client = OpenAI( 
    base_url="http://localhost:11434/v1",
    api_key="none"
)

def analyze_chess_llm(moves: str) -> str:
    system_prompt = """ 
        Ты шахматный ассистент. 
        Отвечай только по фактам. Не придумывай ходы. 
        Используй шахматные дебюты.

        Примеры:
        1. e4 e5 Nf3 Nc6 Bb5 — Дебют: Испанская партия, Лучший следующий ход: O-O
        2. d4 d5 c4 — Дебют: Ферзевый гамбит, Лучший следующий ход: Nc3
        3. e4 c5 — Дебют: Сицилианская защита, Лучший следующий ход: Nf3

        Ответь строго в формате:
        Дебют: <название>
        Лучший следующий ход: <ход в SAN>
        Если информации недостаточно, напиши "Информации недостаточно".
    """

    user_prompt = f"Ходы партии: {moves}"

    response = client.chat.completions.create(
        model="deepseek-llm:7b-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0 
    )

    answer_text = response.choices[0].message.content.strip()
    return answer_text
