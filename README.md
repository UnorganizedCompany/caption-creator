# caption-creator

## name_with_image ver.

* 이름 대신 이미지를 사용하고 싶은 경우에 사용 가능한 버전

### 프로그램 실행 순서
1. 프로그램 실행 전 `main.py`와 같은 폴더 내에 `dist`, `image` 폴더를 생성
2. 작업할 자막 파일(`srt_file.srt`)를 `main.py`와 같은 폴더 내에 위치
    * 아래 예시에서 각 index (1, 2)가 한 이미지로 생성됨
    ```
    1
    01:00:31,840 --> 01:00:34,800
    test1:first line
    second line
   
    2
    01:00:35,000 --> 01:00:40,400
    test2:first line
    second line
    third line
    
    
    ```
    * 위와 같이 입력한 경우 첫 `:`앞에 적힌 문자열을 이미지 파일 명으로 인식함
    * 따라서 `test1.png`, `test2.png`(확장자 주의)를 이름 대신 사용하게 됨
    * **`srt` 파일의 마지막에는 두 줄의 공백이 있어야 함**
3. 이름 대신 삽입할 이미지 파일을 `image` 폴더 내에 위치
4. **자막**(이미지 파일에는 적용되지 않음)에 테두리를 넣고 싶은 경우, color_map.yml을 아래와 같이 수정
    ```yaml
    test1:
      r: 20
      g: 20
      b: 200
      a: 256
    test2:
      r: 200
      g: 200
      b: 20
      a: 256
    ```
    * **srt 파일에 명시한 것과 동일한 값이 사용해야 함**
    * 만약 color-map.yml에 srt 파일에 명시한 이름이 없다면 테두리가 생성되지 않음
5. main.py 실행
    ```python
    python main.py srt_file.srt
    ```
