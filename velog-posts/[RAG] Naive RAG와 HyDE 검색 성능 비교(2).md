<h2 id="1-실험-결과-요약">1. 실험 결과 요약</h2>
<p>이번 실험에서는 같은 질문 5개를 대상으로 Naive RAG와 HyDE를 비교했다.</p>
<p>비교 기준은 다음과 같다.</p>
<pre><code class="language-text">1. 검색 정확도
2. Retrieval 시간
3. End-to-end 시간
4. LLM 호출 수
5. Embedding 호출 수</code></pre>
<p>이번 실행에서는 최종 답변 생성까지 포함하여 비교했다.
<img alt="" src="https://velog.velcdn.com/images/miy7625/post/65ef282d-8620-4fe7-8a27-dde4ae4c21c3/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/miy7625/post/643fe8a5-b091-4fd0-a64b-93cfb368ea33/image.png" /></p>
<hr />
<h2 id="2-정확도-비교">2. 정확도 비교</h2>
<p>Naive RAG와 HyDE 모두 정확도는 동일하게 좋게 나왔다.</p>
<pre><code class="language-text">Naive
hit_at_k = 1.0
mrr = 1.0

HyDE
hit_at_k = 1.0
mrr = 1.0</code></pre>
<p><code>hit_at_k = 1.0</code>은 질문 5개 모두에서 정답 근거 chunk를 top-k 검색 결과 안에서 찾았다는 뜻이다.</p>
<p><code>mrr = 1.0</code>은 정답 근거 chunk가 모든 질문에서 1번째 검색 결과로 나왔다는 뜻이다.</p>
<p>즉 이번 결과만 보면 검색 정확도 측면에서는 Naive RAG와 HyDE 사이에 차이가 없었다.</p>
<pre><code class="language-text">정확도: Naive = HyDE
검색 순위: Naive = HyDE</code></pre>
<hr />
<h2 id="3-retrieval-시간-비교">3. Retrieval 시간 비교</h2>
<p>Retrieval 시간에서는 큰 차이가 있었다.</p>
<pre><code class="language-text">Naive avg_retrieval_total_sec = 0.4965초
HyDE avg_retrieval_total_sec = 19.7503초</code></pre>
<p>HyDE가 Naive RAG보다 약 40배 느렸다.</p>
<pre><code class="language-text">19.7503 / 0.4965 ≈ 39.8</code></pre>
<p>이 차이가 발생한 이유는 HyDE가 검색 전에 LLM으로 가상 문서를 생성하기 때문이다.</p>
<p>HyDE의 평균 가상 문서 생성 시간은 다음과 같다.</p>
<pre><code class="language-text">HyDE avg_hyde_generation_sec = 19.0611초</code></pre>
<p>즉 HyDE의 retrieval 시간 대부분은 Vector DB 검색 시간이 아니라, LLM이 가상 문서를 생성하는 시간이었다.</p>
<hr />
<h2 id="4-vector-db-검색-시간-비교">4. Vector DB 검색 시간 비교</h2>
<p>Vector DB 검색 자체는 두 방식 모두 매우 빨랐다.</p>
<pre><code class="language-text">Naive avg_vector_search_sec = 0.0126초
HyDE avg_vector_search_sec = 0.0042초</code></pre>
<p>이 차이는 의미 있는 성능 차이라기보다는 실행 순간의 미세한 변동으로 보는 것이 적절하다.</p>
<p>둘 다 Chroma에서 실제 vector search를 수행하는 시간은 거의 0초대였다.</p>
<p>따라서 병목은 Vector DB가 아니라 LLM 호출에 있었다.</p>
<pre><code class="language-text">병목 지점: Chroma 검색 X
병목 지점: HyDE의 가상 문서 생성 O</code></pre>
<hr />
<h2 id="5-end-to-end-시간-비교">5. End-to-end 시간 비교</h2>
<p>최종 답변 생성까지 포함한 전체 처리 시간은 다음과 같았다.</p>
<pre><code class="language-text">Naive avg_end_to_end_sec = 4.7715초
HyDE avg_end_to_end_sec = 24.5073초</code></pre>
<p>HyDE가 질문 1개당 평균 약 20초 더 오래 걸렸다.</p>
<p>전체 실행 시간도 HyDE가 훨씬 길었다.</p>
<pre><code class="language-text">Naive elapsed_sec = 23.858초
HyDE elapsed_sec = 122.537초</code></pre>
<p>즉 사용자 입장에서 체감하는 전체 응답 시간도 Naive RAG가 훨씬 짧다.</p>
<hr />
<h2 id="6-llm-호출-수-비교">6. LLM 호출 수 비교</h2>
<p>LLM 호출 수에서도 차이가 있었다.</p>
<pre><code class="language-text">Naive llm_calls = 5
HyDE llm_calls = 10</code></pre>
<p>Naive RAG는 질문마다 최종 답변 생성을 위해 LLM을 1번 호출한다.</p>
<pre><code class="language-text">Naive RAG
질문 1개당 LLM 호출 1회</code></pre>
<p>반면 HyDE는 질문마다 LLM을 2번 호출한다.</p>
<pre><code class="language-text">HyDE
1. 가상 문서 생성 1회
2. 최종 답변 생성 1회</code></pre>
<p>따라서 질문 5개 기준으로 Naive RAG는 LLM을 5번 호출했고, HyDE는 LLM을 10번 호출했다.</p>
<hr />
<h2 id="7-embedding-호출-수-비교">7. Embedding 호출 수 비교</h2>
<p>Embedding 호출 수는 두 방식 모두 동일했다.</p>
<pre><code class="language-text">Naive embed_query_calls = 5
HyDE embed_query_calls = 5</code></pre>
<p>차이는 무엇을 embedding했는지에 있다.</p>
<pre><code class="language-text">Naive
사용자 질문을 embedding

