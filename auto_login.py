#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import Dict, Optional

class BilibiliAutoLogin:
    
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
    
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--window-size=1280,720')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def manual_login_bilibili(self) -> Optional[Dict]:
        try:
            self.setup_driver()
            print("正在打开B站登录页面...")
            if self.driver != None:
                self.driver.get("https://passport.bilibili.com/login")
            
            print("请在浏览器中手动登录，程序将自动检测登录状态...")
            
            max_wait_time = 300
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                try:
                    if self.driver != None:
                        current_url = self.driver.current_url
                    
                    if any([
                        "www.bilibili.com" in current_url and "passport" not in current_url,
                        "space.bilibili.com" in current_url,
                        "member.bilibili.com" in current_url
                    ]):
                        print("登录成功！正在获取凭据...")
                        break
                        
                    time.sleep(2)
                except Exception:
                    time.sleep(2)
                    continue
            else:
                print("登录超时")
                return None
            
            if self.driver != None:
                cookies = self.driver.get_cookies()
            cookie_dict = {}
            
            for cookie in cookies:
                if cookie['name'] in ['SESSDATA', 'bili_jct', 'DedeUserID', 'DedeUserID__ckMd5']:
                    cookie_dict[cookie['name']] = cookie['value']
            
            if 'SESSDATA' in cookie_dict and 'bili_jct' in cookie_dict:
                return cookie_dict
            else:
                print("获取凭据失败")
                return None
                
        except Exception as e:
            print(f"登录失败: {e}")
            return None
            
        finally:
            if self.driver:
                try:
                    time.sleep(2)
                    self.driver.quit()
                except:
                    pass

    def create_config_file(self, cookies: Dict) -> bool:
        try:
            config_template = {
                "cookies": {
                    "SESSDATA": "",
                    "bili_jct": "",
                    "DedeUserID": ""
                },
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Referer": "https://www.bilibili.com/"
                },
                "settings": {
                    "delay_between_requests": 1.0,
                    "max_retries": 3,
                    "batch_size": 50,
                    "test_mode": False,
                    "max_test_operations": 5
                }
            }
            
            config_template["cookies"]["SESSDATA"] = cookies.get("SESSDATA", "")
            config_template["cookies"]["bili_jct"] = cookies.get("bili_jct", "")
            config_template["cookies"]["DedeUserID"] = cookies.get("DedeUserID", "")
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config_template, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"创建配置文件失败: {e}")
            return False

def auto_login_setup() -> bool:
    print("程序将打开B站登录页面，请手动登录")
    
    login_tool = BilibiliAutoLogin()
    cookies = login_tool.manual_login_bilibili()
    
    if cookies and login_tool.create_config_file(cookies):
        print("登录成功！")
        return True
    else:
        print("登录失败")
        return False

if __name__ == "__main__":
    auto_login_setup()
