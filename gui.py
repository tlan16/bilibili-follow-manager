#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import json
import os
import time
from bilibili_api import BilibiliAPI
from auto_login import auto_login_setup

class BilibiliManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("B站关注管理器")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # 设置现代化主题
        self.setup_theme()
        
        self.api = None
        self.following_list = []
        
        self.create_widgets()
        self.check_config()
    
    def setup_theme(self):
        """设置现代化主题"""
        style = ttk.Style()
        
        # 使用默认主题但自定义样式
        try:
            style.theme_use('vista')  # Windows现代主题
        except:
            style.theme_use('clam')   # 备用主题
        
        # 自定义颜色
        self.colors = {
            'primary': '#00A1D6',      # B站蓝
            'primary_dark': '#0084B4',
            'success': '#52C41A',
            'warning': '#FAAD14',
            'danger': '#FF4D4F',
            'bg_light': '#F8F9FA',
            'bg_dark': '#FFFFFF',
            'text_primary': '#262626',
            'text_secondary': '#8C8C8C',
            'border': '#D9D9D9'
        }
        
        # 配置按钮样式
        style.configure('Primary.TButton',
                       foreground='white',
                       padding=(20, 10),
                       font=('Microsoft YaHei UI', 10, 'bold'))
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_dark']),
                           ('!active', self.colors['primary']),
                           ('pressed', self.colors['primary_dark'])],
                 foreground=[('active', 'white'),
                           ('!active', 'white'),
                           ('pressed', 'white')])
        
        style.configure('Success.TButton',
                       padding=(15, 8),
                       font=('Microsoft YaHei UI', 9))
        
        style.configure('Danger.TButton',
                       padding=(15, 8),
                       font=('Microsoft YaHei UI', 9))
        
        # 设置根窗口背景
        self.root.configure(bg=self.colors['bg_light'])
    
    def create_widgets(self):
        # 主容器
        main_container = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = tk.Frame(main_container, bg=self.colors['bg_light'])
        title_frame.pack(fill=tk.X, pady=(0, 25))
        
        title_label = tk.Label(title_frame, 
                              text="🎬 B站关注管理器", 
                              font=("Microsoft YaHei UI", 24, "bold"),
                              fg=self.colors['primary'],
                              bg=self.colors['bg_light'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="轻松管理你的B站关注列表",
                                 font=("Microsoft YaHei UI", 11),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_light'])
        subtitle_label.pack(pady=(5, 0))
        
        # 登录状态卡片
        login_card = ttk.LabelFrame(main_container, text="  登录状态  ", padding=20)
        login_card.pack(fill=tk.X, pady=(0, 20))
        
        status_frame = tk.Frame(login_card, bg=self.colors['bg_dark'])
        status_frame.pack(fill=tk.X)
        
        # 状态指示器
        self.status_indicator = tk.Label(status_frame, text="●", font=("Arial", 16), 
                                        fg=self.colors['danger'], bg=self.colors['bg_dark'])
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = tk.Label(status_frame, text="未登录", 
                                    font=("Microsoft YaHei UI", 12, "bold"),
                                    fg=self.colors['text_primary'], bg=self.colors['bg_dark'])
        self.status_label.pack(side=tk.LEFT)
        
        self.login_button = tk.Button(status_frame, text="🔐 设置登录", 
                                     command=self.setup_login,
                                     bg=self.colors['primary'],
                                     fg='white',
                                     font=('Microsoft YaHei UI', 10, 'bold'),
                                     relief='flat',
                                     padx=20, pady=8,
                                     cursor='hand2',
                                     activebackground=self.colors['primary_dark'],
                                     activeforeground='white')
        self.login_button.pack(side=tk.RIGHT)
        
        self.user_info_label = tk.Label(login_card, text="", 
                                       font=("Microsoft YaHei UI", 10),
                                       fg=self.colors['text_secondary'], 
                                       bg=self.colors['bg_dark'])
        self.user_info_label.pack(anchor=tk.W, pady=(10, 0))
        
        # 操作按钮区域
        button_frame = tk.Frame(main_container, bg=self.colors['bg_light'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.refresh_button = tk.Button(button_frame, text="🔄 刷新关注列表", 
                                        command=self.refresh_following, 
                                        state="disabled",
                                        bg=self.colors['success'],
                                        fg='white',
                                        font=('Microsoft YaHei UI', 9),
                                        relief='flat',
                                        padx=15, pady=8,
                                        cursor='hand2',
                                        activebackground='#45B315',
                                        activeforeground='white',
                                        disabledforeground='lightgray')
        self.refresh_button.pack(side=tk.LEFT, padx=(0, 15))
        
        self.batch_unfollow_button = tk.Button(button_frame, text="❌ 批量取消关注", 
                                               command=self.batch_unfollow, 
                                               state="disabled",
                                               bg=self.colors['danger'],
                                               fg='white',
                                               font=('Microsoft YaHei UI', 9),
                                               relief='flat',
                                               padx=15, pady=8,
                                               cursor='hand2',
                                               activebackground='#E6393C',
                                               activeforeground='white',
                                               disabledforeground='lightgray')
        self.batch_unfollow_button.pack(side=tk.LEFT, padx=(0, 15))
        
        self.export_button = tk.Button(button_frame, text="📥 导出列表", 
                                       command=self.export_list, 
                                       state="disabled",
                                       bg='#1890FF',
                                       fg='white',
                                       font=('Microsoft YaHei UI', 9),
                                       relief='flat',
                                       padx=15, pady=8,
                                       cursor='hand2',
                                       activebackground='#0969CC',
                                       activeforeground='white',
                                       disabledforeground='lightgray')
        self.export_button.pack(side=tk.LEFT, padx=(0, 15))
        
        self.import_follow_button = tk.Button(button_frame, text="📤 导入关注", 
                                             command=self.import_and_follow, 
                                             state="disabled",
                                             bg='#52C41A',
                                             fg='white',
                                             font=('Microsoft YaHei UI', 9),
                                             relief='flat',
                                             padx=15, pady=8,
                                             cursor='hand2',
                                             activebackground='#389E0D',
                                             activeforeground='white',
                                             disabledforeground='lightgray')
        self.import_follow_button.pack(side=tk.LEFT)
        

        
        # 关注列表卡片
        list_card = ttk.LabelFrame(main_container, text="  关注列表  ", padding=15)
        list_card.pack(fill=tk.BOTH, expand=True)
        
        # 列表工具栏
        list_toolbar = tk.Frame(list_card, bg=self.colors['bg_dark'])
        list_toolbar.pack(fill=tk.X, pady=(0, 15))
        
        self.select_all_button = tk.Button(list_toolbar, text="全选", 
                                           command=self.select_all, state="disabled",
                                           bg='#F0F0F0',
                                           fg=self.colors['text_primary'],
                                           font=('Microsoft YaHei UI', 8),
                                           relief='flat',
                                           padx=12, pady=5,
                                           cursor='hand2',
                                           activebackground='#E0E0E0')
        self.select_all_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.select_none_button = tk.Button(list_toolbar, text="取消全选", 
                                            command=self.select_none, state="disabled",
                                            bg='#F0F0F0',
                                            fg=self.colors['text_primary'],
                                            font=('Microsoft YaHei UI', 8),
                                            relief='flat',
                                            padx=12, pady=5,
                                            cursor='hand2',
                                            activebackground='#E0E0E0')
        self.select_none_button.pack(side=tk.LEFT)
        
        self.count_label = tk.Label(list_toolbar, text="共 0 个关注", 
                                   font=("Microsoft YaHei UI", 10),
                                   fg=self.colors['text_secondary'], 
                                   bg=self.colors['bg_dark'])
        self.count_label.pack(side=tk.RIGHT)
        
        # 创建表格容器
        table_frame = tk.Frame(list_card, bg=self.colors['bg_dark'])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview
        columns = ("用户名", "UID", "关注时间", "签名")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="tree headings", height=15)
        
        # 设置列标题
        self.tree.heading("#0", text="✓")
        self.tree.heading("用户名", text="👤 用户名")
        self.tree.heading("UID", text="🆔 UID")
        self.tree.heading("关注时间", text="⏰ 关注时间")
        self.tree.heading("签名", text="📝 签名")
        
        # 设置列宽
        self.tree.column("#0", width=60, minwidth=60)
        self.tree.column("用户名", width=180, minwidth=150)
        self.tree.column("UID", width=120, minwidth=100)
        self.tree.column("关注时间", width=150, minwidth=120)
        self.tree.column("签名", width=300, minwidth=200)
        self.tree.column("关注时间", width=160, minwidth=140)
        
        # 滚动条
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 布局
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 状态栏
        status_frame = tk.Frame(main_container, bg=self.colors['bg_light'], height=30)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        status_frame.pack_propagate(False)
        
        self.status_bar = tk.Label(status_frame, text="🎯 准备就绪", 
                                  font=("Microsoft YaHei UI", 10),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_light'], anchor=tk.W)
        self.status_bar.pack(fill=tk.BOTH, padx=10, pady=5)
    
    def check_config(self):
        if os.path.exists('config.json'):
            try:
                self.api = BilibiliAPI()
                user_info = self.api.get_user_info()
                if user_info:
                    self.status_indicator.config(fg=self.colors['success'])
                    self.status_label.config(text="已登录", fg=self.colors['success'])
                    self.user_info_label.config(text=f"👋 欢迎回来，{user_info.get('uname', '未知')} (ID: {user_info.get('mid', '未知')})")
                    self.login_button.config(text="🚪 退出登录", command=self.logout, bg=self.colors['danger'])
                    self.enable_buttons()
                    self.update_status("✅ 登录成功，可以开始使用了")
                else:
                    self.status_indicator.config(fg=self.colors['warning'])
                    self.status_label.config(text="登录已过期", fg=self.colors['warning'])
                    self.login_button.config(text="🔐 设置登录", command=self.setup_login, bg=self.colors['primary'])
                    self.update_status("⚠️ 登录信息已过期，请重新设置")
            except Exception:
                self.status_indicator.config(fg=self.colors['danger'])
                self.status_label.config(text="配置错误", fg=self.colors['danger'])
                self.login_button.config(text="🔐 设置登录", command=self.setup_login, bg=self.colors['primary'])
                self.update_status("❌ 配置文件错误")
        else:
            self.login_button.config(text="🔐 设置登录", command=self.setup_login, bg=self.colors['primary'])
            self.update_status("💡 首次使用？点击\"设置登录\"开始吧")
    
    def setup_login(self):
        def login_thread():
            self.update_status("🔄 正在设置登录...")
            self.login_button.config(state="disabled")
            
            try:
                success = auto_login_setup()
                if success:
                    self.root.after(0, self.login_success)
                else:
                    self.root.after(0, self.login_failed)
            except Exception:
                self.root.after(0, self.login_failed)
        
        thread = threading.Thread(target=login_thread)
        thread.daemon = True
        thread.start()
    
    def logout(self):
        """退出登录，删除配置文件"""
        # 确认退出
        if not messagebox.askyesno("🚪 确认退出", 
                                  "确定要退出登录吗？\n\n这将删除本地保存的登录信息，\n下次需要重新登录。", 
                                  icon="question"):
            return
        
        try:
            # 删除配置文件
            if os.path.exists('config.json'):
                os.remove('config.json')
            
            # 重置API对象
            self.api = None
            
            # 重置UI状态
            self.status_indicator.config(fg=self.colors['danger'])
            self.status_label.config(text="未登录", fg=self.colors['text_primary'])
            self.user_info_label.config(text="")
            self.login_button.config(text="🔐 设置登录", command=self.setup_login, bg=self.colors['primary'])
            
            # 禁用所有功能按钮
            self.refresh_button.config(state="disabled")
            self.batch_unfollow_button.config(state="disabled")
            self.export_button.config(state="disabled")
            self.import_follow_button.config(state="disabled")
            self.select_all_button.config(state="disabled")
            self.select_none_button.config(state="disabled")
            
            # 清空关注列表
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.following_list = []
            self.count_label.config(text="共 0 个关注")
            
            # 更新状态
            self.update_status("🚪 已退出登录，点击\"设置登录\"重新开始")
            messagebox.showinfo("🎉 退出成功", "已成功退出登录！")
            
        except Exception as e:
            messagebox.showerror("❌ 错误", f"退出登录失败：{str(e)}")
            self.update_status("❌ 退出登录失败")

    def login_success(self):
        self.login_button.config(state="normal")
        messagebox.showinfo("🎉 成功", "登录设置成功！")
        self.check_config()  # 重新检查配置，更新按钮状态
    
    def login_failed(self):
        self.login_button.config(state="normal")
        messagebox.showerror("❌ 错误", "登录设置失败")
        self.update_status("❌ 登录设置失败")
    
    def enable_buttons(self):
        self.refresh_button.config(state="normal")
        self.batch_unfollow_button.config(state="normal")
        self.export_button.config(state="normal")
        self.import_follow_button.config(state="normal")
        self.select_all_button.config(state="normal")
        self.select_none_button.config(state="normal")
    
    def refresh_following(self):
        def refresh_thread():
            self.root.after(0, lambda: self.refresh_button.config(state="disabled"))
            self.root.after(0, lambda: self.update_status("🔄 正在获取关注列表..."))
            
            try:
                following_list = self.api.get_all_following()
                self.root.after(0, lambda: self.update_following_list(following_list))
            except Exception:
                self.root.after(0, self.refresh_failed)
        
        thread = threading.Thread(target=refresh_thread)
        thread.daemon = True
        thread.start()
    
    def update_following_list(self, following_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.following_list = following_list
        
        for user in following_list:
            # 格式化时间显示
            mtime_str = user.get('mtime_str', '未知')
            
            # 获取签名，如果为空则显示默认值
            sign = user.get('sign', '').strip()
            if not sign:
                sign = '暂无签名'
            
            self.tree.insert("", tk.END, values=(
                user.get('uname', '未知'),
                user.get('mid', ''),
                mtime_str,
                sign
            ))
        
        self.refresh_button.config(state="normal")
        self.count_label.config(text=f"共 {len(following_list)} 个关注")
        self.update_status(f"✅ 已加载 {len(following_list)} 个关注用户")
    
    def refresh_failed(self):
        self.refresh_button.config(state="normal")
        messagebox.showerror("❌ 错误", "获取关注列表失败")
        self.update_status("❌ 获取关注列表失败")
    
    def select_all(self):
        for item in self.tree.get_children():
            self.tree.selection_add(item)
    
    def select_none(self):
        self.tree.selection_remove(self.tree.selection())
    
    def batch_unfollow(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("⚠️ 警告", "请先选择要取消关注的用户")
            return
        
        count = len(selected_items)
        if not messagebox.askyesno("⚠️ 确认操作", 
                                  f"确定要取消关注 {count} 个用户吗？\n\n⚠️ 此操作不可撤销！", 
                                  icon="warning"):
            return
        
        def unfollow_thread():
            self.root.after(0, lambda: self.batch_unfollow_button.config(state="disabled"))
            
            success_count = 0
            for item in selected_items:
                try:
                    values = self.tree.item(item)['values']
                    uid = int(values[1])
                    username = values[0]
                    
                    self.root.after(0, lambda u=username: self.update_status(f"🔄 正在取消关注: {u}"))
                    
                    if self.api.unfollow_user(uid):
                        success_count += 1
                        self.root.after(0, lambda i=item: self.tree.delete(i))
                
                except Exception:
                    continue
            
            self.root.after(0, lambda: self.batch_unfollow_button.config(state="normal"))
            self.root.after(0, lambda: self.count_label.config(text=f"共 {len(self.tree.get_children())} 个关注"))
            self.root.after(0, lambda: self.update_status(f"✅ 完成！成功取消关注 {success_count} 个用户"))
            self.root.after(0, lambda: messagebox.showinfo("🎉 完成", f"成功取消关注 {success_count} 个用户"))
        
        thread = threading.Thread(target=unfollow_thread)
        thread.daemon = True
        thread.start()
    
    def export_list(self):
        if not self.following_list:
            messagebox.showwarning("⚠️ 警告", "关注列表为空")
            return
        
        try:
            # 只导出重要的数据字段
            simplified_list = []
            for user in self.following_list:
                simplified_user = {
                    '用户名': user.get('uname', '未知'),
                    'UID': user.get('mid', ''),
                    '关注时间': user.get('mtime_str', '未知'),
                    '关注时间戳': user.get('mtime', ''),
                    '签名': user.get('sign', '').strip() or '暂无签名',
                    '官方认证': user.get('official_verify', {}).get('desc', '') if user.get('official_verify') else '',
                    '头像链接': user.get('face', '')
                }
                simplified_list.append(simplified_user)
            
            filename = f"bilibili_following_{len(simplified_list)}_users_简化版.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(simplified_list, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("🎉 成功", f"关注列表已导出到:\n{filename}\n\n📊 已导出 {len(simplified_list)} 个用户的重要信息")
            self.update_status(f"📥 列表已导出到 {filename}")
        except Exception as e:
            messagebox.showerror("❌ 错误", f"导出失败：{str(e)}")
    
    def import_and_follow(self):
        """导入文件并批量关注所有用户"""
        # 选择文件
        file_path = filedialog.askopenfilename(
            title="选择要导入的关注列表文件",
            filetypes=[
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ],
            initialdir=os.getcwd()
        )
        
        if not file_path:
            return
        
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                user_list = json.load(f)
            
            if not isinstance(user_list, list):
                messagebox.showerror("❌ 错误", "文件格式不正确，应该是包含用户列表的JSON数组")
                return
            
            if not user_list:
                messagebox.showerror("❌ 错误", "文件中没有用户数据")
                return
            
            # 检测文件格式并提取UID
            uids_to_follow = []
            file_format = "unknown"
            
            # 检查是否是简化版格式（中文字段名）
            if 'UID' in user_list[0]:
                file_format = "simplified"
                for user in user_list:
                    uid = user.get('UID')
                    if uid:
                        uids_to_follow.append(int(uid))
            
            # 检查是否是原始格式（英文字段名）
            elif 'mid' in user_list[0]:
                file_format = "original"
                for user in user_list:
                    uid = user.get('mid')
                    if uid:
                        uids_to_follow.append(int(uid))
            
            if not uids_to_follow:
                messagebox.showerror("❌ 错误", "文件中没有找到有效的用户ID")
                return
            
            # 确认操作
            username_sample = ""
            if file_format == "simplified" and 'username' in user_list[0]:
                username_sample = f"\n例如：{user_list[0].get('用户名', '未知')}"
            elif file_format == "original" and 'uname' in user_list[0]:
                username_sample = f"\n例如：{user_list[0].get('uname', '未知')}"
            
            if not messagebox.askyesno("🔔 确认批量关注", 
                                      f"确定要关注文件中的 {len(uids_to_follow)} 个用户吗？{username_sample}\n\n"
                                      f"⚠️ 此操作将会逐个关注这些用户\n"
                                      f"⏱️ 预计需要 {len(uids_to_follow)//10}-{len(uids_to_follow)//5} 分钟",
                                      icon="question"):
                return
            
            # 开始批量关注
            self.start_batch_follow(uids_to_follow, file_path)
            
        except json.JSONDecodeError:
            messagebox.showerror("❌ 错误", "文件不是有效的JSON格式")
        except Exception as e:
            messagebox.showerror("❌ 错误", f"读取文件失败：{str(e)}")
    
    def start_batch_follow(self, uids_to_follow, file_path):
        """开始批量关注操作"""
        def follow_thread():
            self.root.after(0, lambda: self.import_follow_button.config(state="disabled"))
            self.root.after(0, lambda: self.update_status("🔄 正在批量关注用户..."))
            
            success_count = 0
            failed_count = 0
            total = len(uids_to_follow)
            
            for i, uid in enumerate(uids_to_follow):
                try:
                    self.root.after(0, lambda current=i+1, total=total: 
                                  self.update_status(f"🔄 正在关注用户 ({current}/{total})..."))
                    
                    if self.api.follow_user(uid):
                        success_count += 1
                    else:
                        failed_count += 1
                    
                    # 避免操作过快
                    time.sleep(1.0)  # 固定延迟1秒
                    
                except Exception as e:
                    failed_count += 1
                    print(f"关注用户 {uid} 失败: {e}")  # 使用print替代logger
            
            self.root.after(0, lambda: self.import_follow_button.config(state="normal"))
            
            # 显示结果
            result_msg = f"🎉 批量关注完成！\n\n✅ 成功关注: {success_count} 个用户\n"
            if failed_count > 0:
                result_msg += f"❌ 失败: {failed_count} 个用户\n"
            result_msg += f"📁 源文件: {os.path.basename(file_path)}"
            
            self.root.after(0, lambda: messagebox.showinfo("🎉 完成", result_msg))
            self.root.after(0, lambda: self.update_status(f"✅ 批量关注完成！成功 {success_count} 个，失败 {failed_count} 个"))
            
            # 刷新关注列表
            if success_count > 0:
                self.root.after(2000, self.refresh_following)  # 2秒后自动刷新
        
        thread = threading.Thread(target=follow_thread)
        thread.daemon = True
        thread.start()
    
    def update_status(self, message):
        self.status_bar.config(text=message)

def main():
    root = tk.Tk()
    app = BilibiliManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
