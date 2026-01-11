import xml.etree.ElementTree as ET
import os

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

def create_initial_xml(filename):
    print(f"[OP-10] '{filename}' 파일 생성 시작...")
    
    # 1. Root 생성
    root = ET.Element("InspectionData")
    
    # 2. Glass 정보 생성
    glass = ET.SubElement(root, "Glass")
    glass.set("serial", "GLS-20240111-001")
    glass.set("type", "Type-A")
    glass.set("thickness", "0.5t")
    
    # 3. Panel 정보 생성
    panel = ET.SubElement(root, "Panel")
    panel.set("id", "PNL-01")
    panel.set("position", "1,1")
    
    # 4. DefectBody 생성 (불량 담을 그릇)
    defect_body = ET.SubElement(root, "DefectBody")
    
    # 5. OP-10 불량 추가
    # 불량 1
    d1 = ET.SubElement(defect_body, "Defect")
    d1.set("sequence", "1")
    d1.set("type", "Scratch")
    d1.set("x", "120")
    d1.set("y", "45")
    d1.set("process", "OP-10")
    
    # 불량 2
    d2 = ET.SubElement(defect_body, "Defect")
    d2.set("sequence", "2")
    d2.set("type", "Dent")
    d2.set("x", "200")
    d2.set("y", "90")
    d2.set("process", "OP-10")

    # 저장
    indent(root)
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"[OP-10] 파일 생성 완료: {filename}")
    print("-" * 30)

if __name__ == "__main__":
    create_initial_xml("product_inspection.xml")
