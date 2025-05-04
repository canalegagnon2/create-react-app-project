import json
import pandas as pd
import os

PROFILE_MAP_PATH = "profile_map.json"
ACCOUNT_PATH = "data/accounts.csv"
ASSIGNMENTS_PATH = "tweet_token_assignments.json"
TWEET_COLUMN = "tweets"


def load_tokens():
    df = pd.read_csv(ACCOUNT_PATH)
    return [t for t in df[TWEET_COLUMN].dropna().astype(str).tolist() if t.strip()]


def main():
    print("🔧 正在根据现有 profile_map.json 分配发推 token...")
    if not os.path.exists(PROFILE_MAP_PATH):
        raise Exception("❌ 未找到 profile_map.json，请先运行评论初始化脚本生成浏览器 profile")

    with open(PROFILE_MAP_PATH, "r", encoding="utf-8") as f:
        profile_map = json.load(f)

    tokens = load_tokens()
    assignments = {}
    profile_keys = list(profile_map.keys())

    for i, token in enumerate(tokens):
        key = profile_keys[i % len(profile_keys)]
        if key not in assignments:
            assignments[key] = []
        assignments[key].append(token)

    with open(ASSIGNMENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(assignments, f, indent=2)

    print(f"✅ 已为 {len(tokens)} 个 token 分配至 {len(profile_map)} 个 profile")


if __name__ == "__main__":
    main()