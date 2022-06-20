# 1. [프로젝트명] Dev's book
# 2. [프로젝트 간단소개]
개발자들을 대상으로 개발에 도움이 되는 책들을 소개하고 리뷰도 같이 볼 수 있으며 구매 사이트로 바로 구매까지 가능한 사이트입니다.

# 3. [기능]
1) 메인페이지
로그인, 회원 가입 (get)
책 추천(크롤링) >>프론/백 메뉴 클릭시 리스트화or페이지화 할건지 정하기

2) 서브페이지 - 책 소개
책 소개 크롤링

3) 서브페이지 - 사용자 리뷰
사용자들의 댓글 작성 (post)
주문 하기.

4) 서브페이지 - 알라딘 주문 링크 연결

# 4. [역할분담]

-형 석 : 리뷰 작성

-주 영 : 로그인, 회원 가입

-소 현:   주문하기

-호 영: 메인 페이지

# 5. [와이어 프레임]
![KakaoTalk_20220620_205113048](https://user-images.githubusercontent.com/107523641/174595784-5da44ef8-4ad3-4573-aa05-77f9092f8a0d.png)

 회원가입 페이지

![캡처](https://user-images.githubusercontent.com/107523641/174597995-5ef5b894-701e-4638-b13d-2c36cc835399.PNG)


# 6. [개발해야하는 기능들]


 |기능|method|url|request|respeonse|
|------|------|--------|-------------------|-------------|
|회원가입|POST|/signup|{"id":"id","p w":"pw", "email":"email", "tell":"tell","pwcheck":"pwcheck"}|가입완료|
|로그인|POST|/login|	{"id":"id","pw":"pw"}|로그인완료|
|댓글|POST|/review|{"comment":"comment"}|작성완료|
|메인페이지|GET|/books|{"books":"books"}||
