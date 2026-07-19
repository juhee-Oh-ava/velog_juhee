<h2 id="1-rag란-무엇인가">1. RAG란 무엇인가?</h2>
<p>RAG는 Retrieval-Augmented Generation의 약자로, <strong>검색 기반 생성 방식</strong>이다.</p>
<p>LLM이 질문에 바로 답변하도록 하는 것이 아니라, 먼저 외부 문서에서 관련 정보를 검색한 뒤, 그 검색 결과를 프롬프트에 넣어 최종 답변을 생성한다.</p>
<p>기본 흐름은 다음과 같다.</p>
<pre><code class="language-text">사용자 질문
→ 관련 문서 검색
→ 검색 결과를 프롬프트에 삽입
→ LLM이 최종 답변 생성</code></pre>
<p>이 방식은 LLM이 가지고 있는 내부 지식에만 의존하지 않고, 사용자가 준비한 문서나 데이터베이스를 근거로 답변할 수 있게 해준다.</p>
<h2 id="2-naive-rag란">2. Naive RAG란?</h2>
<p>Naive RAG는 가장 기본적인 RAG 구조이다.</p>
<p>미리 문서를 임베딩하여 Vector DB에 저장해두고, 사용자의 질문이 들어오면 질문 자체를 임베딩한 뒤 Vector DB에서 유사한 문서를 검색한다.</p>
<pre><code class="language-text">문서
→ chunk 분할
→ embedding
→ Vector DB 저장

사용자 질문
→ 질문 embedding
→ Vector DB retrieval
→ 검색 결과 기반 답변 생성</code></pre>
<p>즉 Naive RAG에서는 <strong>사용자의 질문 자체가 검색 쿼리</strong>가 된다.</p>
<h2 id="3-advanced-rag의-주요-개선-지점">3. Advanced RAG의 주요 개선 지점</h2>
<p>Advanced RAG는 기본 RAG 구조의 여러 단계에 추가 기법을 적용한다.</p>
<p>대표적으로 다음 단계에서 개선이 가능하다.</p>
<pre><code class="language-text">Indexing
Query Translation
Routing
Query Construction
Retrieval
Generation</code></pre>
<p>예를 들어 인덱싱 단계에서는 다음과 같은 점을 고려할 수 있다.</p>
<ul>
<li>문서를 적절한 크기로 chunking하기</li>
<li>문서의 카테고리, 페이지, 출처 등을 metadata로 저장하기</li>
<li>검색 품질을 높이기 위해 문서 자체의 품질을 개선하기</li>
</ul>
<p>RAG의 성능은 단순히 LLM 성능만으로 결정되지 않는다.</p>
<pre><code class="language-text">문서 품질
검색 정확도
최종 생성 품질</code></pre>
<p>이 중 어디가 병목인지 파악하는 것이 중요하다.</p>
<h2 id="4-hyde란">4. HyDE란?</h2>
<p>HyDE는 Hypothetical Document Embeddings의 약자이다.</p>
<p>사용자의 질문을 바로 검색에 사용하지 않고, 먼저 LLM에게 <strong>그 질문에 대한 가상의 이상적인 답변 문서</strong>를 생성하게 한다.</p>
<p>그 다음 이 가상 문서를 임베딩하여 Vector DB에서 검색한다.</p>
<pre><code class="language-text">사용자 질문
→ LLM이 가상 문서 생성
→ 가상 문서 embedding
→ Vector DB retrieval
→ 검색 결과 기반 최종 답변 생성</code></pre>
<p>HyDE의 핵심 가정은 다음과 같다.</p>
<blockquote>
<p>짧은 사용자 질문보다, LLM이 생성한 답변 형태의 문서가 실제 문서와 의미적으로 더 가까울 수 있다.</p>
</blockquote>
<p>따라서 HyDE는 사용자의 질문이 짧거나 추상적일 때 검색 성능을 높이는 데 도움이 될 수 있다.</p>
<h2 id="5-hyde의-동작-과정">5. HyDE의 동작 과정</h2>
<p>HyDE는 크게 세 단계로 나눌 수 있다.</p>
<pre><code class="language-text">1. 가상 문서 생성
2. 가상 문서 임베딩 및 검색
3. 검색 결과 기반 최종 답변 생성</code></pre>
<p>첫 번째 단계에서는 LLM을 사용해 질문에 대한 가상의 답변 문서를 만든다.</p>
<p>두 번째 단계에서는 그 가상 문서를 임베딩하고, Vector DB에서 유사한 실제 문서를 검색한다.</p>
<p>세 번째 단계에서는 검색된 문서를 context로 사용해 최종 답변을 생성한다.</p>
<h2 id="6-hyde의-장점과-주의점">6. HyDE의 장점과 주의점</h2>
<p>HyDE의 장점은 질문의 의미를 자연스럽게 확장할 수 있다는 점이다.</p>
<p>예를 들어 사용자의 질문이 짧더라도 LLM이 관련 표현을 풍부하게 포함한 가상 문서를 생성하면, Vector DB 검색에서 더 좋은 문서를 찾을 가능성이 있다.</p>
<p>하지만 주의할 점도 있다.</p>
<ul>
<li>LLM이 만든 가상 문서의 품질이 낮으면 검색 품질도 낮아질 수 있다.</li>
<li>Naive RAG보다 LLM 호출이 1회 이상 추가된다.</li>
<li>비용과 응답 시간이 증가한다.</li>
<li>법령처럼 원문 용어가 중요한 도메인에서는 오히려 Naive RAG가 더 잘 맞을 수도 있다.</li>
</ul>
<p>즉 HyDE가 항상 Naive RAG보다 좋은 것은 아니다.</p>
<h2 id="7-문서-인덱싱-결과">7. 문서 인덱싱 결과</h2>
<p>실습에서는 법령 PDF를 Chroma Vector DB에 저장했다.</p>
<p>처음에는 다음과 같이 chunk 크기를 작게 설정했다.</p>
<pre><code class="language-python">text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,      # 문서를 300자 단위로 분할
    chunk_overlap=100,   # 앞뒤 문맥 유지를 위해 100자 중복
)</code></pre>
<p>하지만 chunk가 너무 많이 생성되어 임베딩 API 호출 제한에 걸렸다.</p>
<p>그래서 다음과 같이 수정했다.</p>
<pre><code class="language-python">text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,     # 법령 조문이 너무 잘게 쪼개지지 않도록 chunk 크기를 키움
    chunk_overlap=150,   # 문맥 단절을 줄이기 위해 일부 텍스트를 겹치게 유지
)</code></pre>
<p>인덱싱 결과는 다음과 같았다.</p>
<pre><code class="language-text">pages=15, chunks=41, indexed=41</code></pre>
<p>각 의미는 다음과 같다.</p>
<pre><code class="language-text">pages=15
PDF에서 15페이지를 읽었다는 뜻

