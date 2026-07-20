# Git Flow와 GitHub Flow 비교

## 1. Branch란?

Branch는 기존 코드를 유지하면서 별도의 공간에서 새로운 기능을 개발하거나 오류를 수정할 수 있도록 해주는 기능이다.

별도의 Branch에서 작업하면 main Branch의 코드에 직접 영향을 주지 않고 안전하게 작업할 수 있다.

## 2. Git Flow

Git Flow는 개발과 배포 과정을 여러 종류의 Branch로 나누어 관리하는 방식이다.

### 주요 Branch

- main: 실제 배포에 사용하는 안정적인 코드
- develop: 다음 버전을 준비하는 개발 코드
- feature: 새로운 기능을 개발하는 Branch
- release: 배포 전 최종 점검을 하는 Branch
- hotfix: 배포된 코드의 긴급 오류를 수정하는 Branch

### 장점

- 개발과 배포 과정을 체계적으로 관리할 수 있다.
- 규모가 크고 여러 버전을 관리하는 프로젝트에 적합하다.

### 단점

- 사용하는 Branch가 많아서 관리가 복잡할 수 있다.
- 짧고 간단한 프로젝트에는 불필요하게 복잡할 수 있다.

## 3. GitHub Flow

GitHub Flow는 main Branch와 기능 작업용 Branch를 중심으로 사용하는 간단한 방식이다.

### 작업 순서

1. main Branch에서 새로운 작업 Branch를 만든다.
2. 작업 Branch에서 코드를 작성한다.
3. 변경 내용을 Add와 Commit으로 기록한다.
4. 작업 Branch를 GitHub에 Push한다.
5. Pull Request를 작성한다.
6. 변경된 코드를 확인하고 Review한다.
7. 문제가 없으면 main Branch에 Merge한다.

### 장점

- 구조가 간단해서 이해하고 사용하기 쉽다.
- 기능을 빠르게 개발하고 main에 반영할 수 있다.
- 기간이 짧은 프로젝트에 적합하다.

### 단점

- 복잡한 출시 버전을 관리하는 큰 프로젝트에는 부족할 수 있다.

## 4. 이번 프로젝트에서 사용할 전략

이번 프로젝트에서는 GitHub Flow를 사용한다.

개인 프로젝트이며 과제 기간이 짧기 때문에 여러 종류의 Branch를 사용하는 Git Flow보다 main Branch와 기능 Branch를 사용하는 GitHub Flow가 더 적합하다고 판단하였다.

### 적용 과정

main Branch  
→ feature/day2-practice-api Branch 생성  
→ FastAPI 코드 작성  
→ Add  
→ Commit  
→ Push  
→ Pull Request  
→ 코드 확인  
→ main Branch에 Merge