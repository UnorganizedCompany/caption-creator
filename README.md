# caption-creator

## name_with_image ver.

* 이름 대신 이미지를 사용하고 싶은 경우에 사용 가능한 버전

### 프로그램 실행 순서
1. 프로그램 실행 전 `main.py`와 같은 폴더 내에 `dist`, `images` 폴더를 생성
2. 작업할 자막 파일(`srt_file.srt`)를 `main.py`와 같은 폴더 내에 위치
    * 한 이미지로 생성될 자막이 아래와 같은 구조여야 함
    ```
    1
    01:00:31,840 --> 01:00:34,800
    tb_normal:first line
    second line
   
    2
    01:00:35,000 --> 01:00:40,400
    tb_smile:first line
    second line
    third line
    
    
    ```
    * 위와 같이 입력한 경우 `:`앞에 적힌 문자열을 이미지 파일 명으로 인식함
    * 따라서 `tb_normal.png`, `tb_smile.png`(확장자 주의)를 이름 대신 사용하게 됨
    * **`srt` 파일의 마지막에는 두 줄의 공백이 있어야 함**
3. 이름 대신 삽입할 이미지 파일을 `images` 폴더 내에 위치
4. **자막**(이미지 파일에는 적용되지 )에 테두리를 넣고 싶은 경우, color_map.yml을 아래와 같이 수정
    ```yaml
    color_map:
      tb_normal:
        r: 20
        g: 20
        b: 200
        a: 256
      tb_smile:
        r: 200
        g: 200
        b: 20
        a: 256
    ```
    * **colorMap 하위에 srt 파일에 명시한 것과 동일한 값을 사용해야 함**
5. main.py 실행
    ```python
    python main.py srt_file.srt
    ```
