import json
import os


def load_data(filepath):
    """JSON 파일을 읽어 Python 객체(list/dict)로 반환한다.

    파일이 없으면 빈 리스트를 반환한다.
    JSON 형식이 잘못되었으면 빈 리스트를 반환한다.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_data(filepath, data):
    """Python 객체를 JSON 파일로 저장한다."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"파일 저장 중 오류 발생: {e}")