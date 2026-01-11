# XML Defect Log Management & FTP Upload System

공정 간 제품 불량 정보를 XML 파일로 누적 관리하고, 작업 완료 후 FTP 서버로 자동 업로드하는 시스템입니다.

## 📌 기능 개요
1. **OP-10 공정 (초기 생성)**: 제품(Glass/Panel) 정보와 초기 불량 내역이 담긴 XML 파일을 생성합니다.
2. **OP-20 공정 (추가 기록)**: 이전 공정의 XML 파일을 읽어 새로운 불량 정보를 `DefectBody`에 추가합니다.
3. **자동 업로드**: OP-20 작업이 완료되면 수정된 XML 파일을 지정된 FTP 서버로 전송합니다.

## 📁 파일 구성
- `create_initial_log.py`: **[OP-10]** 초기 XML 파일 생성 스크립트
- `append_new_log.py`: **[OP-20]** 불량 추가 및 FTP 업로드 자동 실행 스크립트
- `upload_log_ftp.py`: FTP 업로드 기능을 담당하는 모듈
- `product_inspection.xml`: 생성 및 관리되는 데이터 파일

## ⚙️ XML 데이터 구조
데이터는 `Glass`, `Panel`, `DefectBody` 세 가지 주요 섹션으로 구분됩니다.

```xml
<InspectionData>
  <!-- 자재 정보 -->
  <Glass serial="GLS-20240111-001" type="Type-A" thickness="0.5t" />
  
  <!-- 패널 정보 -->
  <Panel id="PNL-01" position="1,1" />
  
  <!-- 불량 리스트 (누적) -->
  <DefectBody>
    <Defect sequence="1" type="Scratch" x="120" y="45" process="OP-10" />
    <Defect sequence="2" type="Dent" x="200" y="90" process="OP-10" />
    <Defect sequence="3" type="Bubble" x="50" y="50" process="OP-20" />
  </DefectBody>
</InspectionData>
```

## 🚀 사용 방법

### 1. 환경 설정
`upload_log_ftp.py` 파일을 열어 FTP 서버 정보를 수정하세요.
```python
FTP_HOST = "192.168.0.100"  # 서버 IP
FTP_PORT = 21               # 포트
FTP_USER = "user"           # 아이디
FTP_PASS = "password"       # 비밀번호
```

### 2. OP-10 (초기 검사) 실행
```bash
python create_initial_log.py
```
`product_inspection.xml` 파일이 생성됩니다.

### 3. OP-20 (추가 검사) 실행
```bash
python append_new_log.py
```
기존 XML에 새로운 불량이 추가되고, **자동으로 FTP 업로드가 시도**됩니다.

## ⚠️ 주의사항
- FTP 서버가 실행 중이어야 업로드가 성공합니다.
- 예제 코드는 로컬 테스트 IP(`192.168.0.100`)로 설정되어 있으므로 실제 환경에 맞게 변경해야 합니다.
