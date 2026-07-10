<p>수정 전
<img alt="" src="https://velog.velcdn.com/images/miy7625/post/194d4a19-998a-4bdc-826d-aaaf249a0400/image.png" /></p>
<p>수정 후
<img alt="" src="https://velog.velcdn.com/images/miy7625/post/6e9a76e6-abb1-4b2e-87f7-a2efb26ac8ef/image.png" /></p>
<p>고민했던 것들</p>
<p>Q2. products 테이블에서 last_synced_at 이 반드시 있어야 하는가?</p>
<p>→ api를 다시 호출하는 기준(가격 변동될때)을 last_synced_at 으로 정했습니다</p>
<p>Q3. Unique index 왜 필요할까? </p>
<p>Unique indexes 가 없으면 같은 상품으로 인식하지 못한다. -&gt; 만약 장바구니에 똑같은 상품을 담아도 Unique index가 없으면 같은 상품으로 인식하지 못해 2개의 데이터가 저장되고 수량이 올라가지 않는다.</p>
<p>중요한 전제 : DB 는 “같은 상품인지”를 스스로 판단하지 못한다.
쿠팡 상품: (platform_id=1, external_pr.[oduct_id=12345)
두 요청이 거의 동시에 들어옴 -&gt; 두 트랜잭션이 동시에 실행됨.(SELECT) (이 시점에는 DB는 “없다”고 두 번 대답한다)
If unique index가 없을 때: 두 트랜잭션이 각각 INSERT 되면 DB 입장에서는 문제없고, 규칙 위반 아니고, 에러 아님.
If unique index가 있을 때: 두 트랜잭션이 각각 INSERT 되면 DB 입장에서는 트랜잭션 A 는 성공, B는 실패.</p>
<p>여기서 굳이 unique index 쓰지 않고 그냥 히스토리 테이블에서 과거에 구매했던 제품코드와  플랫폼 id를 product 테이블의 제품코드와 플랫폼id를 비교해서 같으면 카운팅하는 식으로 로직을 짜서 같은 제품 갯수 셀 수는 없을까? 굳이 db에서까지 unique index로 해야하나?</p>
<p>셀 수는 있다. 근데 ‘같은 제품이 여러 row로 존재하는 상황’을 허용하는 순간 설계가 망가진다.”</p>
<p><strong>count는 히스토리에서 하면 되잖아?”에 대한 핵심 반박</strong></p>
<p>이 말 자체는 맞아 👌</p>
<p>근데 전제가 있음</p>
<p>“products는 ‘유일한 상품 1행’이 보장되어 있어야 한다”</p>
<p>→ 우리 서비스는 외부 플랫폼 api를 조회해서 상품을 가져오는 오픈 마켓 개념. 그렇다면 (같은 플랫폼 + 같은 상품_id) 지만 가격이 다른 경우에는 동일 상품으로 볼 것 인가? 다른 상품으로 볼 것인가? </p>
<ol>
<li><p>다른 상품으로 봐야 한다. → 몇 개월 이내에 중복 구매한 상품을 바로 결제할 때 가격이 다르면 내가 원하는 상품이 아닐 수도 있으니까</p>
</li>
<li><p>같은 상품으로 봐야 한다 →</p>
</li>
</ol>
<p><strong>정리 (이걸로 끝내도 됨)</strong></p>
<p><strong>지금 설계 유지 시</strong></p>
<ul>
<li>products = 상품 마스터</li>
<li>(platform_id, external_product_id ) → UNIQUE 필수</li>
</ul>
<p><strong>가격 때문에 중복이 필요하다면</strong></p>
<ul>
<li>테이블 분리</li>
<li>offers / listings / price_history 생성(가격 칼럼 추가)</li>
<li>products는 유일성 유지</li>
</ul>
<p>그럼 url은 상품 상세 페이지의 고유한 값이니까 platform_id + product_url 로 unique index를 하면 괜찮지 않을까? </p>
<p>→ url 은 다른데 파라미터 순서가 다른 상황은 같은 데이터지만 url 이 다르니깐 데이터 무결성이 확보되지 않는다고 생각했습니다. 예를 들어서 같은 플랫폼 + 같은 상품인데 가격도 동일하지만 판매처가 다르면 같은 상품으로 봐야할까요? 다른 상품으로 봐야할까요? 이상황일때는 url은 다르지만 그냥 “같은 상품”으로 봐야된다고 생각했습니다.</p>
<p>그래서 상품 productId는 쇼핑몰 api 응답 데이터에서 받아오고 옵션 정보는 추가로 제공해주지 않아서 mcp + playwright 로 json을 생성해서 json + productId 조합으로 즐겨찾기(매크로) flow 가능할 것 같다. </p>
<p>방향을 바꿔서 이렇게 하기로 했습니다!</p>
<pre><code>매우 통찰력 있는 질문입니다. 쇼핑몰 시스템 설계에서 가장 고민되는 &quot;상품(Product) vs 판매조건(Offer)&quot; 문제네요.

결론부터 말씀드리면, DB에서는 &quot;다른 상품&quot;으로 저장하고, 사용자에게 보여줄 때만 &quot;같은 상품&quot;처럼 묶어서 보여주는 것이 에이전트 시스템에서는 훨씬 안전하고 유리합니다.

이유를 설명해 드릴게요.

1. 에이전트에게 &quot;URL&quot;은 &quot;주소지&quot;입니다.
사용자가 &quot;이거 사줘&quot;라고 했을 때, AI는 그 URL로 찾아가서 구매 버튼을 누릅니다.

상품 A: 판매자 '철수네' (URL: .../products/111) - 평점 5.0
상품 B: 판매자 '영희네' (URL: .../products/222) - 평점 1.0 (사기꾼)
만약 이 둘을 DB에서 합쳐버려서 (product_id: 1 ➡️ URL은 아무거나 하나 저장), AI가 실수로 영희네 링크로 들어가서 사버리면 문제가 됩니다. 가격이 같아도 **&quot;누구한테 사는지(URL)&quot;**는 구매 대행에서 매우 중요한 정보입니다.

2. &quot;같은 상품으로 보고 싶다&quot;는 건 &quot;UI의 영역&quot;입니다.
사용자 요구사항(&quot;같은 상품으로 봐야 된다&quot;)은 **&quot;화면에서 보거나 검색할 때 중복해서 뜨지 않았으면 좋겠다&quot;**는 뜻일 겁니다. 이건 DB를 합칠 게 아니라, 데이터를 가져와서 보여줄 때 처리하면 됩니다.

DB: Row 1 (URL A), Row 2 (URL B) 따로 저장 (안전 확보)
Logic: &quot;어? 이름이랑 가격이 똑같네? 화면에는 하나만 보여주고, 클릭하면 '판매처 2곳'이라고 알려주자.&quot;
3. 결론 및 제안
products 테이블은 **&quot;구매 가능한 좌표(URL)&quot;**를 기준으로 하는 것이 가장 깔끔합다. 사용자의 의도(&quot;같은 상품 처리&quot;)는 나중에 개발 단계에서 **&quot;이름이 같으면 그룹핑(Grouping)&quot;**하는 로직으로 푸는 것을 추천합니다.

DB는 있는 그대로(URL 기준) 저장하는 게 맞습니다.</code></pre>