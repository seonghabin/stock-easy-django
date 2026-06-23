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

rewritten_content 작성 규칙:
- rewritten_content는 원문 content를 요약한 글이 아니라, 같은 내용을 다시 쓴 재구성 기사 본문이다.
- 원문의 핵심 정보, 주요 수치, 날짜, 인물, 기관, 원인, 전망은 유지한다.
- 단, 원문 문장을 그대로 복사하지 말고 문장 구조와 표현을 바꿔 작성한다.
- 어려운 표현은 일반 투자자가 이해하기 쉬운 표현으로 풀어 쓴다.
- 전체 길이는 원문 content의 약 60~80% 수준을 유지한다.
- 광고 문구, 기자 이메일, 저작권 문구, 불필요한 HTML 흔적은 제외한다.

sentiment 분석 기준:
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

highlight 작성 규칙:
- highlight에는 분석의 근거가 되는 핵심 문장을 뽑는다.
- highlight의 sentence는 반드시 rewritten_content 안에 실제로 포함된 문장을 그대로 사용하라.
- description, content에는 있지만 rewritten_content에는 없는 문장은 사용하지 마라.
- sentence 값을 생성할 때 문장을 바꿔 쓰거나 요약하지 마라.
- highlight.sentence가 rewritten_content에 문자열 그대로 포함되지 않으면 잘못된 응답이다.

difficult_terms 작성 규칙:
- difficult_terms는 반드시 rewritten_content에 실제로 포함된 경제·금융·투자·증권 용어 중에서만 추출한다.
- rewritten_content에 없는 용어는 포함하지 마라.
- 일상어, 직책명, 일반 명사는 포함하지 마라.
- 어려운 경제·투자 용어가 없으면 빈 배열 []로 응답하라.
- 각 용어에는 초보 투자자도 이해할 수 있는 쉬운 설명을 제공한다.

반드시 아래 JSON 형식으로만 응답하라.
마크다운 코드블록은 사용하지 마라.

{{
  "rewritten_content": "원문의 정보량을 유지한 재작성 기사 본문",
  "sentiment": "positive",
  "sentiment_reason": "호재/악재/중립으로 판단한 이유",
  "impact_score": 8.5,
  "impact_reason": "impact_score가 왜 이 점수인지에 대한 설명",
  "highlight": [
    {{
      "sentence": "rewritten_content 안에 실제로 포함된 핵심 문장",
      "reason": "이 문장이 중요한 이유"
    }}
  ],
  "difficult_terms": [
    {{
      "term": "rewritten_content 안에 실제로 포함된 경제·투자 용어",
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