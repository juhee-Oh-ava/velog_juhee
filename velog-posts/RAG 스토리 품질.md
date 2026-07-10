<p>RAG를 사용해서 스토리를 만들었는데 스토리 품질이 이상하다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/miy7625/post/cae0feb3-4164-46b2-816e-6541121be423/image.png" /></p>
<p>문제점은 다음과 같다.</p>
<pre><code>
1. mission_description을 그대로 붙이고 뒤에 &quot;는 것입니다&quot;를 붙임
→ &quot;이야기해 보세요는 것입니다&quot; 같은 문장 발생

2. user_result.choice를 selected_keywords로도 넣고 있음
→ &quot;함께 고른 키워드는 남쪽 창이 하늘을 향해 열려 있는 것 같았다.입니다.&quot; 발생</code></pre><p>해결 방법</p>
<pre><code>1. 문장을 억지로 명사화하지 말고 그대로 안내문으로 쓰는 것

2. selected_keywords=[choice] 코드를 수정하자.
-&gt; 때문에 &quot;함께 고른 키워드는 남쪽 창이 하늘을 향해 열려 있는 것 같았다.입니다.&quot; 와 같은 문장이 나오게 된다. 
</code></pre>