---
type: aws_developer
number: 2
---

## 2025-12-29 IAM Policies

[📄 원본 파일 보기](raw/002.%20Creating%20an%20AWS%20Account.md)


<details>
<summary>복습 키워드: IAM 정책, 권한 부여 방법, IAM 정책의 구조</summary>

### IAM 정책


### 권한 부여 방법

- 그룹 정책: 여러 사용자를 한데 묶어 공통된 권한을 부여할 때 매우 효과적
- 사용자별 인라인 정책: 특정 사용자에게만 고유한 권한이 필요한 경우
- 다중 그룹 소속 및 권한 상속: 두 그룹에 연결된 모든 정책의 권한을 상속
    - 가장 넓은 범위의 허용(Allow) 권한이 우선적으로 적용됩니다 (명시적인 거부(Deny) 정책이 없는 한)


### IAM 정책의 구조

- json 형식으로 되어 있음.
- Version: 정책의 버전
- Id: 정책의 고유한 식별자
- Statement 배열로 구성됨.
    - Sid: 정책의 고유한 식별자
    - Effect: Allow 또는 Deny
    - Principal: 정책이 적용될 대상 계정, 사용자, 역할 또는 서비스를 지정
    - Action: `Effect`에 따라 허용되거나 거부될 AWS API 호출 또는 작업 목록
    - Resource: `Effect`에 따라 허용되거나 거부될 AWS 리소스
    - Condition: 정책이 적용될 시점을 정의하는 선택적 조건

</details>