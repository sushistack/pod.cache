---
type: aws_developer
number: 55
---

## 2026-01-19 Application Load Balancer

<details>
<summary>복습 키워드: ALB, 특징 및 장점, 고급 라우팅 기능, 타겟 그룹, 고려사항</summary>

### ALB 란?

AWS Application Load Balancer(ALB)는 HTTP/HTTPS 트래픽 분산에 특화된 레이어 7 로드 밸런서입니다.

### ALB의 핵심 특징과 장점

- 레이어 7 전용: HTTP, HTTPS 트래픽에 최적화되어 있으며, 요청의 내용을 분석하여 라우팅 결정을 내립니다.
- 다중 애플리케이션 지원: 하나의 ALB 뒤에 여러 개의 HTTP 애플리케이션을 배치하고 관리할 수 있습니다. 이는 기존 Classic Load Balancer가 애플리케이션당 하나의 로드 밸런서가 필요했던 것과 대조적입니다.
- 프로토콜 지원: HTTP/2 및 WebSockets를 지원하여 최신 웹 기술을 활용하는 애플리케이션에 적합합니다.
- 자동 리디렉션: HTTP 요청을 자동으로 HTTPS로 리디렉션하는 기능을 제공하여 보안을 강화하고 관리 부담을 줄여줍니다.

### 고급 라우팅 기능

1. URL 경로 기반 라우팅 (Path-based Routing)
2. 호스트명 기반 라우팅 (Host-based Routing)
3. 쿼리 스트링 및 HTTP 헤더 기반 라우팅 (Query String & Header-based Routing)


### 타겟 그룹(Target Group)의 이해

ALB는 요청을 처리할 대상 서버들을 `타겟 그룹`이라는 논리적인 그룹으로 묶습니다.

ALB가 지원하는 타겟 유형은 다음과 같습니다.

- EC2 인스턴스: 가장 일반적인 형태로, Auto Scaling Group과 연동하여 자동으로 확장/축소될 수 있습니다.
- ECS(Elastic Container Service) 태스크: 컨테이너 기반 애플리케이션을 위한 핵심 타겟 유형입니다.
- Lambda 함수: 서버리스 아키텍처를 구현할 때 ALB를 프런트엔드로 사용할 수 있습니다.
- IP 주소: AWS 클라우드 외부의 온프레미스 서버나 다른 VPC의 리소스 등 특정 IP 주소로도 트래픽을 라우팅할 수 있습니다 (단, 사설 IP 주소여야 함).


### 마이크로서비스 및 컨테이너 환경에서의 ALB

ALB는 마이크로서비스와 컨테이너 기반 애플리케이션(특히 Docker 및 Amazon ECS)에 최적화된 로드 밸런서입니다.

동적 포트 매핑: ECS 환경에서 컨테이너는 호스트 EC2 인스턴스의 동적 포트에 할당될 수 있습니다.

### ALB 사용 시 고려사항

1. 고정 호스트명: ALB는 생성 시 고유한 고정 호스트명(예: `my-alb-123456789.us-east-1.elb.amazonaws.com`)을 제공합니다.
2. 클라이언트 IP 주소 전달 (X-Forwarded-* 헤더): ALB는 클라이언트의 요청을 받아 타겟 그룹의 인스턴스로 전달할 때, 클라이언트와 직접 통신하는 대신 ALB 자체가 중간에서 연결을 종료하고 새로운 연결을 타겟 인스턴스와 수립합니다.

</details>

