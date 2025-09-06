import copy
import json
from typing import Dict, List, Iterable, Generator

from bilibili_api import BilibiliAPI
import sys
import os
import time
api = BilibiliAPI()


def get_app_dir():
    """获取应用程序目录"""
    if getattr(sys, 'frozen', False):
        # 打包后的可执行文件
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        return os.path.dirname(os.path.abspath(__file__))

def welcome_back(user_info) -> None:
    user_info = api.get_user_info()
    print("已登录")
    print(f"👋 欢迎回来，{user_info.get('uname', '未知')} (ID: {user_info.get('mid', '未知')})")
    print("✅ 登录成功，可以开始使用了")

def check_config() -> Dict | None:
    config_path = os.path.join(get_app_dir(), 'config.json')
    if os.path.exists(config_path):
        try:
            user_info = api.get_user_info()
            if user_info:
                return user_info
            else:
                print("⚠️ 登录信息已过期，请重新设置")
        except Exception as e:
            print(f"❌ 配置文件错误. {e}")
    else:
        print("💡 首次使用？登录吧")

def generate_newpipe_data(following_list_generator: Iterable[Dict]) -> Dict:
    result = {
        "app_version": "4.7.2",
        "app_version_int": 108500,
        "subscriptions": []
    }

    for user in following_list_generator:
        user_with_newpipe_fields = copy.deepcopy(user)
        mid = user.get('mid')
        uname = user.get('uname')
        if mid and uname:
            result['subscriptions'].append({
                "service_id": 5,
                "url": f"https://space.bilibili.com/{mid}",
                "name": uname
            })
    return result

def get_all_following() -> Generator[Dict]:
    print("🔄 正在获取关注列表...")
    yield from api.get_all_following()

def export_list():
    bilibili_data = list(get_all_following())
    newpipe_data = generate_newpipe_data(bilibili_data)
    localtime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    filename_raw = f"bilibili_following_{localtime}_{len(bilibili_data)}_raw.json"

    # Example: newpipe_subscriptions_202509061543.json
    localtime = time.strftime("%Y%m%d%H%M", time.localtime())
    filename_newpipe = f"newpipe_subscriptions_{localtime}.json"
    # 将文件保存到应用程序目录
    file_path = os.path.join(get_app_dir(), filename_raw)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(filename_raw, f, indent=2, ensure_ascii=False)
    print("🎉 成功", f"关注列表已导出到:\n{file_path}\n\n📊 已导出 {len(filename_raw)} 个用户的重要信息")

    file_path = os.path.join(get_app_dir(), filename_newpipe)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(newpipe_data, f, ensure_ascii=False)
    print("🎉 成功", f"关注列表已导出到:\n{file_path}\n\n📊 已导出 {len(filename_newpipe)} 个用户的重要信息")


def main() -> None:
    from auto_login import auto_login_setup
    user_info = check_config()
    if user_info:
        welcome_back(user_info)
    else:
        auto_login_setup()
    assert check_config(), "登录失败，无法继续"

    export_list()


if __name__ == "__main__":
    main()
