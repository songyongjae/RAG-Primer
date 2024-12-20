import os

# BASE_DIR 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ../datasets 경로를 절대 경로로 변환
RESOURCES_DIR = os.path.abspath(os.path.join(BASE_DIR, "../datasets"))

# 클러스터링 및 차원 축소 설정
MODEL_NAME = 'all-MiniLM-L6-v2'
PCA_COMPONENTS = 25
DBSCAN_EPS = 0.5
DBSCAN_MIN_SAMPLES = 2