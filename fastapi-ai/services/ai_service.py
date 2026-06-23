import json
import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.4-mini")


SYSTEM_PROMPT = """
너는 주식 뉴스 분석 전문가다.

입력된 뉴스 제목과 본문을 바탕으로
개인 투자자가 이해하기 쉽게 분석하라.

반드시 아래 JSON 형식으로만 응답하라.
마크다운 코드블록은 사용하지 마라.


{{
  "rewritten_content": "뉴스 내용을 쉬운 문장으로 재작성",
  "sentiment": "positive | neutral | negative",
  "impact_score": 0.0,
  "impact_reason": "주가 또는 시장에 영향을 줄 수 있는 이유",
  "difficult_terms": ["어려운 용어1", "어려운 용어2"],
  "check_points": ["투자자가 확인할 점1", "투자자가 확인할 점2"]
}}

"""

USER_PROMPT = """
뉴스 제목:
{title}

뉴스 본문:
{content}
"""


def analyze_news_with_ai(title: str, content: str) -> dict:
   
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        model=MODEL_NAME,
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", USER_PROMPT),
        ]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "title": title,
            "content": content,
        }
    )

    return json.loads(response.content)