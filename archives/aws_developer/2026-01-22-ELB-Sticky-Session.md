---
type: aws_developer
number: 61
---

## 2026-01-22 AWS ELB Sticky Session

[📄 원본 파일 보기](raw/061.%20Elastic%20Load%20Balancer%20-%20Sticky%20Sessions.md)

<details>
<summary>복습 키워드:Sticky Session이란?, 장단점, Sticky Session 쿠키 유형</summary>

### Sticky Session이란 무엇인가요?

Sticky Session은 로드 밸런서가 특정 클라이언트의 모든 요청을 동일한 백엔드 인스턴스로 지속적으로 라우팅하도록 하는 기능입니다.

#### 지원 가능 LB

- Classic Load Balancer (CLB)
- Application Load Balancer (ALB)
- Network Load Balancer (NLB)

### Sticky Session의 동작 원리

Sticky Session은 주로 HTTP/HTTPS 요청에서 **쿠키(Cookie)**를 기반으로 동작합니다.

```
초기 요청 -> 인스턴스 할당 -> 쿠키 발행 -> 후속 요청 -> 세션 유지 -> 쿠키 만료
```

#### 이점

Sticky Session의 가장 큰 이점은 **사용자 세션 데이터의 무결성 유지**입니다.

#### 주의할 점: 부하 불균형 (Load Imbalance)

Sticky Session은 사용자 경험을 향상시키지만, **로드 밸런싱의 균형을 해칠 수 있다**는 단점이 있습니다.


### Sticky Session 쿠키 유형

#### 애플리케이션 기반 쿠키 (Application-Based Cookie)

- 어플리케이션이 직접 생성: 백엔드 애플리케이션이 고유한 세션 ID를 담은 사용자 정의 쿠키를 생성하여 응답 헤더에 포함시킵니다. 이 쿠키에는 애플리케이션이 필요로 하는 모든 사용자 정의 속성을 포함할 수 있습니다. 로드 밸런서는 이 쿠키의 이름만 알면 됩니다.
- ELB가 생성: 로드 밸런서가 애플리케이션을 대신하여 쿠키를 생성합니다. 이때 ELB는 `AWSALBAPP`라는 이름의 쿠키를 사용합니다. 이 쿠키는 애플리케이션에서 설정한 세션 유지 정보를 기반으로 합니다.

#### 지속 시간 기반 쿠키 (Duration-Based Cookie)

- ELB가 생성: 로드 밸런서가 `AWSALB` (ALB용) 또는 `AWSELB` (CLB용)라는 이름의 쿠키를 생성합니다.
- 이 쿠키는 로드 밸런서 설정에 따라 1초에서 7일까지의 만료 기간을 가집니다. 만료 기간이 지나면 클라이언트는 다른 인스턴스로 라우팅될 수 있습니다.


</details>

