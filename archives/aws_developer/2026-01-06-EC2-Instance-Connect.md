---
type: aws_developer
number: 37
---

## 2026-01-06 EC2 Instance Connect

<details>
<summary>복습 키워드: EC2 Instance Connect</summary>

### EC2 Instance Connect

- SSH 키 관리의 번거로움 없이 웹 브라우저를 통해 EC2 인스턴스에 안전하게 접속할 수 있는 서비스.
- 접속 시 AWS가 임시 SSH 키를 자동으로 생성하여 인스턴스에 업로드하고 연결을 설정.


### EC2 Instance Connect의 내부 동작 및 보안 그룹 설정의 중요성

- 여전히 내부적으로는 SSH 프로토콜(Port 22)을 사용
- 인스턴스의 보안 그룹(Security Group)에서 Port 22가 열려 있어야만 정상적인 연결이 가능

> 해결책: 보안 그룹 규칙 수정

</details>