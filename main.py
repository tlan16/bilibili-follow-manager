#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from bilibili_api import BilibiliAPI
import logging

def confirm_batch_unfollow(total_count: int) -> bool:
    """确认批量取消关注操作"""
    print(f"\n⚠️  警告：您即将取消关注 {total_count} 个用户！")
    print("❌ 这个操作是不可逆的，一旦执行将无法恢复。")
    print("\n请仔细考虑是否继续...")
    
    while True:
        choice = input("\n确认要继续吗？(yes/no): ").lower().strip()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("请输入 'yes' 或 'no'")

def display_user_info(api: BilibiliAPI):
    """显示用户信息"""
    try:
        user_info = api.get_user_info()
        if user_info:
            print(f"\n👤 当前登录用户: {user_info.get('uname', '未知')}")
            print(f"🆔 用户ID: {user_info.get('mid', '未知')}")
            print(f"💰 硬币数: {user_info.get('money', 0)}")
            print(f"📊 等级: {user_info.get('level_info', {}).get('current_level', 0)}")
    except Exception as e:
        print(f"获取用户信息失败: {e}")

def display_following_stats(api: BilibiliAPI):
    """显示关注统计"""
    try:
        print("\n📊 正在获取关注统计...")
        following_list = api.get_all_following()
        
        if not following_list:
            print("❌ 没有找到任何关注用户")
            return
        
        print(f"\n📈 关注统计:")
        print(f"  总关注数: {len(following_list)}")
        
        # 显示前10个关注用户
        print(f"\n👥 最近关注的用户 (前10个):")
        for i, user in enumerate(following_list[:10], 1):
            print(f"  {i}. {user['uname']} (ID: {user['mid']})")
            
        if len(following_list) > 10:
            print(f"  ... 还有 {len(following_list) - 10} 个用户")
            
    except Exception as e:
        print(f"获取关注统计失败: {e}")

def batch_unfollow_menu(api: BilibiliAPI):
    """批量取消关注菜单"""
    print(f"\n🗑️ 批量取消关注")
    print("=" * 50)
    
    try:
        # 显示统计信息
        display_following_stats(api)
        
        print(f"\n⚠️  注意事项:")
        print("  1. 此操作将取消关注所有用户")
        print("  2. 操作无法撤销，请谨慎考虑")
        print("  3. 操作过程可能需要较长时间")
        
        choice = input("\n是否继续？(y/n): ").lower().strip()
        if choice not in ['y', 'yes']:
            print("操作已取消")
            return
        
        # 执行批量取消关注
        result = api.batch_unfollow_all(confirm_callback=confirm_batch_unfollow)
        
        if result.get('cancelled'):
            print("\n❌ 操作已被用户取消")
        else:
            print(f"\n✅ 批量取消关注完成!")
            print(f"📊 结果统计:")
            print(f"  总数: {result['total']}")
            print(f"  成功: {result['success']}")
            print(f"  失败: {result['failed']}")
            
            if result['failed'] > 0:
                print(f"\n⚠️  有 {result['failed']} 个用户取消关注失败，可能是网络问题或API限制")
                
    except Exception as e:
        print(f"❌ 批量取消关注失败: {e}")

def main_menu():
    """主菜单"""
    print("\n" + "=" * 50)
    print("🎬 Bilibili 关注管理器")
    print("=" * 50)
    print("1. 查看用户信息")
    print("2. 查看关注统计")
    print("3. 批量取消所有关注")
    print("0. 退出程序")
    print("=" * 50)

def main():
    """主函数"""
    print("🎬 Bilibili 关注管理器")
    print("正在初始化...")
    
    # 检查配置文件
    if not os.path.exists('config.json'):
        print("\n❌ 错误: 配置文件 config.json 不存在")
        print("请复制 config.example.json 为 config.json 并填入您的登录信息")
        sys.exit(1)
    
    try:
        # 初始化API客户端
        api = BilibiliAPI()
        
        # 验证登录状态
        user_info = api.get_user_info()
        if not user_info:
            print("\n❌ 登录验证失败，请检查配置文件中的登录信息")
            sys.exit(1)
        
        print(f"✅ 登录成功! 欢迎，{user_info.get('uname', '用户')}")
        
        while True:
            main_menu()
            
            try:
                choice = input("\n请选择操作 (0-3): ").strip()
                
                if choice == '0':
                    print("\n👋 再见!")
                    break
                elif choice == '1':
                    display_user_info(api)
                elif choice == '2':
                    display_following_stats(api)
                elif choice == '3':
                    batch_unfollow_menu(api)
                else:
                    print("❌ 无效选择，请输入 0-3 之间的数字")
                    
            except KeyboardInterrupt:
                print("\n\n👋 程序被用户中断，再见!")
                break
            except EOFError:
                print("\n\n👋 再见!")
                break
                
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        logging.exception("程序异常")
        sys.exit(1)

if __name__ == "__main__":
    main()
