import xml.etree.ElementTree as ET
import os
import upload_log_ftp  # FTP 업로드 모듈 임포트

def indent(elem, level=0):
    """XML 가독성을 위한 들여쓰기 함수"""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def append_defect_info(filename):
    print(f"[OP-20] '{filename}' 파일 로딩 중...")
    
    if not os.path.exists(filename):
        print("오류: 파일이 없습니다.")
        return

    try:
        # 1. 파일 파싱
        tree = ET.parse(filename)
        root = tree.getroot()
        
        # 2. DefectBody 찾기
        defect_body = root.find("DefectBody")
        if defect_body is None:
            # 만약 없다면 새로 생성 (예외 처리)
            defect_body = ET.SubElement(root, "DefectBody")
            print("[OP-20] DefectBody 태그가 없어 새로 생성했습니다.")

        # 현재 등록된 불량 개수 확인 (Sequence 생성을 위해)
        current_defects = defect_body.findall("Defect")
        next_seq = len(current_defects) + 1
        
        # 3. 새로운 불량 추가 (OP-20)
        new_defect = ET.SubElement(defect_body, "Defect")
        new_defect.set("sequence", str(next_seq))
        new_defect.set("type", "Bubble")
        new_defect.set("x", "50")
        new_defect.set("y", "50")
        new_defect.set("process", "OP-20")
        
        print(f"[OP-20] 신규 불량(Bubble, seq={next_seq}) 추가 완료")

        # 4. 저장
        indent(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"[OP-20] 파일 업데이트 완료: {filename}")
        print("-" * 30)
        
        # 5. FTP 업로드 자동 수행
        print("[System] FTP 자동 업로드 시작...")
        upload_log_ftp.upload_to_ftp(filename)
        print("-" * 30)
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    append_defect_info("product_inspection.xml")
