def main():
    try:
        from gui import main 
        main()
    except Exception as e:
        print(f"程序运行时出错: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
