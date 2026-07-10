import feedparser
import os

# 벨로그 RSS 피드 URL
# example : rss_url = 'https://api.velog.io/rss/@soozi'
rss_url = 'https://api.velog.io/rss/@miy7625'

# 깃허브 레포지토리 경로
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 각 글을 파일로 저장
for entry in feed.entries:
    # 파일 이름에서 유효하지 않은 문자 제거 또는 대체
    file_name = entry.title
    file_name = file_name.replace('/', '-')  # 슬래시를 대시로 대체
    file_name = file_name.replace('\\', '-')  # 백슬래시를 대시로 대체
    # 필요에 따라 추가 문자 대체
    file_name += '.md'
    file_path = os.path.join(posts_dir, file_name)

    new_content = entry.description

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            old_content = file.read()
    else:
        old_content = None

    # 파일이 없거나 Velog 글 내용이 바뀌었으면 업데이트
    if old_content != new_content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)  # 글 내용을 파일에 작성
