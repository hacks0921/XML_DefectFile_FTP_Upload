

# 구현 계획: 공장 불량 이력 XML 관리 시스템 (수정됨)

사용자의 요청에 따라 `Glass`, `Panel`, `DefectBody` 구조로 세분화하여 불량 정보를 관리하는 시스템입니다.

## 1. 파일 구조
- `create_initial_log.py`: 초기 XML 생성 (OP-10 공정 가정)
- `append_new_log.py`: 기존 XML에 신규 불량 추가 (OP-20 공정 가정)
- `upload_log_ftp.py`: 완성된 XML 파일을 FTP 서버로 업로드 (신규)
- `product_inspection.xml`: 데이터 파일

## 2. 변경된 XML 데이터 구조
데이터를 **Glass(자재 정보)**, **Panel(패널 정보)**, **DefectBody(불량 리스트)** 세 부분으로 나누어 관리합니다.

```xml
<InspectionData>
    <!-- 1. Glass 정보 -->
    <Glass serial="GLS-20240111-001" type="Type-A" thickness="0.5t" />
    
    <!-- 2. Panel 정보 -->
    <Panel id="PNL-01" position="1,1" />

    <!-- 3. 불량 정보 (DefectBody 안에 누적) -->
    <DefectBody>
        <!-- OP-10 불량 -->
        <Defect sequence="1" type="Scratch" x="120" y="45" process="OP-10" />
        <Defect sequence="2" type="Dent" x="200" y="90" process="OP-10" />
        
        <!-- OP-20에서 추가될 불량 -->
        <Defect sequence="3" type="Bubble" x="50" y="50" process="OP-20" />
    </DefectBody>
</InspectionData>
```

## 3. 구현 상세
1.  **초기 생성 (`create_initial_log.py`)**: Root를 만들고 `Glass`, `Panel`, `DefectBody` 요소를 생성하여 기본 불량을 추가합니다.
2.  **추가 기록 (`append_new_log.py`)**: 파일을 읽어 `DefectBody` 태그를 찾아 새로운 `Defect` 태그를 추가(`append`)합니다.
3.  **FTP 업로드 (`upload_log_ftp.py`)**:
    - `ftplib` 내장 라이브러리 사용
    - 바이너리 모드(`STOR`)로 업로드하여 파일 손상 방지
    - 예외 처리를 통해 접속 실패 및 전송 오류 대응