chunks=41
PDF 텍스트를 41개의 조각으로 나누었다는 뜻

indexed=41
41개의 chunk가 Chroma Vector DB에 저장되었다는 뜻</code></pre>
<p><code>indexed=41</code>이므로 41개의 문서 조각이 임베딩되어 Vector DB에 저장된 상태라고 볼 수 있다.</p>
<h2 id="8-hyde에서-가상-문서를-임베딩하는-함수">8. HyDE에서 가상 문서를 임베딩하는 함수</h2>
<p>HyDE에서는 먼저 LLM이 만든 가상 문서를 검색용 임베딩으로 변환해야 한다.</p>
<pre><code class="language-python">def embed_hypothetical_document(
    vector_store: Chroma,
    hypothetical_document: str,
    timings: StepTimings,
) -&gt; list[float]:
    &quot;&quot;&quot;HyDE 2단계: 생성된 가상 문서를 검색용 query embedding으로 변환한다.&quot;&quot;&quot;

    # 현재 시간을 기록하여 embedding 소요 시간을 측정한다.
    step_started_at = now()

    # 가상 문서를 embedding 벡터로 변환한다.
    query_embedding = vector_store._embedding_function.embed_query(hypothetical_document)

    # 가상 문서 embedding에 걸린 시간을 기록한다.
    timings.hyde_embedding_sec = elapsed_since(step_started_at)

    # 생성된 query embedding을 반환한다.
    return query_embedding</code></pre>
