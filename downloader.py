import sqlite3
import requests
import os
import logging

# 워드스케치 업데이터
# 24.10.27

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt ='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

def download_fileinfo():
    logging.info(f"최신버전의 파일 정보를 받아옵니다.")
    url = "http://update.wordsketch.co.kr/@update/getfile.php?uri=fileInfo.dat&mf=mintpass&did=MP100M"
    save_path = "fileinfo.dat"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"{save_path}가 성공적으로 다운로드 되었습니다.")
    except Exception as e:
        logging.warning(f"fileinfo.dat 다운로드 실패: {e}")
        return False
    return True

def download_file(url, save_path):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"{save_path} 파일이 성공적으로 다운로드 되었습니다.")
    except Exception as e:
        logging.warning(f"다운로드 실패: {e}")

def version_info():
    db_path = "fileinfo.dat"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(""" 
        SELECT Version, platform, codename, release_date, release_note 
        FROM VersionHistory 
        ORDER BY release_date DESC 
        LIMIT 1 
    """)
    latest_version = cursor.fetchone()

    if latest_version:
        version, platform, codename, release_date, release_note = latest_version
        if isinstance(release_note, bytes):
            release_note = release_note.decode('utf-8')
        version_info = (f"Version: {version} Platform: {platform} Codename: {codename} Release Date: {release_date}\nRelease Note: \n{release_note}")

        logging.info("")
        logging.info(f"최신 버전 정보: {version_info}")

        with open("Changelog.txt", "w", encoding="utf-8") as changelog_file:
            changelog_file.write(version_info)
        logging.info("Changelog.txt에 최신 버전 정보가 저장되었습니다.")
    else:
        logging.warning("VersionHistory 테이블에 데이터가 없습니다.")

    conn.close()

if download_fileinfo():
    db_path = "fileinfo.dat"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT uri, header, size FROM files")
    rows = cursor.fetchall()
    base_dir = "wm/"

    logging.info(f"데이터 파일 다운로드를 시작합니다.")
    for row in rows:
        uri, header, size = row
        url = f"http://update.wordsketch.co.kr/@update/getfile.php?uri={uri}&mf=mintpass&did=MP100M&header={header}&size={size}"
        save_path = os.path.join(base_dir, uri)
        download_file(url, save_path)

    version_info()
    logging.info(f"다운로드가 완료되었습니다. wm 폴더를 그대로 MINTPAD나 P35의 NAND에 위치해주세요. 사용자 정보를 유지하고 싶다면 wm 폴더 내의 user.wsk를 백업한 후 업데이트한 wm 폴더에 넣어주세요.")

    conn.close()
