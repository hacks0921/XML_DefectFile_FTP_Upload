import ftplib
import os
import sys

def upload_to_ftp(local_file, remote_file=None):
    """
    FTP 서버로 파일을 업로드하는 함수
    """
    # ==========================================
    # [사용자 설정 영역] FTP 접속 정보 수정 필요
    FTP_HOST = "192.168.0.100"  # FTP 서버 IP 주소 
    FTP_PORT = 21               # FTP 포트 (기본 21)
    FTP_USER = "user"           # FTP 아이디
    FTP_PASS = "password"       # FTP 비밀번호
    FTP_DIR  = "/logs/xml"      # 업로드할 서버 경로 (없으면 루트에 업로드)
    # ==========================================

    if not os.path.exists(local_file):
        print(f"[오류] 로컬 파일이 존재하지 않습니다: {local_file}")
        return

    # 원격 파일명이 지정되지 않았으면 로컬 파일명 그대로 사용
    if remote_file is None:
        remote_file = os.path.basename(local_file)

    ftp = None
    try:
        print(f"[FTP] 서버({FTP_HOST}:{FTP_PORT}) 접속 시도 중...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"[FTP] 로그인 성공: {FTP_USER}")

        # 디렉토리 이동 (없으면 예외 발생 가능성이 있으므로 주의)
        try:
            ftp.cwd(FTP_DIR)
            print(f"[FTP] 작업 디렉토리 변경: {FTP_DIR}")
        except ftplib.error_perm:
            print(f"[주의] 디렉토리 변경 실패 ({FTP_DIR}). 루트 디렉토리에 업로드합니다.")

        print(f"[FTP] 파일 업로드 시작: {local_file} -> {remote_file}")
        
        # 바이너리 모드로 업로드
        with open(local_file, "rb") as f:
            ftp.storbinary(f"STOR {remote_file}", f)
            
        print("[FTP] 업로드 완료!")
        
    except ftplib.all_errors as e:
        print(f"[오류] FTP 작업 중 문제 발생: {e}")
        
    finally:
        if ftp:
            try:
                ftp.quit()
                print("[FTP] 연결 종료")
            except:
                pass

if __name__ == "__main__":
    target_file = "product_inspection.xml"
    
    # 예시: 현재 날짜를 붙여서 서버에 저장하고 싶을 때
    # from datetime import datetime
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # remote_name = f"Log_{timestamp}.xml"
    
    print("====== FTP 파일 업로드 예제 시작 ======")
    upload_to_ftp(target_file)
    print("=======================================")
