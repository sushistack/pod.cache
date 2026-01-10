---
type: aws_developer
number: 48
---

## 2026-01-10 EBS Multi-Attach

[📄 원본 파일 보기](raw/048.%20EBS%20Multi-Attach.md)


<details>
<summary>복습 키워드: EBS Multi-Attach, EBS Multi-Attach의 주요 특징 및 고려사항, EBS Multi-Attach의 활용 사례</summary>

### EBS Multi-Attach란 무엇인가

EBS Multi-Attach는 이름 그대로 하나의 EBS 볼륨을 **동일한 가용 영역(Availability Zone) 내의 여러 EC2 인스턴스에 동시에 연결**할 수 있도록 하는 기능입니다.

이 기능은 특히 다음과 같은 고성능 볼륨 유형에서 지원됩니다.

* `io1` (Provisioned IOPS SSD)
* `io2` (Provisioned IOPS SSD)

### 주요 특징 및 고려사항

- Multi-Attach는 AWS의 고성능 Provisioned IOPS SSD 볼륨인 `io1`과 `io2`에서만 지원됩니다.
- 가장 중요한 제한 사항 중 하나는 Multi-Attach가 **동일한 가용 영역(AZ) 내에서만 작동**한다는 것입니다.
- 하나의 EBS Multi-Attach 볼륨에 동시에 연결할 수 있는 EC2 인스턴스의 수는 **최대 16개**로 제한됩니다.
- Multi-Attach 볼륨을 여러 인스턴스에서 안전하게 사용하려면 **클러스터 인식 파일 시스템(Cluster-aware File System)**이 필수적입니다.

### EBS Multi-Attach 활용 사례

- 가장 대표적인 활용 사례는 **클러스터링된 리눅스 애플리케이션의 고가용성 확보**
- 여러 인스턴스가 동일한 데이터에 대해 **동시 읽기/쓰기 작업을 수행**해야 하는 시나리오

</details>

