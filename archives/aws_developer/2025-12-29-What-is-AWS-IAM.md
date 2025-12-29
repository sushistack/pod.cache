---
type: aws_developer
number: 1
---

## 2025-12-29 What is AWS IAM(Identity and Access Management)

[📄 원본 파일 보기](raw/001.%20Course%20Introduction%20-%20AWS%20Certified%20Developer%20Associate.md)


<details>
<summary>복습 키워드: IAM, 사용자, 그룹, 정책, 최소 권한 원칙</summary>

### IAM의 핵심 구성 요소와 원칙

- 사용자: 특정 개인이나 어플리케이션, 고유의 자격증명을 가짐.
- 그룹: IAM 사용자들을 효율적으로 관리하기 위한 논리적 집합.
    - 사용자만 포함 가능
    - 다른 그룹 포함 불가능
    - 여러 사용자는 여러 그룹에 포함 가능
- 정책: AWS 리소스에 대한 접근 권한을 정의하는 문서.
    - Statement 배열 (Effect, Action, Resource, Condition)
    - Effect: Allow 또는 Deny
    - Action: AWS 서비스에 대한 접근 권한 정의
    - Resource: AWS 리소스에 대한 접근 권한 정의, 리소스는 ARN(Amazon Resource Name) 형식으로 지정
    - Condition: 추가적인 조건

### 최소 권한 원칙

- IAM 정책은 최소한의 권한만을 부여해야 함.
- 필요하지 않은 권한은 제거해야 함.

목적은 보안 강화와 비용 절감(의도치 않은 서비스 생성이나 리소스 수정으로 인한 불필요한 비용 발생을 방지)

</details>