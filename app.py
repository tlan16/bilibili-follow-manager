#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    try:
        from gui import main as gui_main
        gui_main()
    except ImportError:
        print("GUI模块导入失败")
        input("按回车键退出...")
    except Exception as e:
        print(f"程序运行时出错: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
