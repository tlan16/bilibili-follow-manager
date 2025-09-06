import json
from typing import Dict, List

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

def refresh_following():
    print("🔄 正在获取关注列表...")
    return api.get_all_following()

def export_list(following_list: List[Dict]):
    localtime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    filename = f"bilibili_following_{localtime}_{len(following_list)}_users.json"
    # 将文件保存到应用程序目录
    file_path = os.path.join(get_app_dir(), filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(following_list, f, indent=2, ensure_ascii=False)

    print("🎉 成功", f"关注列表已导出到:\n{file_path}\n\n📊 已导出 {len(following_list)} 个用户的重要信息")
    print(f"📥 列表已导出到 {filename}")


def main() -> None:
    from auto_login import auto_login_setup
    user_info = check_config()
    if user_info:
        welcome_back(user_info)
    else:
        auto_login_setup()
    assert check_config(), "登录失败，无法继续"

    following_list = refresh_following()
    print(f"总共获取到 {len(following_list)} 个关注用户")
    export_list(following_list)


if __name__ == "__main__":
    main()
