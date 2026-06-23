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

분석 기준:
- sentiment는 뉴스가 투자 심리에 미치는 방향성을 의미한다.
- sentiment는 반드시 positive, neutral, negative 중 하나로 응답한다.
- sentiment_reason에는 왜 해당 감정으로 판단했는지 설명한다.

impact_score 기준:
- 0.0 ~ 2.0: 시장 영향 거의 없음
- 2.1 ~ 4.0: 일부 종목/업종에 제한적 영향
- 4.1 ~ 6.0: 관련 업종에 중간 수준 영향
- 6.1 ~ 8.0: 시장 또는 주요 종목에 뚜렷한 영향
- 8.1 ~ 10.0: 시장 전반 또는 핵심 대형주에 매우 강한 영향

impact_reason에는 위 기준 중 어떤 이유로 해당 점수를 부여했는지 설명한다.

highlight에는 분석의 근거가 되는 핵심 문장을 원문 또는 재작성된 문장에서 뽑고,
각 문장이 왜 중요한지 설명한다.

difficult_terms에는 초보 투자자가 이해하기 어려울 수 있는 용어를 뽑고,
각 용어의 쉬운 설명을 제공한다.

반드시 아래 JSON 형식으로만 응답하라.
마크다운 코드블록은 사용하지 마라.

{{
  "rewritten_content": "뉴스 내용을 쉬운 문장으로 재작성",
  "sentiment": "positive",
  "sentiment_reason": "호재/악재/중립으로 판단한 이유",
  "impact_score": 8.5,
  "impact_reason": "impact_score가 왜 이 점수인지에 대한 설명",
  "highlight": [
    {{
      "sentence": "분석 근거가 되는 핵심 문장",
      "reason": "이 문장이 중요한 이유"
    }}
  ],
  "difficult_terms": [
    {{
      "term": "어려운 용어",
      "explanation": "초보 투자자도 이해할 수 있는 설명"
    }}
  ],
  "check_points": [
    "투자자가 추가로 확인해야 할 점1",
    "투자자가 추가로 확인해야 할 점2"
  ]
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