BOJ Code Downloader
=====================

## 1. 실행방법

```
$ python download.py
```

```
1. cmd(terminal) -> cd 현재폴더경로 
2. python setup.py install
3. python download.py
```

* Chrome 브라우저가 설치되어 있어야 합니다.
* Python3가 이미 설치되어 있어야 합니다.
* C/C++/Python/JAVA/Text로 작성 된 소스코드만 다운로드가 가능합니다.
* 다운로드가 완료 된 소스코드들은 "./download/"에 저장됩니다.

## 2. Chromedriver가 Permission error가 날 경우
	
	1. Windows : 모든 폴더 읽기전용 권한 해제
	2. Linux/Mac : chmod a+x driver/chromedirver_linux(mac)

## 3. Upgrade가 필요한 부분

	1. Python2 버전
	2. driver 없이 Cookie 받아오기
	3. Permission error 나는 경우들 해결

## 4. Using
	1. Python3
	2. requests
	3. selenium
	4. bs4