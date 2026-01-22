---
type: aws_developer
number: 60
---

## 2026-01-22 Gateway Load Balancer

[📄 원본 파일 보기](raw/060.%20Gateway%20Load%20Balancer%20%28GWLB%29.md)


<details>
<summary>복습 키워드: GWLB란, 핵심기능 4개, 다른 LB와 비교</summary>

### Gateway Load Balancer란 무엇인가?

Gateway Load Balancer는 네트워크 트래픽을 가상 어플라이언스 플릿으로 전달하고, 어플라이언스가 트래픽을 처리한 후 다시 애플리케이션으로 보내는 과정을 총괄합니다.

#### GWLB의 등장 배경과 목적

과거에는 애플리케이션으로 향하는 모든 트래픽을 방화벽, 침입 탐지/방지 시스템(IDS/IPS), 딥 패킷 인스펙션(DPI) 시스템과 같은 써드파티 가상 어플라이언스를 거치도록 구성하는 것이 매우 복잡했습니다. 수동으로 라우팅 테이블을 조작하거나, 여러 네트워크 인터페이스를 관리하고, 어플라이언스의 가용성을 확보하기 위한 추가적인 노력이 필요했습니다. 이는 곧 복잡한 아키텍처, 높은 운영 비용, 그리고 확장성의 한계로 이어졌습니다.

AWS Gateway Load Balancer는 이러한 문제점들을 해결하기 위해 등장했습니다. GWLB의 주된 목적은 AWS 클라우드 환경에서 써드파티 네트워크 가상 어플라이언스(예: EC2 인스턴스에 배포된 방화벽 소프트웨어)를 배포, 확장, 관리하는 과정을 단순화하고 자동화하는 것입니다. 이를 통해 개발자와 운영팀은 네트워크 보안 및 가시성 요구사항을 충족하면서도, 핵심 애플리케이션 개발에 더욱 집중할 수 있게 되었습니다.

### 핵심 기능 및 주요 활용 사례

- 방화벽(Firewall)
- 침입 탐지 및 방지 시스템 (IDS/IPS)
- 심층 패킷 검사 (Deep Packet Inspection, DPI)
- 네트워크 레벨 페이로드 수정

### GWLB의 동작 원리: 트래픽 흐름 해부

```
사용자 트래픽 발생 -> VPC 라우팅 업데이트 -> GWLB로 트래픽 전송 
-> 어플라이언스 플릿으로 분산 -> 트래픽 검사 및 처리 -> GWLB로 트래픽 반환
-> 애플리케이션으로 최종 전달 -> 애플리케이션 투명성
```

### 레이어 3 동작과 GENEVE 프로토콜

GWLB는 OSI 모델의 **레이어 3 (네트워크 계층)**에서 작동합니다. 이는 IP 패킷 수준에서 트래픽을 처리한다는 의미입니다. 다른 AWS 로드 밸런서(예: Application Load Balancer는 L7, Network Load Balancer는 L4)와 달리, GWLB는 저수준의 네트워크 트래픽을 다룹니다. 또한 GWLB는 가상 어플라이언스와의 통신을 위해 **GENEVE (Generic Network Virtualization Encapsulation) 프로토콜**을 사용합니다.

| 구분 | ALB (Application) | NLB (Network) | GWLB (Gateway) |
| - | - | - | - |
| OSI 계층 | Layer 7 (애플리케이션) | Layer 4 (전송) | Layer 3 (네트워크) |
| 주요 대상 | HTTP/HTTPS 웹 서비스 | 고성능 TCP/UDP 서비스 | 가상 보안 어플라이언스 |
| 동작 방식 | 패킷을 열어 경로/헤더 기반 라우팅 | IP/포트 기반 빠른 전달 | 패킷 전체를 캡슐화하여 전달 |
| IP 보존 | X-Forwarded-For 헤더 사용 | 타겟 그룹 설정에 따라 보존 가능 | 원래 패킷 내용 100% 보존 |


</details>

