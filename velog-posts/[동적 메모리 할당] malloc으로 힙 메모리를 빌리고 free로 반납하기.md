<h2 id="1-메모리-사용하기">1. 메모리 사용하기</h2>
<p>C 언어에서는 포인터를 이용해 원하는 만큼 메모리 공간을 할당받아 사용할 수 있다.</p>
<p>이때 주로 사용하는 패턴은 다음과 같다.</p>
<pre><code class="language-c">malloc -&gt; 사용 -&gt; free</code></pre>
<p>즉, <code>malloc</code>으로 메모리를 할당받고 필요한 작업을 한 뒤, 더 이상 사용하지 않으면 <code>free</code>로 메모리를 해제한다.</p>
<hr />
<h2 id="2-메모리-할당하기">2. 메모리 할당하기</h2>
<p>메모리를 직접 사용하려면 <code>malloc</code> 함수로 사용할 메모리 공간을 확보해야 한다.</p>
<pre><code class="language-c">포인터 = malloc(크기);</code></pre>
<p><code>malloc</code> 함수의 원형은 다음과 같다.</p>
<pre><code class="language-c">void *malloc(size_t size);</code></pre>
<p><code>malloc</code>은 메모리 할당에 성공하면 할당된 메모리의 시작 주소를 반환하고, 실패하면 <code>NULL</code>을 반환한다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main(void)
{
    int *numPtr = malloc(sizeof(int)); // int 크기만큼 힙 메모리 할당

    if (numPtr == NULL) // malloc 실패 여부 확인
    {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    *numPtr = 10; // 포인터를 역참조하여 값 저장

    printf(&quot;%d\n&quot;, *numPtr); // 포인터를 역참조하여 값 출력

    free(numPtr); // 할당받은 메모리 해제

    return 0;
}</code></pre>
<p>여기서 <code>numPtr</code>이라는 포인터 변수 자체는 스택에 생성된다.</p>
<p>하지만 <code>malloc</code>으로 할당받은 메모리 공간은 힙 영역에 생성된다.</p>
<p>스택에 생성된 일반 변수는 함수가 끝나면 자동으로 정리되지만, <code>malloc</code>으로 할당받은 힙 메모리는 자동으로 해제되지 않는다.</p>
<p>따라서 반드시 <code>free</code> 함수를 사용해 직접 해제해야 한다.</p>
<hr />
<h2 id="3-메모리에-값-저장하기">3. 메모리에 값 저장하기</h2>
<p><code>malloc</code>으로 할당받은 메모리에 값을 저장하려면 포인터를 역참조해야 한다.</p>
<pre><code class="language-c">*numPtr = 10;</code></pre>
<p>여기서 <code>numPtr</code>은 주소를 저장하고 있고, <code>*numPtr</code>은 그 주소에 있는 실제 공간을 의미한다.</p>
<p>출력할 때도 마찬가지로 포인터를 역참조해서 값을 가져온다.</p>
<pre><code class="language-c">printf(&quot;%d\n&quot;, *numPtr);</code></pre>
<p>정리하면 다음과 같다.</p>
<pre><code class="language-c">int *numPtr = malloc(sizeof(int)); // int 하나를 저장할 공간 확보

*numPtr = 10; // 할당받은 공간에 10 저장

printf(&quot;%d\n&quot;, *numPtr); // 저장된 값 출력

free(numPtr); // 메모리 해제</code></pre>
<hr />
<h2 id="4-memset-함수로-메모리-초기화하기">4. memset 함수로 메모리 초기화하기</h2>
<p><code>malloc</code>으로 메모리를 할당받으면 그 공간 안에 어떤 값이 들어 있는지 알 수 없다.</p>
<p>이전에 사용되던 값이 남아 있을 수 있는데, 이를 흔히 쓰레기 값이라고 한다.</p>
<p>이때 <code>memset</code> 함수를 사용해 메모리를 특정 값으로 채울 수 있다.</p>
<pre><code class="language-c">memset(포인터, 설정할 값, 크기);</code></pre>
<p>예시는 다음과 같다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;

int main(void)
{
    int *numPtr = malloc(sizeof(int)); // int 크기만큼 메모리 할당

    if (numPtr == NULL)
    {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    memset(numPtr, 0, sizeof(int)); // 할당받은 메모리를 0으로 초기화

    printf(&quot;%d\n&quot;, *numPtr); // 0 출력

    free(numPtr); // 메모리 해제

    return 0;
}</code></pre>
<p><code>malloc</code> 함수가 방을 빌리는 역할이라면, <code>memset</code> 함수는 빌린 방을 깨끗하게 청소하거나 도색하는 역할이라고 볼 수 있다.</p>
<p>실제로는 메모리를 <code>0</code>으로 초기화할 때 자주 사용한다.</p>
<hr />
<h2 id="5-memset은-왜-1바이트-단위로-동작할까">5. memset은 왜 1바이트 단위로 동작할까?</h2>
<p><code>memset</code>은 메모리를 바이트 단위로 채우는 함수이다.</p>
<p>즉, <code>int</code>, <code>double</code>, <code>struct</code> 같은 자료형 단위로 값을 넣는 것이 아니라 메모리의 가장 작은 단위인 1바이트씩 값을 채운다.</p>
<p>예를 들어 <code>int</code>가 4바이트인 환경에서 다음 코드를 실행한다고 생각해보자.</p>
<pre><code class="language-c">int num;
memset(&amp;num, 0, sizeof(int));</code></pre>
<p><code>sizeof(int)</code>가 4라면, <code>memset</code>은 <code>num</code>이 차지하는 4바이트를 다음처럼 채운다.</p>
<pre><code class="language-text">초기 상태

[ ? ][ ? ][ ? ][ ? ]

memset(&amp;num, 0, sizeof(int)) 실행 후

[ 0 ][ 0 ][ 0 ][ 0 ]</code></pre>
<p>그래서 정수형 변수 전체가 0으로 초기화된다.</p>
<p>하지만 주의할 점이 있다.</p>
<p><code>memset</code>은 바이트 단위로 값을 채우기 때문에 다음처럼 사용하는 것은 위험할 수 있다.</p>
<pre><code class="language-c">int num;
memset(&amp;num, 1, sizeof(int));</code></pre>
<p>이 코드는 <code>num</code>에 정수 <code>1</code>을 넣는다는 뜻이 아니다.</p>
<p>실제로는 4바이트를 모두 <code>1</code>로 채운다.</p>
<pre><code class="language-text">[ 1 ][ 1 ][ 1 ][ 1 ]</code></pre>
<p>따라서 <code>int</code> 값이 정확히 <code>1</code>이 되는 것이 아니다.</p>
<p>그래서 <code>memset</code>은 보통 메모리를 <code>0</code>으로 초기화할 때 많이 사용한다.</p>
<hr />
<h2 id="6-null-포인터">6. NULL 포인터</h2>
<p><code>NULL</code>이 들어 있는 포인터를 널 포인터라고 한다.</p>
<p>널 포인터는 아무것도 가리키지 않는 상태이다.</p>
<pre><code class="language-c">int *numPtr = NULL;</code></pre>
<p>널 포인터는 실제 메모리 공간을 가리키고 있지 않으므로 역참조하면 안 된다.</p>
<pre><code class="language-c">int *numPtr = NULL;

// 잘못된 코드
// *numPtr = 10;</code></pre>
<p>위 코드는 <code>numPtr</code>이 아무것도 가리키지 않는데 값을 저장하려고 하므로 문제가 발생한다.</p>
<p>실무에서는 포인터가 <code>NULL</code>인지 확인한 뒤, <code>NULL</code>이면 메모리를 할당하는 패턴을 자주 사용한다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main(void)
{
    int *numPtr = NULL;

    if (numPtr == NULL) // 포인터가 아무것도 가리키지 않는다면
    {
        numPtr = malloc(sizeof(int)); // 메모리 할당
    }

    if (numPtr == NULL) // malloc 실패 여부 확인
    {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    *numPtr = 20;

    printf(&quot;%d\n&quot;, *numPtr);

    free(numPtr);

    return 0;
}</code></pre>
<hr />
<h2 id="7-배열의-포인터">7. 배열의 포인터</h2>
<p>배열 이름은 대부분의 상황에서 배열의 첫 번째 요소 주소처럼 사용된다.</p>
<p>따라서 배열을 포인터에 넣을 수 있다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void)
{
    int numArr[5] = { 10, 20, 30, 40, 50 };

    int *numPtr = numArr; // 배열의 첫 번째 요소 주소를 포인터에 저장

    printf(&quot;%d\n&quot;, *numPtr);      // 첫 번째 요소 출력: 10
    printf(&quot;%d\n&quot;, numPtr[0]);    // 첫 번째 요소 출력: 10
    printf(&quot;%d\n&quot;, numPtr[1]);    // 두 번째 요소 출력: 20

    return 0;
}</code></pre>
<p><code>numArr</code>은 배열 전체를 의미하지만, 많은 표현식에서 <code>numArr</code>은 첫 번째 요소의 주소로 변환된다.</p>
<p>따라서 다음 두 코드는 같은 의미로 볼 수 있다.</p>
<pre><code class="language-c">int *numPtr = numArr;
int *numPtr = &amp;numArr[0];</code></pre>
<p>그리고 포인터를 역참조하면 배열의 첫 번째 요소에 접근할 수 있다.</p>
<pre><code class="language-c">printf(&quot;%d\n&quot;, *numPtr); // numArr[0]과 같음</code></pre>
<p>배열 자체를 역참조해도 첫 번째 요소에 접근할 수 있다.</p>
<pre><code class="language-c">printf(&quot;%d\n&quot;, *numArr); // numArr[0]과 같음</code></pre>
<hr />
<h2 id="8-배열과-포인터의-자료형">8. 배열과 포인터의 자료형</h2>
<p>배열을 포인터에 할당하려면 자료형이 맞아야 한다.</p>
<p>예를 들어 <code>int</code> 배열이라면 <code>int *</code> 포인터에 넣어야 한다.</p>
<pre><code class="language-c">int numArr[5] = { 10, 20, 30, 40, 50 };

int *numPtr = numArr; // 올바른 코드</code></pre>
<p>1차원 배열의 요소에 접근할 목적이라면 <code>*</code>가 한 개인 단일 포인터를 사용한다.</p>
<pre><code class="language-c">int *numPtr;</code></pre>
<p>단, 엄밀히 말하면 배열 자체와 포인터는 완전히 같은 것은 아니다.</p>
<p>배열 이름이 포인터처럼 사용되는 경우가 많아서 비슷해 보일 뿐이다.</p>
<hr />
<h2 id="9-배열과-포인터의-차이점">9. 배열과 포인터의 차이점</h2>
<p>배열과 포인터의 대표적인 차이는 <code>sizeof</code> 결과에서 확인할 수 있다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;

int main(void)
{
    int numArr[5] = { 10, 20, 30, 40, 50 };
    int *numPtr = numArr;

    printf(&quot;%zu\n&quot;, sizeof(numArr)); // 배열 전체 크기
    printf(&quot;%zu\n&quot;, sizeof(numPtr)); // 포인터 변수의 크기

    return 0;
}</code></pre>
<p><code>int</code>가 4바이트라면 <code>numArr</code>은 <code>int</code> 5개짜리 배열이므로 총 20바이트이다.</p>
<pre><code class="language-text">sizeof(numArr) = 20</code></pre>
<p>하지만 <code>numPtr</code>은 배열 전체가 아니라 주소를 저장하는 포인터 변수이다.</p>
<p>따라서 <code>sizeof(numPtr)</code>은 포인터 자체의 크기를 출력한다.</p>
<pre><code class="language-text">32비트 환경: 4
64비트 환경: 8</code></pre>
<p>즉, 배열과 포인터는 비슷하게 사용할 수 있는 경우가 있지만, 완전히 같은 개념은 아니다.</p>
<hr />
<h2 id="10-malloc으로-배열처럼-메모리-사용하기">10. malloc으로 배열처럼 메모리 사용하기</h2>
<p><code>malloc</code>을 사용하면 배열처럼 사용할 수 있는 메모리 공간도 만들 수 있다.</p>
<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main(void)
{
    int *numPtr = malloc(sizeof(int) * 5); // int 5개 크기만큼 메모리 할당

    if (numPtr == NULL)
    {
        printf(&quot;메모리 할당 실패\n&quot;);
        return 1;
    }

    numPtr[0] = 10; // 배열처럼 사용
    numPtr[1] = 20;
    numPtr[2] = 30;
    numPtr[3] = 40;
    numPtr[4] = 50;

    for (int i = 0; i &lt; 5; i++)
    {
        printf(&quot;%d\n&quot;, numPtr[i]); // 각 요소 출력
    }

    free(numPtr); // malloc으로 할당한 메모리 해제

    return 0;
}</code></pre>
<p><code>malloc(sizeof(int) * 5)</code>는 <code>int</code> 값 5개를 저장할 수 있는 공간을 힙에 할당한다.</p>
<p>이렇게 할당받은 메모리는 배열처럼 <code>numPtr[0]</code>, <code>numPtr[1]</code> 형식으로 접근할 수 있다.</p>
<hr />
<h2 id="정리">정리</h2>
<ul>
<li><p><code>malloc</code>은 힙 메모리를 할당하는 함수이다.</p>
</li>
<li><p><code>malloc</code>은 성공하면 메모리 주소를 반환하고, 실패하면 <code>NULL</code>을 반환한다.</p>
</li>
<li><p><code>malloc</code>으로 할당받은 메모리는 반드시 <code>free</code>로 해제해야 한다.</p>
</li>
<li><p>포인터에 값을 저장하거나 값을 가져올 때는 역참조를 사용한다.</p>
</li>
<li><p><code>memset</code>은 메모리를 바이트 단위로 특정 값으로 채우는 함수이다.</p>
</li>
<li><p><code>memset</code>은 주로 메모리를 <code>0</code>으로 초기화할 때 사용한다.</p>
</li>
<li><p><code>NULL</code> 포인터는 아무것도 가리키지 않는 포인터이므로 역참조하면 안 된다.</p>
</li>
<li><p>배열 이름은 많은 상황에서 배열의 첫 번째 요소 주소처럼 사용된다.</p>
</li>
<li><p>배열을 포인터에 저장하면 포인터를 통해 배열 요소에 접근할 수 있다.
(하지만 배열과 포인터는 완전히 같은 것은 아니다)</p>
</li>
<li><p><code>sizeof(배열)</code>은 배열 전체 크기를 구하고, <code>sizeof(포인터)</code>는 포인터 변수 자체의 크기를 구한다.</p>
</li>
</ul>
<p><em>참조: 코딩도장</em>
```</p>