HyDE
LLM이 생성한 가상 문서를 embedding</code></pre>
<p>즉 retrieval 단계에서 embedding 호출 횟수 자체는 같지만, HyDE는 embedding 전에 LLM을 한 번 더 호출한다.</p>
<hr />
<h2 id="8-질문별-특이점">8. 질문별 특이점</h2>
<p>질문의 핵심 키워드가 원문 법령 표현에 거의 그대로 드러난다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/miy7625/post/1857bfb9-9991-4b4e-821e-b6253a525828/image.png" /></p>
<blockquote>
<p>Q. 지방보조금을 운영비로 교부할 수 있는가?</p>
</blockquote>
<blockquote>
<p>원문에 가까운 핵심 표현:</p>
</blockquote>
<ul>
<li>지방보조금</li>
<li>운영비</li>
<li>교부</li>
</ul>
<h3 id="법령에-명시적-근거가-있는-경우에는-naive-rag가-강하다">법령에 명시적 근거가 있는 경우에는 Naive RAG가 강하다.</h3>
<p>질문 자체에 이미 검색에 필요한 핵심 키워드가 들어 있기 때문이다.</p>
<p>반면 HyDE는 가상 문서를 만들면서 다음처럼 내용을 더 길게 확장합니다.</p>
<pre><code class="language-text">원칙적으로 운영비 목적 교부 불가
법령에 명시적인 지원 규정
조례에 직접적인 운영비 지원 근거
예외적인 요건
지정된 용도 외 사용 불가
집행 및 정산 절차</code></pre>
<p>이 확장은 검색에 도움이 될 수도 있지만, 이 질문에서는 이미 질문 자체가 충분히 명확했기 때문에 불필요한 비용으로 작용했다.</p>
<blockquote>
<ol>
<li>Naive와 HyDE 모두 정확도는 동일하다.</li>
<li>둘 다 rank=1로 정답 근거를 찾았다.</li>
<li>그런데 HyDE retrieval 시간이 약 88배 더 길다.</li>
<li>질문 자체에 원문 핵심 키워드가 이미 들어 있어 Naive가 충분히 잘 작동하는 사례다.</li>
<li>HyDE가 언제 불필요한 비용이 되는지 가장 선명하게 보여준다.</li>
</ol>
</blockquote>
<hr />
<h2 id="9-최종-결론">9. 최종 결론</h2>
<p>이번 로그 기준 결론은 명확하다.</p>
<pre><code class="language-text">정확도: Naive = HyDE
검색 순위: Naive = HyDE
Vector DB 검색 속도: 거의 동일
Retrieval 전체 시간: Naive가 압도적으로 빠름
End-to-end 시간: Naive가 압도적으로 빠름
LLM 호출 수: Naive가 절반</code></pre>
<p>현재 사용한 법령 PDF와 평가 질문 기준에서는 HyDE를 사용할 실익이 크지 않았다.</p>
<p>법령 문서는 사용자의 질문에 포함된 핵심 용어가 원문에도 그대로 등장하는 경우가 많다. 이런 경우에는 질문 자체를 embedding해서 검색하는 Naive RAG만으로도 충분히 좋은 검색 결과를 얻을 수 있다.</p>
<p>반면 HyDE는 가상 문서를 생성하는 LLM 호출이 추가되므로 비용과 시간이 크게 증가한다.</p>
<p>따라서 이번 실험에서는 다음과 같이 정리할 수 있다.</p>
<pre><code class="language-text">Naive RAG가 더 단순하고, 더 빠르며, 정확도도 동일했다.
HyDE는 추가 비용과 시간이 들었지만 검색 정확도 향상은 확인되지 않았다.</code></pre>