<p>이 함수는 실제 검색을 수행하지 않는다.</p>
<p>역할은 오직 다음 하나이다.</p>
<pre><code class="language-text">가상 문서 문자열
→ embedding vector</code></pre>
<h2 id="9-vector-db에서-검색하는-함수">9. Vector DB에서 검색하는 함수</h2>
<p>이미 만들어진 query embedding을 사용해 Chroma에서 top-k 문서를 검색한다.</p>
<pre><code class="language-python">def search_with_query_embedding(
    vector_store: Chroma,
    query_embedding: list[float],
    k: int,
    timings: StepTimings,
) -&gt; list[tuple[Any, float]]:
    &quot;&quot;&quot;공통 vector search 단계: 이미 만든 query embedding으로 Chroma에서 top-k 문서를 검색한다.&quot;&quot;&quot;

    # 현재 시간을 기록하여 Vector DB 검색 시간을 측정한다.
    step_started_at = now()

    # 미리 계산된 query embedding을 사용해 Chroma에서 top-k 문서를 검색한다.
    results = query_chroma_with_embedding(vector_store, query_embedding, k)

    # 순수 Vector DB 검색에 걸린 시간을 기록한다.
    timings.vector_search_sec = elapsed_since(step_started_at)

    # 검색 결과를 반환한다.
    return results</code></pre>
<p>여기서 <code>k</code>는 검색 결과를 몇 개 가져올지 정하는 값이다.</p>
<p>예를 들어 <code>k=4</code>이면 가장 유사한 문서 4개를 가져온다.</p>
<pre><code class="language-text">top-k = 유사도 기준 상위 k개 검색 결과</code></pre>
<h2 id="10-왜-결과를-튜플로-반환할까">10. 왜 결과를 튜플로 반환할까?</h2>
<p>검색 결과는 다음 형태로 반환된다.</p>
<pre><code class="language-python">list[tuple[Any, float]]</code></pre>
<p>즉 구조는 다음과 같다.</p>
<pre><code class="language-text">[
  (Document, score),
  (Document, score),
  ...
]</code></pre>
<p>여기서 <code>Document</code>에는 실제 문서 내용과 metadata가 들어 있다.</p>
<pre><code class="language-python">doc.page_content  # 문서의 실제 텍스트
doc.metadata      # 페이지, 출처 등 부가 정보
score             # query와 문서 사이의 거리 또는 유사도 점수</code></pre>
<p>주의할 점은 Chroma에서 반환되는 <code>score</code>가 일반적인 “높을수록 좋은 유사도”가 아닐 수 있다는 것이다.</p>
<p>Chroma의 distance score는 보통 <strong>낮을수록 더 가까운 결과</strong>로 해석한다.</p>
<p>출력이나 JSON 저장이 필요할 때는 다음처럼 dictionary 형태로 바꿀 수 있다.</p>
<pre><code class="language-python">def serialize_results(results: list[tuple[Any, float]]) -&gt; list[dict[str, Any]]:
    &quot;&quot;&quot;LangChain 검색 결과를 JSON 저장과 출력에 적합한 dict 목록으로 바꾼다.&quot;&quot;&quot;

    return [
        {
            # 검색 점수를 소수점 4자리로 반올림한다.
            &quot;score&quot;: round(result_score, 4),

            # 페이지 번호, 원본 파일명 등 metadata를 저장한다.
            &quot;metadata&quot;: doc.metadata,

            # 실제 문서 내용을 저장한다.
            &quot;document&quot;: doc.page_content,
        }
        for doc, result_score in results
    ]</code></pre>
<p>즉 내부 처리에서는 <code>(Document, score)</code> 튜플을 사용하고, 출력이나 저장 단계에서는 dictionary로 변환한다.</p>
<h2 id="11-hyde-retrieval-전체-흐름">11. HyDE Retrieval 전체 흐름</h2>
<p>HyDE retrieval 전체 함수는 다음과 같다.</p>
<pre><code class="language-python">def retrieve_hyde(
    vector_store: Chroma,
    llm: ChatGoogleGenerativeAI,
    stats: RetrievalStats,
    question: str,
    k: int,
) -&gt; tuple[str, list[tuple[Any, float]], StepTimings]:
    &quot;&quot;&quot;HyDE retrieval 전체 흐름의 단계별 시간을 측정한다.&quot;&quot;&quot;

    # 단계별 시간을 저장할 객체를 만든다.
    timings = StepTimings()

    # HyDE retrieval 전체 시작 시간을 기록한다.
    retrieval_started_at = now()

    # Retrieval step 1: 질문을 바탕으로 검색용 가상 문서를 생성한다.
    step_started_at = now()
    hypothetical_document = generate_hypothetical_document(llm, stats, question)
    timings.hyde_generation_sec = elapsed_since(step_started_at)

    # Retrieval step 2: 가상 문서를 query embedding으로 변환한다.
    query_embedding = embed_hypothetical_document(vector_store, hypothetical_document, timings)

    # Retrieval step 3: query embedding으로 Chroma에서 top-k 문서를 검색한다.
    results = search_with_query_embedding(vector_store, query_embedding, k, timings)

    # Retrieval total: HyDE 생성, 임베딩, vector search까지의 전체 retrieval 시간을 기록한다.
    timings.retrieval_total_sec = elapsed_since(retrieval_started_at)

    # 가상 문서, 검색 결과, 시간 측정 결과를 반환한다.
    return hypothetical_document, results, timings</code></pre>
