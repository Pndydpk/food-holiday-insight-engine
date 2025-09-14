from kaggle.api.kaggle_api_extended import KaggleApi
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')
os.makedirs(RAW_PATH, exist_ok=True)

api = KaggleApi()
api.authenticate()
api.dataset_download_files(
    "ahmedshahriarsakib/uber-eats-usa-restaurants-menus",
    path=RAW_PATH,
    unzip=True
)

print(f"✅ Dataset downloaded and unzipped to {RAW_PATH}")