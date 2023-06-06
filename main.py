import sys
import os

# 검색 키워드
keyword = sys.argv[1]

# 이미지 장 수
numImages = int(sys.argv[2])

# 결과물을 저장할 폴더 이름
result_dir = sys.argv[3]
if result_dir not in os.listdir():
    os.mkdir(result_dir)

# (True / False)
high_resolution = sys.argv[4]

if high_resolution in "True true":
    import my_selenium2x as pc
elif high_resolution in "False false":
    import my_selenium as pc

# 크롤링을 수행합니다
pc.crawling(keyword, numImages, result_dir)