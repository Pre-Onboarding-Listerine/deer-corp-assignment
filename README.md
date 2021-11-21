# 🛴 deer-corp-assignment 🛴

## 🛴 기업과제
- 기업명: 디어코퍼레이션
- 기업사이트: https://web.deering.co/
- 기업채용공고: https://www.wanted.co.kr/wd/59051

## 🛴 과제 내용

### **[필수 포함 사항]**

- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

### **[주요 평가 사항]**

- 주어진 정보를 기술적으로 설계하고 구현할 수 있는 역량
- 확장성을 고려한 시스템 설계 및 구현

### 과제 안내

디어는 사용자의 요금을 계산하기 위해 다양한 상황을 고려합니다. 

- 우선 지역별로 다양한 요금제를 적용하고 있습니다. 예를 들어 건대에서 이용하는 유저는 기본요금 790원에 분당요금 150원, 여수에서 이용하는 유저는 기본요금 300원에 분당요금 70원으로 적용됩니다.
- 할인 조건도 있습니다. 사용자가 파킹존에서 반납하는 경우 요금의 30%를 할인해주며, 사용자가 마지막 이용으로부터 30분 이내에 다시 이용하면 기본요금을 면제해줍니다.
- 벌금 조건도 있습니다. 사용자가 지역 바깥에 반납한 경우 얼마나 멀리 떨어져있는지 거리에 비례하는 벌금을 부과하며, 반납 금지로 지정된 구역에 반납하면 6,000원의 벌금을 요금에 추과로 부과합니다.
- 예외도 있는데, 킥보드가 고장나서 정상적인 이용을 못하는 경우의 유저들을 배려하여 1분 이내의 이용에는 요금을 청구하지 않고 있습니다.

- 최근에 다양한 할인과 벌금을 사용하여 지자체와 협력하는 경우가 점점 많아지고 있어 요금제에 새로운 할인/벌금 조건을 추가하는 일을 쉽게 만드려고 합니다. 어떻게 하면 앞으로 발생할 수 있는 다양한 할인과 벌금 조건을 기존의 요금제에 쉽게 추가할 수 있는 소프트웨어를 만들 수 있을까요? 

- 우선은 사용자의 이용에 관한 정보를 알려주면 현재의 요금 정책에 따라 요금을 계산해주는 API를 만들어주세요. 그 다음은, 기능을 유지한 채로 새로운 할인이나 벌금 조건이 쉽게 추가될 수 있게 코드를 개선하여 최종 코드를 만들어주세요.
----

## 🛴 팀: 리스테린(Listerine)

* 팀원

| 이름 | 역할 | GITHUB | BLOG |
| :---: | :---: | :---: | :---: |
| `김주완` | 개발 및 배포환경 설정, API 설계 및 구현 | [joowankim](https://github.com/joowankim) | https://make-easy-anything.tistory.com |
| `박은혜` | 애플리케이션 배포, 기능 구현 | [eunhye43](https://github.com/eunhye43) | https://velog.io/@majaeh43 |
| `윤수진` | API 구현 | [study-by-myself](https://github.com/study-by-myself)| https://pro-yomi.tistory.com |
| `주종민` | 모델 설계 및 구현 | [Gouache-studio](https://github.com/Gouache-studio) | https://gouache-studio.tistory.com/ |


## 🛴 구현 API

POSTMAN 주소:


### Unit test

테스트 코드는 `/tests` 디렉토리에서 확인하실 수 있습니다. 그리고 루트 디렉토리에서 다음 명령어로 테스트를 실행할 수 있습니다.

```commandline
$ pytest
```

## 🛴 모델 관계

- 

### 존재하는 모델

- ``: 
- ``: 
- ``: 

## 애플리케이션 구조



## 🛴 실행환경 설절 방법

> `git`과 `docker`, `docker-compose`가 설치되어 있어야 합니다.

1. 레포지토리 git 클론

    ```bash
    $ git clone https://github.com/Pre-Onboarding-Listerine/deer-corp-assignment.git
    ```

2. 애플리케이션 실행하기

    ```bash
    $ docker-compose up

    # 애플리케이션을 백그라운드에서 실행하고 싶다면
    $ docker-compose up -d
    
    # 어플리케이션이 실행이 되고 난 후에 데이터베이스 migration이 필요하다면
    $ docker-compose exec api
   
    # 데이터베이스 초기화
    $ docker-compose exec backend python init_db.py
    ```

3. 애플리케이션에 접근하기

    ```
    http://localhost:8000
    ```

## 🛴 과제 결과물 테스트 및 확인 방법

1. POSTMAN 확인: https://documenter.getpostman.com/view/15905881/UVJWqfZk

2. 배포된 서버의 주소

    ```commandline
    3.37.127.222:8000
    ```

# 🛴 Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 디어코퍼레이션에서 출제한 과제를 기반으로 만들었습니다.
