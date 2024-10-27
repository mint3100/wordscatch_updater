# 워드스케치 업데이터
본 파이썬 파일은 워드스케치 포터블 (MP100), 워드스케치 플러스 (WS200)을 위한 워드스케치 업데이터 입니다.

사용된 모듈은 다음과 같습니다.\
```sqlite3, requests, os, logging```

## 사용법
1. downloader.py를 실행하면 자동으로 wm 폴더가 생성되며 폴더 내에 워드스케치 업데이트 파일이 다운로드 됩니다.
2. 혹시 모를 업데이트 꼬임을 방지하여 기기 내의 wm 폴더를 백업합니다. (선택사항)
3. 다운로드된 wm 폴더를 그대로 덮어쓰기 합니다.
4. 업데이트가 완료되었습니다. 업데이트 정보는 생성된 Changelog.txt 파일을 확인하세요

---------------------
본 프로그램에서 통신하는 서버는 (주)위버스마인드의 서버이며, 모든 파일의 저작권은 (주)위버스마인드에 있습니다. 본 프로그램을 사용하여 발생하는 문제는 책임지지 않습니다.