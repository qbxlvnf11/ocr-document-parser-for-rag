# MinerU 실행 가이드

## 1. 실행 방법 (How to Run)
```bash
# 기본 실행 (pipeline 모드, 한국어)
sudo docker compose up

# 옵션 변경 실행 (하이브리드 엔진 사용 예시)
BACKEND=hybrid-auto-engine sudo docker compose up

# 특정 파일만 변환 (명령어 직접 실행)
sudo docker compose run --rm mineru-demo python3 demo.py -p demo/pdfs/demo2.pdf -b pipeline -l en

# 컨테이너 내리기
sudo docker compose down
```

## 2. 주요 옵션 설명

### 변환 엔진 선택 (`BACKEND`)
문서를 분석하는 핵심 알고리즘 및 추론 엔진을 결정합니다.

| 옵션명 | 설명 | 비고 |
| :--- | :--- | :--- |
| **`hybrid-auto-engine`** | **(권장/정밀)** 차세대 솔루션. VLM의 정확도와 Pipeline의 안정성 결합. | GPU 필요 (VRAM 10GB+) |
| **`pipeline`** | **(호환/기본)** 가장 범용적인 방식. CPU 환경에서도 실행 가능. | CPU 지원 / 저사양 GPU |
| **`vlm-auto-engine`** | 순수 VLM 기반 고정밀 분석. 하드웨어 요구사항 높음. | 고사양 GPU 필요 |

### 분석 방식 선택 (`METHOD`)
PDF 내부 데이터를 읽는 성격을 지정합니다.

| 옵션명 | 설명 | 비고 |
| :--- | :--- | :--- |
| **`auto`** | **(기본값)** 파일 타입을 자동으로 판단 (텍스트 vs 이미지) | 범용적 사용 |
| **`txt`** | **텍스트 추출 우선.** 디지털 PDF에 적합하며 속도가 빠름. | 스캔본 사용 불가 |
| **`ocr`** | **광학 문자 인식.** 이미지 형태의 PDF나 스캔본에 필수 사용. | 속도가 상대적으로 느림 |

### 언어 선택 (`LANG`)
OCR 정확도 향상을 위한 언어 지정입니다.
- `korean` (한국어), `en` (영어), `ch` (중국어) 등