<p>이 함수에서 측정하는 시간은 다음과 같다.</p>
<pre><code class="language-text">hyde_generation_sec
LLM이 가상 문서를 생성하는 데 걸린 시간

hyde_embedding_sec
가상 문서를 embedding하는 데 걸린 시간

vector_search_sec
Chroma Vector DB에서 검색하는 데 걸린 시간

retrieval_total_sec
HyDE retrieval 전체 시간</code></pre>
<h2 id="12-최종-답변-생성">12. 최종 답변 생성</h2>
<p>검색된 문서들을 context로 묶은 뒤 LLM에게 최종 답변을 생성하도록 요청한다.</p>
<pre><code class="language-python">def build_context(results: list[tuple[Any, float]]) -&gt; str:
    &quot;&quot;&quot;검색된 문서들의 본문만 모아 최종 답변 생성용 context 문자열을 만든다.&quot;&quot;&quot;

    # 검색된 문서들의 page_content만 모아 하나의 context로 만든다.
    return &quot;\n\n&quot;.join(doc.page_content for doc, _ in results)</code></pre>
<pre><code class="language-python">def generate_final_answer(
    llm: ChatGoogleGenerativeAI,
    stats: RetrievalStats,
    question: str,
    results: list[tuple[Any, float]],
) -&gt; str:
    &quot;&quot;&quot;검색 결과를 근거로 최종 답변을 생성한다. context에 없는 내용은 답하지 않도록 지시한다.&quot;&quot;&quot;

    # 최종 답변 생성을 위해 LLM을 한 번 호출하므로 호출 횟수를 증가시킨다.
    stats.llm_calls += 1

    # 검색된 문서들을 하나의 context로 합친다.
    context = build_context(results)

    # 검색 결과에 근거해서만 답변하도록 프롬프트를 구성한다.
    prompt = f&quot;&quot;&quot;다음 검색 결과를 바탕으로 질문에 답변하세요.
검색 결과의 정보를 최대한 사용하고, 검색 결과에 없는 정보는 답변하지 마세요.
법령 조문 번호나 페이지 정보가 보이면 함께 언급하세요.

검색 결과:
{context}

질문: {question}

답변:&quot;&quot;&quot;

    # LLM에게 최종 답변 생성을 요청한다.
    response = llm.invoke(prompt)

    # 응답 content를 문자열로 변환하여 반환한다.
    return stringify_llm_content(response.content)</code></pre>
<h2 id="13-naive-rag와-hyde의-시간-측정-기준">13. Naive RAG와 HyDE의 시간 측정 기준</h2>
<p>Naive RAG에서는 다음 시간을 따로 측정한다.</p>
<pre><code class="language-text">query_embedding_sec
사용자 질문을 embedding하는 데 걸린 시간

vector_search_sec
Chroma Vector DB에서 검색하는 데 걸린 시간

retrieval_total_sec
질문 embedding과 vector search를 합친 전체 retrieval 시간</code></pre>
<p>HyDE에서는 다음 시간을 따로 측정한다.</p>
<pre><code class="language-text">hyde_generation_sec
LLM이 가상 문서를 생성하는 데 걸린 시간

hyde_embedding_sec
가상 문서를 embedding하는 데 걸린 시간

vector_search_sec
Chroma Vector DB에서 검색하는 데 걸린 시간

retrieval_total_sec
가상 문서 생성, embedding, vector search를 합친 전체 retrieval 시간</code></pre>
<p>최종 답변 생성까지 측정할 경우 다음 항목도 추가된다.</p>
<pre><code class="language-text">answer_generation_sec
검색 결과를 바탕으로 최종 답변을 생성하는 시간

