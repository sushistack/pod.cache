---
type: terraform  # (udemy_terraform 디렉토리 매핑)
number: 1        # (001. Introduction... 파일 매핑)
---

## 2025-12-19 Terraform 이란

<details>
<summary>Terraform 왜 써야함?</summary>

### 왜 테라폼 써야함?
현대 IT 인프라 복잡한 상황 => IaC 반복작업 줄이고 일관성 유지
테라폼의 역할 => 다양한 클라우드 서비스에 걸쳐 인프라를 프로비저닝
자동화, 일관성, 버전관리, 재해복구에 유용


### 핵심 개념
provider: 테라폼은 다양한 클라우드 또는 API와 상호작용함.
Input Variables: tf 실행 시, 외부로 부터 전달 받기 위해 사용
Output Variables: tf 실행 시, tf 로 프로비저닝한 리소스 정보를 외부로 노출

### tf state
테라폼이 관리하는 인프라의 현재 상태를 기록
변경사항을 추적하고, 계획하는데 필수적
인프라의 구성과 실제 환경 간의 일치를 보장.
state 파일 관리: 로컬, S3

### 명령어
init, plan, apply, destory
 
### tf 라이프 사이클 룰
lifecycle 블록을 이용하여, 리소스 동작 방식을 세밀하게 제어

### 데이터 소스 & 메타 아규먼트 & 버전 컨스트레인츠

데이터 소스: 외부 정보를 가져와 사용 가능 (최신 AMI ID 동적 획득)
메타 아규먼트: 여러 개의 리소스를 효율적
버전 컨스트레인츠: tf & provider 의 버전을 명시, 호환성 이슈 방지

### AWS & Terraform

tf 를 이용하여 AWS 의 서비스들을 프로비저닝하고 관리하는 방법 실습

### Provisioners & Resource Taints & Debugging & Import

Provisioners: 리소스가 생성된 후, 리소스에 코드를 복사/명령어 실행
Resource Taints: 테라폼에 관리되지 않도록 표시, apply 시, 재생성 유도
Debugging: 디버깅 법 학습
Import: 외부 리소스를 테라폼 상태 파일로 관리 할 수있게

### TF 모듈

TF 모듈: 재사용 가능한 단위로 묶어, TF Registry 에서 활용

### Functions & Conditional Expression & Workspaces

Functions: 문자열 처리, 숫자 계산, 리소스 속성 접근
Conditional Expression: 조건 표현식
Workspaces: 동일한 코드로 여러 환경(개발, 스테이징, 프로덕션 등)을 관리할 수 있게 해주는 기능

</details>
