---
type: aws_developer
number: 58
---

## 2026-01-20 Network Load Balancer

[📄 원본 파일 보기](raw/058.%20Network%20Load%20Balancer%20%28NLB%29.md)


<details>
<summary>복습 키워드: NLB란, 타겟 그룹, 헬스 체크 프로토콜 지원</summary>

### Network Load Balancer 란?


- 전송 계층(Layer 4) 로드 밸런싱: NLB는 OSI 모델의 전송 계층(Layer 4)에서 작동하며, 주로 **TCP(Transmission Control Protocol)** 및 **UDP(User Datagram Protocol)** 트래픽을 처리합니다.
- 초고성능 및 초저지연: 초당 수백만 건의 요청 처리, 실시간 서비스나 높은 처리량이 요구되는 애플리케이션에 최소한의 지연 시간을 보장
- 가용성 영역당 고정 IP 주소: NLB의 가장 독특한 특징 중 하나는 각 가용성 영역(Availability Zone, AZ)마다 하나의 **고정 IP 주소**를 제공

### Network Load Balancer의 타겟 그룹

NLB는 Application Load Balancer와 유사하게 **타겟 그룹(Target Group)**을 사용하여 트래픽을 백엔드 리소스로 라우팅합니다.

- EC2 인스턴스
- IP 주소 (이때 등록되는 IP 주소는 **사설 IP(Private IP)**여야 합니다.)
    - 소유한 EC2 인스턴스의 사설 IP
    - 온프레미스 데이터센터 서버의 사설 IP
- Application Load Balancer (ALB): NLB를 ALB 앞에 배치함으로써, 고정 IP 주소의 이점을 유지하면서 ALB의 풍부한 HTTP/HTTPS 라우팅 규칙과 고급 기능을 활용할 수 있게 됩니다.

### 헬스 체크 프로토콜 지원

- TCP
- UDP
- HTTP / HTTPS

위 프로토콜 모두 제공

</details>