end_to_end_sec
사용자 질문 입력부터 최종 답변 생성까지 걸린 전체 시간</code></pre>
<h2 id="14-naive-rag와-hyde의-차이">14. Naive RAG와 HyDE의 차이</h2>
<p>Naive RAG는 질문 자체를 검색에 사용한다.</p>
<pre><code class="language-text">질문
→ 질문 embedding
→ Vector DB 검색</code></pre>
<p>HyDE는 질문으로 가상 문서를 만든 뒤 검색에 사용한다.</p>
<pre><code class="language-text">질문
→ 가상 문서 생성
→ 가상 문서 embedding
→ Vector DB 검색</code></pre>
<p>따라서 HyDE는 Naive RAG보다 LLM 호출이 추가된다.</p>
<pre><code class="language-text">Naive RAG retrieval
LLM 호출 없음
embedding 호출 1회

HyDE retrieval
LLM 호출 1회
embedding 호출 1회</code></pre>
<p>최종 답변 생성까지 포함하면 다음과 같다.</p>
<pre><code class="language-text">Naive RAG + answer generation
LLM 호출 1회
embedding 호출 1회

HyDE + answer generation
LLM 호출 2회
embedding 호출 1회</code></pre>
<h2 id="15-보충-설명-시간-측정-구조">15. 보충 설명: 시간 측정 구조</h2>
<p>아래 그림처럼 보면 이해하기 쉽다.</p>
<pre><code class="language-text">Naive RAG

사용자 질문
   │
   ▼
[query_embedding_sec]
   │
   ▼
[vector_search_sec]
   │
   ▼
검색 결과

retrieval_total_sec = query_embedding_sec + vector_search_sec</code></pre>
<pre><code class="language-text">HyDE

사용자 질문
   │
   ▼
[hyde_generation_sec]
   │
   ▼
가상 문서
   │
   ▼
[hyde_embedding_sec]
   │
   ▼
query embedding
   │
   ▼
[vector_search_sec]
   │
   ▼
검색 결과

retrieval_total_sec = hyde_generation_sec + hyde_embedding_sec + vector_search_sec</code></pre>
<p>이처럼 Vector DB 자체의 검색 속도만 비교하려면 <code>vector_search_sec</code>를 보면 된다.</p>
<p>하지만 사용자가 실제로 체감하는 검색 준비 시간까지 비교하려면 <code>retrieval_total_sec</code>를 봐야 한다.</p>
<p>최종 답변 생성까지 포함한 서비스 관점의 시간은 <code>end_to_end_sec</code>를 보면 된다.</p>
<h2 id="16-마무리-정리">16. 마무리 정리</h2>
<p>Naive RAG는 사용자의 질문을 그대로 embedding하여 Vector DB에서 검색하는 가장 기본적인 방식이다.</p>
<p>HyDE는 질문을 바로 검색하지 않고, 먼저 LLM이 생성한 가상 문서를 검색 쿼리로 사용하는 방식이다.</p>
<p>HyDE는 질문의 의미를 확장해 검색 품질을 높일 수 있지만, LLM 호출이 추가되기 때문에 비용과 시간이 증가한다.</p>
<p>따라서 RAG 실험에서는 단순히 전체 시간만 볼 것이 아니라 다음 지표를 나누어 측정하는 것이 좋다.</p>
<pre><code class="language-text">query_embedding_sec
hyde_generation_sec
hyde_embedding_sec
vector_search_sec
retrieval_total_sec
answer_generation_sec
end_to_end_sec</code></pre>
<p>또한 검색 정확도를 제대로 평가하려면 단순 키워드 기반 평가보다, 질문별 정답 문서나 정답 조문을 지정한 golden dataset을 만드는 것이 더 좋다.</p>
<p>결론적으로 현재 단계에서는 먼저 Naive RAG와 HyDE의 retrieval 시간을 분리 측정하고, 이후 golden dataset을 만들어 검색 정확도를 더 엄밀하게 비교하는 방향으로 발전시키면 된다.</p>
<blockquote>
<p>참조</p>
</blockquote>
<ul>
<li><a href="https://wikidocs.net/288622">https://wikidocs.net/288622</a></li>
<li>랭체인과 랭그래프로 구현하는 RAG, AI 에이전트 실전 입문</li>
</ul>