"""
战网管家 Pro Max Ultra - 多主题幻境版 v6.0
═══════════════════════════════════════════════════════════════════
12种主题 · 全局动效 · 剪贴板注入 · 最近使用追踪 · 智能转到当前
═══════════════════════════════════════════════════════════════════
"""

import sys
import os
import json
import time
import subprocess
import threading
import re
import random
import math
import ctypes
import shutil
from datetime import datetime, timedelta

import requests
import pyautogui
import keyboard

from PySide6.QtCore import (Qt, Signal, QObject, QTimer, QPointF, QRectF,
                            QPropertyAnimation, QEasingCurve, Property, QSize)
from PySide6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout,
                               QGridLayout, QFileDialog, QHeaderView, QTableWidgetItem,
                               QAbstractItemView, QLabel, QLineEdit, QPushButton, QFrame,
                               QTableWidget, QGraphicsDropShadowEffect, QGraphicsOpacityEffect,
                               QScrollArea, QSystemTrayIcon, QMenu, QSlider, QCheckBox,
                               QMessageBox)
from PySide6.QtGui import (QFont, QColor, QPainter, QRadialGradient, QLinearGradient,
                           QBrush, QPen, QPainterPath, QPolygonF, QConicalGradient,
                           QTransform, QIcon, QPixmap, QAction, QKeySequence, QShortcut,
                           QCursor)

# ═══════════════════════════════════════════════════════════════════
# 全局配置 & 常量
# ═══════════════════════════════════════════════════════════════════

# 关闭 pyautogui 角落 fail-safe，避免鼠标移到屏幕角落时崩溃
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0  # 我们手动控制延迟

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATH = os.path.join(BASE_DIR, "accounts.txt")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# 战网默认路径
DEFAULT_BNET_DIR = r"D:\Program Files (x86)\Battle.net"
DEFAULT_BNET_LAUNCHER = os.path.join(DEFAULT_BNET_DIR, "Battle.net Launcher.exe")

# 风控关键词
RISK_KEYWORDS = ("风控", "封号", "异常")

# 最近使用时间显示阈值（天）
RECENT_USE_THRESHOLD_DAYS = 7

# 文件读写锁
_FILE_LOCK = threading.Lock()


# ═══════════════════════════════════════════════════════════════════
# 主题配置中心
# ═══════════════════════════════════════════════════════════════════

THEMES = {
    'cyberpunk': {
        'name': '🌃 赛博朋克',
        'name_en': 'CYBERPUNK',
        'category': '赛博',
        'bg_color': QColor(2, 2, 8),
        'primary': QColor(0, 255, 255),
        'secondary': QColor(255, 0, 128),
        'accent': QColor(255, 215, 0),
        'text_color': '#00FFFF',
        'text_secondary': '#A5B4FC',
        'card_bg': 'rgba(5, 10, 25, 0.75)',
        'input_bg': 'rgba(0, 10, 20, 0.8)',
        'input_text': '#E0FFFF',
        'border': 'rgba(0, 255, 255, 0.3)',
        'font': "'Consolas', 'Microsoft YaHei'",
        'subtitle': 'NEXUS_FORGE :: 战网指挥终端 v6.0',
    },
    'space': {
        'name': '🌌 太空宇宙',
        'name_en': 'COSMOS',
        'category': '科幻',
        'bg_color': QColor(5, 5, 20),
        'primary': QColor(120, 180, 255),
        'secondary': QColor(220, 130, 255),
        'accent': QColor(255, 230, 150),
        'text_color': '#A8C5FF',
        'text_secondary': '#C4B5FD',
        'card_bg': 'rgba(10, 15, 40, 0.8)',
        'input_bg': 'rgba(8, 10, 30, 0.85)',
        'input_text': '#F0F4FF',
        'border': 'rgba(120, 180, 255, 0.35)',
        'font': "'Microsoft YaHei', 'Segoe UI'",
        'subtitle': '🌌 COSMOS_STATION :: 星际舰队登录系统',
    },
    'wheat': {
        'name': '🌾 金色麦田',
        'name_en': 'WHEAT',
        'category': '自然',
        'bg_color': QColor(60, 35, 15),
        'primary': QColor(255, 195, 80),
        'secondary': QColor(255, 140, 60),
        'accent': QColor(110, 180, 100),
        'text_color': '#FFD580',
        'text_secondary': '#FFE5B4',
        'card_bg': 'rgba(45, 25, 10, 0.78)',
        'input_bg': 'rgba(35, 18, 5, 0.85)',
        'input_text': '#FFF5E0',
        'border': 'rgba(255, 195, 80, 0.35)',
        'font': "'Microsoft YaHei', serif",
        'subtitle': '🌾 GOLDEN_FIELD :: 麦浪庄园 · 黄昏时分',
    },
    'candy': {
        'name': '🍭 梦幻糖果',
        'name_en': 'CANDY',
        'category': '梦幻',
        'bg_color': QColor(40, 25, 50),
        'primary': QColor(255, 150, 200),
        'secondary': QColor(180, 200, 255),
        'accent': QColor(255, 230, 130),
        'text_color': '#FFB6E1',
        'text_secondary': '#E0BBFF',
        'card_bg': 'rgba(60, 35, 75, 0.75)',
        'input_bg': 'rgba(50, 28, 65, 0.85)',
        'input_text': '#FFE4F0',
        'border': 'rgba(255, 150, 200, 0.4)',
        'font': "'Microsoft YaHei', 'Comic Sans MS'",
        'subtitle': '🍭 CANDY_LAND :: 甜蜜糖果屋',
    },
    'ocean': {
        'name': '🌊 深海秘境',
        'name_en': 'OCEAN',
        'category': '自然',
        'bg_color': QColor(5, 25, 50),
        'primary': QColor(80, 200, 220),
        'secondary': QColor(100, 230, 200),
        'accent': QColor(255, 200, 100),
        'text_color': '#7DD3FC',
        'text_secondary': '#A5F3FC',
        'card_bg': 'rgba(8, 30, 55, 0.78)',
        'input_bg': 'rgba(5, 20, 40, 0.85)',
        'input_text': '#E0F7FA',
        'border': 'rgba(80, 200, 220, 0.35)',
        'font': "'Microsoft YaHei', 'Segoe UI'",
        'subtitle': '🌊 ABYSS_DEEP :: 深海探测潜艇',
    },
    'sakura': {
        'name': '🌸 樱花飞舞',
        'name_en': 'SAKURA',
        'category': '自然',
        'bg_color': QColor(35, 20, 35),
        'primary': QColor(255, 180, 200),
        'secondary': QColor(200, 130, 180),
        'accent': QColor(255, 255, 220),
        'text_color': '#FFC8DD',
        'text_secondary': '#FFAFCC',
        'card_bg': 'rgba(50, 30, 50, 0.78)',
        'input_bg': 'rgba(40, 22, 40, 0.85)',
        'input_text': '#FFE0EC',
        'border': 'rgba(255, 180, 200, 0.4)',
        'font': "'Microsoft YaHei', 'KaiTi'",
        'subtitle': '🌸 SAKURA_NIGHT :: 月下樱花夜',
    },
    'lava': {
        'name': '🔥 熔岩地狱',
        'name_en': 'LAVA',
        'category': '极端',
        'bg_color': QColor(25, 5, 5),
        'primary': QColor(255, 100, 30),
        'secondary': QColor(255, 50, 50),
        'accent': QColor(255, 220, 80),
        'text_color': '#FF8050',
        'text_secondary': '#FFB088',
        'card_bg': 'rgba(40, 10, 5, 0.78)',
        'input_bg': 'rgba(30, 8, 5, 0.85)',
        'input_text': '#FFE0D0',
        'border': 'rgba(255, 100, 30, 0.4)',
        'font': "'Impact', 'Microsoft YaHei'",
        'subtitle': '🔥 INFERNO_CORE :: 熔岩核心 · 高温警告',
    },
    'arctic': {
        'name': '❄️ 极地冰雪',
        'name_en': 'ARCTIC',
        'category': '极端',
        'bg_color': QColor(8, 18, 35),
        'primary': QColor(150, 220, 255),
        'secondary': QColor(180, 255, 220),
        'accent': QColor(220, 200, 255),
        'text_color': '#A0E0FF',
        'text_secondary': '#C0EFFF',
        'card_bg': 'rgba(15, 25, 50, 0.78)',
        'input_bg': 'rgba(10, 20, 40, 0.85)',
        'input_text': '#E8F8FF',
        'border': 'rgba(150, 220, 255, 0.4)',
        'font': "'Microsoft YaHei', 'Segoe UI'",
        'subtitle': '❄️ AURORA_BASE :: 北极极光观测站',
    },
    'retro': {
        'name': '🎮 复古像素',
        'name_en': 'RETRO',
        'category': '复古',
        'bg_color': QColor(15, 25, 15),
        'primary': QColor(80, 255, 100),
        'secondary': QColor(255, 200, 60),
        'accent': QColor(255, 100, 200),
        'text_color': '#50FF64',
        'text_secondary': '#A0FFB0',
        'card_bg': 'rgba(15, 30, 18, 0.85)',
        'input_bg': 'rgba(10, 22, 12, 0.9)',
        'input_text': '#80FF90',
        'border': 'rgba(80, 255, 100, 0.5)',
        'font': "'Courier New', 'Consolas'",
        'subtitle': '🎮 ARCADE_MAINFRAME v1.0 - INSERT COIN',
    },
    'forest': {
        'name': '🌿 森林秘境',
        'name_en': 'FOREST',
        'category': '自然',
        'bg_color': QColor(10, 25, 15),
        'primary': QColor(140, 230, 130),
        'secondary': QColor(255, 230, 100),
        'accent': QColor(180, 255, 200),
        'text_color': '#A0E8A0',
        'text_secondary': '#C8F0C0',
        'card_bg': 'rgba(15, 35, 20, 0.78)',
        'input_bg': 'rgba(10, 25, 15, 0.85)',
        'input_text': '#E0FFE0',
        'border': 'rgba(140, 230, 130, 0.4)',
        'font': "'Microsoft YaHei', 'KaiTi'",
        'subtitle': '🌿 EMERALD_GROVE :: 翡翠林深处',
    },
    'neoncity': {
        'name': '🌆 赛博雨夜',
        'name_en': 'NEON_CITY',
        'category': '赛博',
        'bg_color': QColor(8, 12, 30),
        'primary': QColor(255, 80, 180),
        'secondary': QColor(80, 220, 255),
        'accent': QColor(255, 220, 100),
        'text_color': '#FF80B4',
        'text_secondary': '#FFAACC',
        'card_bg': 'rgba(15, 18, 40, 0.78)',
        'input_bg': 'rgba(10, 14, 30, 0.85)',
        'input_text': '#FFE8F4',
        'border': 'rgba(255, 80, 180, 0.4)',
        'font': "'Consolas', 'Microsoft YaHei'",
        'subtitle': '🌆 NEO_TOKYO 2099 :: 雨夜霓虹街区',
    },
    'storm': {
        'name': '⚡ 雷暴天空',
        'name_en': 'STORM',
        'category': '极端',
        'bg_color': QColor(20, 22, 35),
        'primary': QColor(180, 200, 255),
        'secondary': QColor(120, 100, 200),
        'accent': QColor(255, 255, 180),
        'text_color': '#C0D0FF',
        'text_secondary': '#A0B0E0',
        'card_bg': 'rgba(25, 28, 45, 0.78)',
        'input_bg': 'rgba(18, 22, 35, 0.85)',
        'input_text': '#E8F0FF',
        'border': 'rgba(180, 200, 255, 0.4)',
        'font': "'Microsoft YaHei', 'Impact'",
        'subtitle': '⚡ TEMPEST_WATCH :: 雷暴预警系统',
    },
}

CURRENT_THEME = 'cyberpunk'


def T():
    """获取当前主题配置"""
    return THEMES[CURRENT_THEME]


# ═══════════════════════════════════════════════════════════════════
# 数据层
# ═══════════════════════════════════════════════════════════════════

def get_token_from_api(secret):
    url = "http://124.223.168.199:8080/token"
    data = f'{{"token":"{secret.strip()}"}}'
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5)
        if response.status_code == 200:
            res_text = response.text.strip()
            match = re.search(r'\d{6}', res_text)
            return match.group() if match else res_text
        return f"错误:{response.status_code}"
    except Exception:
        return "网络失败"


def load_accounts():
    """
    格式（向后兼容）:
        user----pwd----secret----remark----USED/UNUSED----LASTUSED_ISO
    旧格式可能没有第5、6字段。
    """
    accounts = []
    if not os.path.exists(FILE_PATH):
        try:
            open(FILE_PATH, 'w').close()
        except Exception:
            pass
    try:
        with _FILE_LOCK:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or "----" not in line:
                        continue
                    parts = line.split("----")
                    if len(parts) < 3:
                        continue
                    acc = {
                        "user": parts[0].strip(),
                        "pwd": parts[1].strip(),
                        "secret": parts[2].strip(),
                        "remark": parts[3].strip() if len(parts) >= 4 else "",
                        "used": (len(parts) >= 5 and parts[4].strip() == "USED"),
                        "last_used": parts[5].strip() if len(parts) >= 6 else "",
                    }
                    accounts.append(acc)
    except Exception:
        pass
    return accounts


def save_accounts(db):
    try:
        with _FILE_LOCK:
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                for acc in db:
                    safe_remark = acc.get('remark', '').replace("----", " ")
                    used_flag = "USED" if acc.get('used') else "UNUSED"
                    last_used = acc.get('last_used', '') or ''
                    f.write(
                        f"{acc['user']}----{acc['pwd']}----{acc['secret']}"
                        f"----{safe_remark}----{used_flag}----{last_used}\n"
                    )
    except Exception:
        pass


def mark_account_used_now(acc):
    """标记账号为已用，并打上当前时间戳"""
    acc['used'] = True
    acc['last_used'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def format_last_used(iso_str):
    """
    格式化最近使用时间。
    阈值内显示 'MM-DD HH:MM:SS'，超过显示 '—'，空值显示 '—'。
    """
    if not iso_str:
        return "—"
    try:
        dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S")
    except Exception:
        return "—"
    now = datetime.now()
    if (now - dt) > timedelta(days=RECENT_USE_THRESHOLD_DAYS):
        return "—"
    return dt.strftime("%m-%d %H:%M:%S")


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with _FILE_LOCK:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
    return {
        "current_idx": 0,
        "theme": "cyberpunk",
        "opacity": 100,
        "stats": {},
        "auto_backup": True,
        "bnet_path": DEFAULT_BNET_LAUNCHER,
    }


def save_config(**kwargs):
    cfg = load_config()
    for k, v in kwargs.items():
        if v is not None:
            cfg[k] = v
    try:
        with _FILE_LOCK:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def backup_accounts():
    """启动时自动备份"""
    if not os.path.exists(FILE_PATH):
        return
    backup_dir = os.path.join(BASE_DIR, "backups")
    try:
        os.makedirs(backup_dir, exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        backup_file = os.path.join(backup_dir, f"accounts_{today}.txt")
        if not os.path.exists(backup_file):
            shutil.copy2(FILE_PATH, backup_file)
        # 清理 14 天前的备份
        now = time.time()
        for fname in os.listdir(backup_dir):
            fpath = os.path.join(backup_dir, fname)
            if os.path.isfile(fpath) and now - os.path.getmtime(fpath) > 14 * 86400:
                try:
                    os.remove(fpath)
                except Exception:
                    pass
    except Exception:
        pass


def increment_today_stat():
    cfg = load_config()
    stats = cfg.get("stats", {})
    today = datetime.now().strftime("%Y-%m-%d")
    stats[today] = stats.get(today, 0) + 1
    sorted_keys = sorted(stats.keys(), reverse=True)
    if len(sorted_keys) > 30:
        for k in sorted_keys[30:]:
            del stats[k]
    save_config(stats=stats)
    return stats[today]


def get_today_stat():
    cfg = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    return cfg.get("stats", {}).get(today, 0)


# ═══════════════════════════════════════════════════════════════════
# 注入工具（剪贴板法 + 输入法切换 + 窗口聚焦）
# ═══════════════════════════════════════════════════════════════════

def force_english_ime():
    """
    切换当前焦点窗口的输入法为英文。
    主要解决搜狗/QQ/微软拼音激活时 pyautogui.write 被吞字的问题。
    """
    if sys.platform != 'win32':
        return
    try:
        # 加载美式英文键盘 (0x0409)
        ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 1)
        # 通知前台窗口切换 IME
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if hwnd:
            # WM_INPUTLANGCHANGEREQUEST = 0x0050
            ctypes.windll.user32.PostMessageW(hwnd, 0x0050, 0, 0x04090409)
    except Exception:
        pass


def force_chinese_ime():
    """
    切换当前焦点窗口的输入法为中文。
    点击备注栏时自动切回中文输入，方便用户快速输入中文备注。
    """
    if sys.platform != 'win32':
        return
    try:
        # 加载中文键盘布局 (0x0804 = 简体中文)
        ctypes.windll.user32.LoadKeyboardLayoutW("00000804", 1)
        # 通知前台窗口切换 IME
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if hwnd:
            # WM_INPUTLANGCHANGEREQUEST = 0x0050
            ctypes.windll.user32.PostMessageW(hwnd, 0x0050, 0, 0x08040804)
    except Exception:
        pass


def find_battlenet_window():
    """
    查找战网登录窗口句柄。
    """
    if sys.platform != 'win32':
        return 0
    try:
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        result = {'hwnd': 0}

        def callback(hwnd, _):
            if not IsWindowVisible(hwnd):
                return True
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return True
            buf = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buf, length + 1)
            title = buf.value
            if 'Battle.net' in title or '战网' in title or 'Blizzard' in title:
                result['hwnd'] = hwnd
                return False
            return True

        EnumWindows(EnumWindowsProc(callback), 0)
        return result['hwnd']
    except Exception:
        return 0


def focus_battlenet_window():
    """尝试将战网窗口置于前台"""
    if sys.platform != 'win32':
        return False
    try:
        hwnd = find_battlenet_window()
        if hwnd:
            # 先恢复（如果最小化）再置顶
            ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            return True
    except Exception:
        pass
    return False


def _set_clipboard_text_win(text):
    """
    使用 Windows API 直接设置剪贴板，可在任意线程调用。
    比 QApplication.clipboard().setText() 更稳，不会触发跨线程警告。
    """
    if sys.platform != 'win32':
        return False
    try:
        CF_UNICODETEXT = 13
        GMEM_MOVEABLE = 0x0002
        # UTF-16-LE 加 null 结尾
        data = (text + '\0').encode('utf-16-le')
        size = len(data)
        h_mem = ctypes.windll.kernel32.GlobalAlloc(GMEM_MOVEABLE, size)
        if not h_mem:
            return False
        p_mem = ctypes.windll.kernel32.GlobalLock(h_mem)
        ctypes.memmove(p_mem, data, size)
        ctypes.windll.kernel32.GlobalUnlock(h_mem)
        # 多次重试 OpenClipboard（其他进程可能正在占用）
        opened = False
        for _ in range(8):
            if ctypes.windll.user32.OpenClipboard(0):
                opened = True
                break
            time.sleep(0.02)
        if not opened:
            ctypes.windll.kernel32.GlobalFree(h_mem)
            return False
        ctypes.windll.user32.EmptyClipboard()
        ctypes.windll.user32.SetClipboardData(CF_UNICODETEXT, h_mem)
        ctypes.windll.user32.CloseClipboard()
        return True
    except Exception:
        return False


def paste_text_via_clipboard(text):
    """
    通过剪贴板粘贴文本到当前焦点框，完全绕过输入法。
    优先使用 Win32 API（线程安全），失败时回退 Qt 剪贴板。
    """
    if not text:
        return
    ok = _set_clipboard_text_win(text)
    if not ok:
        try:
            QApplication.clipboard().setText(text)
        except Exception:
            pass
    # 给系统一点时间同步剪贴板
    time.sleep(0.05)
    pyautogui.hotkey('ctrl', 'v')


def clear_focused_input():
    """清空当前焦点输入框"""
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.03)
    pyautogui.press('backspace')
    time.sleep(0.03)


# ═══════════════════════════════════════════════════════════════════
# 信号系统
# ═══════════════════════════════════════════════════════════════════

class WorkerSignals(QObject):
    update_status = Signal(str, str)
    ui_refresh = Signal()
    trigger_f4 = Signal()
    trigger_f2 = Signal()
    trigger_f3 = Signal()
    trigger_mini = Signal()
    trigger_home = Signal()
    token_fetched_manual = Signal(str)
    token_fetched_auto = Signal(str)
    theme_changed = Signal()


signals = WorkerSignals()



# ═══════════════════════════════════════════════════════════════════
# 12 种主题独立粒子系统
# ═══════════════════════════════════════════════════════════════════

class CyberpunkParticles:
    """🌃 赛博朋克 - 粒子连线网络 + 数据流"""
    def __init__(self, w, h, count=130):
        self.w, self.h = w, h
        self.particles = []
        for _ in range(count):
            self.particles.append({
                'x': random.uniform(0, w), 'y': random.uniform(0, h),
                'vx': random.uniform(-0.8, 0.8), 'vy': random.uniform(-0.8, 0.8),
                'r': random.uniform(1.0, 3.0),
                'alpha': random.randint(80, 220),
                'color_idx': random.randint(0, 2),
                'phase': random.uniform(0, math.pi * 2),
                'pulse': random.uniform(0.02, 0.08),
            })
        self.scanlines = [{'y': random.uniform(0, h), 'speed': random.uniform(0.5, 2.0),
                           'thick': random.uniform(1.0, 3.0), 'alpha': random.randint(30, 100)}
                          for _ in range(5)]
        self.t = 0.0
        self.hex_grid = []
        for row in range(15):
            for col in range(20):
                offset_x = 25 if row % 2 else 0
                self.hex_grid.append({'x': col * 50 + offset_x, 'y': row * 45,
                                      'alpha': random.randint(10, 40),
                                      'pulse': random.uniform(0.01, 0.05)})
        # 数据流（垂直下落字符）
        self.data_streams = []
        for _ in range(6):
            self.data_streams.append({
                'x': random.uniform(0, w),
                'y': random.uniform(-200, h),
                'speed': random.uniform(2, 5),
                'len': random.randint(8, 20),
                'chars': [random.choice('01アイウエオカキ#@$%') for _ in range(20)],
            })

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.03
        for p in self.particles:
            p['x'] += p['vx']; p['y'] += p['vy']
            if p['x'] < 0 or p['x'] > w: p['vx'] *= -1
            if p['y'] < 0 or p['y'] > h: p['vy'] *= -1
        for s in self.scanlines:
            s['y'] += s['speed']
            if s['y'] > h:
                s['y'] = -10; s['speed'] = random.uniform(0.5, 2.0)
        for ds in self.data_streams:
            ds['y'] += ds['speed']
            if ds['y'] > h + 200:
                ds['y'] = -200; ds['x'] = random.uniform(0, w)

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        # 六角网格
        painter.setPen(Qt.NoPen)
        for node in self.hex_grid:
            alpha = int(node['alpha'] + 15 * math.sin(self.t * 10 * node['pulse']))
            alpha = max(5, min(60, alpha))
            painter.setBrush(QColor(0, 255, 255, alpha))
            self._draw_hex(painter, node['x'], node['y'], 8)
        # 数据流
        font = painter.font()
        font.setFamily('Consolas')
        font.setPointSize(10)
        painter.setFont(font)
        for ds in self.data_streams:
            for i, ch in enumerate(ds['chars'][:ds['len']]):
                cy = ds['y'] - i * 14
                if -10 < cy < h + 10:
                    a = int(180 * (1 - i / ds['len']))
                    if i == 0:
                        painter.setPen(QColor(200, 255, 255, 255))
                    else:
                        painter.setPen(QColor(0, 255, 128, a))
                    painter.drawText(QPointF(ds['x'], cy), ch)
        # 粒子连线
        for i in range(len(self.particles)):
            for j in range(i + 1, min(i + 12, len(self.particles))):
                p1, p2 = self.particles[i], self.particles[j]
                dx, dy = p1['x'] - p2['x'], p1['y'] - p2['y']
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < 100:
                    a = int(70 * (1 - dist / 100))
                    painter.setPen(QPen(QColor(0, 255, 255, a), 0.8))
                    painter.drawLine(QPointF(p1['x'], p1['y']), QPointF(p2['x'], p2['y']))
        # 粒子
        colors = [QColor(0, 255, 255), QColor(255, 0, 128), QColor(255, 215, 0)]
        painter.setPen(Qt.NoPen)
        for p in self.particles:
            a = int(p['alpha'] * (0.5 + 0.5 * math.sin(self.t * 10 * p['pulse'] + p['phase'])))
            a = max(20, min(255, a))
            c = colors[p['color_idx']]
            painter.setBrush(QColor(c.red(), c.green(), c.blue(), a))
            painter.drawEllipse(QPointF(p['x'], p['y']), p['r'], p['r'])
        # 扫描线
        for s in self.scanlines:
            grad = QLinearGradient(0, s['y'], w, s['y'])
            grad.setColorAt(0, QColor(0, 255, 255, 0))
            grad.setColorAt(0.3, QColor(0, 255, 255, s['alpha']))
            grad.setColorAt(0.7, QColor(255, 0, 128, s['alpha']))
            grad.setColorAt(1, QColor(255, 0, 128, 0))
            painter.setPen(QPen(QBrush(grad), s['thick']))
            painter.drawLine(QPointF(0, s['y']), QPointF(w, s['y']))

    def _draw_hex(self, painter, cx, cy, r):
        pts = [QPointF(cx + r * math.cos(math.pi / 3 * i - math.pi / 6),
                       cy + r * math.sin(math.pi / 3 * i - math.pi / 6)) for i in range(6)]
        painter.drawPolygon(QPolygonF(pts))


class SpaceParticles:
    """🌌 太空宇宙 - 星空+流星+脉冲行星+卫星轨道"""
    def __init__(self, w, h, count=200):
        self.w, self.h = w, h
        self.stars = []
        for _ in range(count):
            self.stars.append({
                'x': random.uniform(0, w), 'y': random.uniform(0, h),
                'r': random.uniform(0.4, 2.5),
                'speed': random.uniform(0.03, 0.5),
                'phase': random.uniform(0, math.pi * 2),
                'pulse': random.uniform(0.015, 0.08),
                'is_meteor': random.random() < 0.06,
                'color_type': random.choice(['white', 'blue', 'gold', 'cyan'])
            })
        self.t = 0.0
        self.planet_phase = 0.0
        # 轨道卫星
        self.satellites = []
        for i in range(3):
            self.satellites.append({
                'angle': random.uniform(0, math.pi * 2),
                'speed': random.uniform(0.005, 0.012),
                'radius_ratio': 0.85 + i * 0.06,
                'r': random.uniform(2, 4),
            })

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.015
        self.planet_phase += 0.005
        for star in self.stars:
            speed = star['speed'] * 15 if star['is_meteor'] else star['speed']
            star['x'] -= speed
            if star['x'] < -120:
                star['x'] = w + random.uniform(30, 150)
                star['y'] = random.uniform(0, h)
        for sat in self.satellites:
            sat['angle'] += sat['speed']

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        # 星云
        nebula1 = QRadialGradient(w * 0.25 + 60 * math.sin(self.t * 0.15),
                                  h * 0.25, w * 0.55)
        nebula1.setColorAt(0, QColor(99, 102, 241, 30))
        nebula1.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(nebula1))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        nebula2 = QRadialGradient(w * 0.75 + 40 * math.cos(self.t * 0.2),
                                  h * 0.6, w * 0.45)
        nebula2.setColorAt(0, QColor(168, 85, 247, 25))
        nebula2.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(nebula2))
        painter.drawRect(rect)

        # 大行星
        planet_radius = w * 0.95
        planet_cx = w / 2
        planet_cy = -planet_radius * 0.68
        planet_rect = QRectF(planet_cx - planet_radius, planet_cy - planet_radius,
                             planet_radius * 2, planet_radius * 2)
        planet_grad = QRadialGradient(planet_rect.center(), planet_radius)
        planet_grad.setFocalPoint(planet_cx, planet_cy + planet_radius * 0.88)
        planet_grad.setColorAt(0.68, QColor(8, 18, 45, 255))
        planet_grad.setColorAt(0.94, QColor(80, 60, 180, 180))
        planet_grad.setColorAt(0.97, QColor(120, 180, 255, 220))
        planet_grad.setColorAt(1.0, QColor(180, 220, 255, 255))
        painter.setBrush(QBrush(planet_grad))
        painter.drawEllipse(planet_rect)

        halo_a = int(70 + 35 * math.sin(self.t))
        painter.setPen(QPen(QColor(180, 220, 255, halo_a), 3.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(planet_rect, 180 * 16, -180 * 16)

        # 卫星轨道
        for sat in self.satellites:
            orbit_r = planet_radius * sat['radius_ratio']
            sx = planet_cx + orbit_r * math.cos(sat['angle'])
            sy = planet_cy + orbit_r * math.sin(sat['angle']) * 0.4
            if 0 < sy < h:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(255, 230, 180, 220))
                painter.drawEllipse(QPointF(sx, sy), sat['r'], sat['r'])
                # 拖尾
                for k in range(5):
                    ka = math.cos(sat['angle'] - k * 0.05) * orbit_r + planet_cx
                    kb = math.sin(sat['angle'] - k * 0.05) * orbit_r * 0.4 + planet_cy
                    painter.setBrush(QColor(255, 230, 180, 100 - k * 18))
                    painter.drawEllipse(QPointF(ka, kb), sat['r'] * (1 - k * 0.15),
                                        sat['r'] * (1 - k * 0.15))

        # 星星
        painter.setPen(Qt.NoPen)
        color_map = {
            'white': QColor(255, 255, 255),
            'blue': QColor(180, 200, 255),
            'gold': QColor(255, 220, 180),
            'cyan': QColor(200, 255, 255)
        }
        for star in self.stars:
            a = int(60 + 150 * math.sin(self.t * 10 * star['pulse'] + star['phase']))
            a = max(0, min(255, a))
            c = color_map[star['color_type']]
            if star['is_meteor']:
                painter.setBrush(QColor(c.red(), c.green(), c.blue(), a))
                painter.drawEllipse(QPointF(star['x'], star['y']),
                                    star['r'] * 3, star['r'] * 0.9)
                painter.setBrush(QColor(0, 212, 255, a // 4))
                painter.drawEllipse(QPointF(star['x'] + 12, star['y']),
                                    star['r'] * 10, star['r'] * 0.6)
            else:
                painter.setBrush(QColor(c.red(), c.green(), c.blue(), a))
                painter.drawEllipse(QPointF(star['x'], star['y']), star['r'], star['r'])


class WheatParticles:
    """🌾 金色麦田 - 摇摆麦穗+夕阳+蜻蜓+鸟群"""
    def __init__(self, w, h, count=80):
        self.w, self.h = w, h
        self.t = 0.0
        self.wheat = []
        for _ in range(count):
            self.wheat.append({
                'x': random.uniform(-50, w + 50),
                'base_y': random.uniform(h * 0.5, h),
                'height': random.uniform(40, 90),
                'phase': random.uniform(0, math.pi * 2),
                'sway_speed': random.uniform(0.02, 0.05),
                'sway_amp': random.uniform(5, 15),
                'depth': random.uniform(0.3, 1.0),
            })
        self.dragonflies = []
        for _ in range(4):
            self.dragonflies.append({
                'x': random.uniform(0, w), 'y': random.uniform(50, h * 0.5),
                'vx': random.uniform(-0.5, 0.5), 'vy': random.uniform(-0.3, 0.3),
                'wing_phase': random.uniform(0, math.pi * 2),
            })
        self.petals = []
        for _ in range(30):
            self.petals.append({
                'x': random.uniform(0, w), 'y': random.uniform(0, h),
                'vx': random.uniform(-0.3, 0.3), 'vy': random.uniform(0.1, 0.4),
                'r': random.uniform(1, 3),
                'phase': random.uniform(0, math.pi * 2),
            })
        # 鸟群（远处剪影 V 字）
        self.birds = [{'x': random.uniform(0, w), 'y': random.uniform(40, 100),
                       'vx': random.uniform(-0.6, -0.3),
                       'phase': random.uniform(0, math.pi * 2)} for _ in range(7)]

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.02
        for d in self.dragonflies:
            d['x'] += d['vx']; d['y'] += d['vy']
            d['wing_phase'] += 0.5
            if d['x'] < 0 or d['x'] > w: d['vx'] *= -1
            if d['y'] < 30 or d['y'] > h * 0.5: d['vy'] *= -1
        for p in self.petals:
            p['x'] += p['vx'] + math.sin(self.t + p['phase']) * 0.3
            p['y'] += p['vy']
            if p['y'] > h: p['y'] = -10; p['x'] = random.uniform(0, w)
        for b in self.birds:
            b['x'] += b['vx']
            if b['x'] < -30: b['x'] = w + 30; b['y'] = random.uniform(40, 100)

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        sky = QLinearGradient(0, 0, 0, h)
        sky.setColorAt(0, QColor(40, 20, 50, 200))
        sky.setColorAt(0.4, QColor(180, 100, 80, 120))
        sky.setColorAt(0.7, QColor(255, 150, 80, 180))
        sky.setColorAt(1.0, QColor(80, 40, 20, 200))
        painter.setBrush(QBrush(sky))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        sun_x = w * 0.7
        sun_y = h * 0.35
        sun_grad = QRadialGradient(sun_x, sun_y, 80)
        sun_grad.setColorAt(0, QColor(255, 240, 180, 230))
        sun_grad.setColorAt(0.5, QColor(255, 180, 80, 180))
        sun_grad.setColorAt(1.0, QColor(255, 100, 50, 0))
        painter.setBrush(QBrush(sun_grad))
        painter.drawEllipse(QPointF(sun_x, sun_y), 60, 60)
        for ring in range(3):
            r = 80 + ring * 30 + 5 * math.sin(self.t + ring)
            painter.setPen(QPen(QColor(255, 200, 100, 30 - ring * 8), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(sun_x, sun_y), r, r)

        # 鸟群（V字）
        for b in self.birds:
            wing = math.sin(self.t * 5 + b['phase']) * 3
            painter.setPen(QPen(QColor(40, 25, 30, 180), 1.6))
            painter.drawLine(QPointF(b['x'], b['y']),
                             QPointF(b['x'] - 6, b['y'] - 3 + wing))
            painter.drawLine(QPointF(b['x'], b['y']),
                             QPointF(b['x'] + 6, b['y'] - 3 + wing))

        painter.setPen(Qt.NoPen)
        for p in self.petals:
            a = int(120 + 80 * math.sin(self.t + p['phase']))
            painter.setBrush(QColor(255, 220, 150, a))
            painter.drawEllipse(QPointF(p['x'], p['y']), p['r'], p['r'])

        sorted_wheat = sorted(self.wheat, key=lambda x: x['depth'])
        for wh in sorted_wheat:
            sway = math.sin(self.t * wh['sway_speed'] * 30 + wh['phase']) * wh['sway_amp']
            x = wh['x']
            base_y = wh['base_y']
            top_x = x + sway
            top_y = base_y - wh['height'] * wh['depth']
            green = int(80 + 80 * wh['depth'])
            painter.setPen(QPen(QColor(110, green, 50, int(180 * wh['depth'])), 1.5))
            painter.drawLine(QPointF(x, base_y), QPointF(top_x, top_y))
            head_color = QColor(255, int(180 + 30 * wh['depth']),
                                int(80 + 40 * wh['depth']),
                                int(220 * wh['depth']))
            painter.setPen(Qt.NoPen)
            painter.setBrush(head_color)
            for k in range(5):
                ky = top_y + k * 4
                kx_offset = (k % 2 - 0.5) * 4
                painter.drawEllipse(QPointF(top_x + kx_offset, ky),
                                    2 * wh['depth'], 3 * wh['depth'])
            painter.setPen(QPen(QColor(255, 220, 100, int(180 * wh['depth'])), 1))
            for k in range(3):
                ang = -math.pi / 2 + (k - 1) * 0.3
                ex = top_x + 12 * math.cos(ang) * wh['depth']
                ey = top_y + 12 * math.sin(ang) * wh['depth']
                painter.drawLine(QPointF(top_x, top_y), QPointF(ex, ey))

        for d in self.dragonflies:
            wing_alpha = int(150 + 100 * math.sin(d['wing_phase']))
            painter.setBrush(QColor(180, 220, 255, wing_alpha))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(d['x'] - 6, d['y'] - 3), 7, 3)
            painter.drawEllipse(QPointF(d['x'] + 6, d['y'] - 3), 7, 3)
            painter.drawEllipse(QPointF(d['x'] - 5, d['y'] + 3), 6, 2.5)
            painter.drawEllipse(QPointF(d['x'] + 5, d['y'] + 3), 6, 2.5)
            painter.setBrush(QColor(80, 120, 180, 220))
            painter.drawEllipse(QPointF(d['x'], d['y']), 1.5, 8)


class CandyParticles:
    """🍭 梦幻糖果 - 飘浮糖果+心形+泡泡+彩虹波浪"""
    def __init__(self, w, h, count=110):
        self.w, self.h = w, h
        self.t = 0.0
        self.candies = []
        candy_types = ['bubble', 'heart', 'star', 'lollipop', 'circle']
        candy_colors = [
            QColor(255, 150, 200), QColor(180, 200, 255),
            QColor(255, 230, 130), QColor(200, 150, 255),
            QColor(150, 255, 200), QColor(255, 180, 150),
        ]
        for _ in range(count):
            self.candies.append({
                'x': random.uniform(0, w), 'y': random.uniform(0, h),
                'vx': random.uniform(-0.4, 0.4), 'vy': random.uniform(-0.6, -0.2),
                'r': random.uniform(4, 12),
                'rotation': 0,
                'rot_speed': random.uniform(-0.05, 0.05),
                'type': random.choice(candy_types),
                'color': random.choice(candy_colors),
                'phase': random.uniform(0, math.pi * 2),
                'wobble': random.uniform(0.02, 0.05),
            })

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.02
        for c in self.candies:
            c['x'] += c['vx'] + math.sin(self.t + c['phase']) * 0.5
            c['y'] += c['vy']
            c['rotation'] += c['rot_speed']
            if c['y'] < -20:
                c['y'] = h + 20
                c['x'] = random.uniform(0, w)

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        bg = QLinearGradient(0, 0, w, h)
        bg.setColorAt(0, QColor(80, 40, 100, 100))
        bg.setColorAt(0.5, QColor(120, 60, 140, 80))
        bg.setColorAt(1, QColor(60, 30, 80, 100))
        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        # 彩虹波浪带
        for layer in range(3):
            colors = [QColor(255, 150, 200, 35), QColor(180, 200, 255, 32),
                      QColor(255, 230, 130, 28)]
            path = QPainterPath()
            base_y = h * (0.4 + layer * 0.2)
            path.moveTo(0, base_y)
            for x_step in range(0, int(w) + 30, 20):
                wave_y = base_y + 22 * math.sin(self.t * 1.5 + x_step * 0.02 + layer)
                path.lineTo(x_step, wave_y)
            path.lineTo(w, h); path.lineTo(0, h); path.closeSubpath()
            painter.setBrush(QBrush(colors[layer]))
            painter.drawPath(path)

        for i in range(3):
            cx = w * (0.2 + 0.3 * i)
            cy = h * (0.3 + 0.2 * math.sin(self.t * 0.3 + i))
            grad = QRadialGradient(cx, cy, 200)
            colors = [QColor(255, 150, 200, 40), QColor(180, 200, 255, 35),
                      QColor(255, 230, 130, 30)]
            grad.setColorAt(0, colors[i])
            grad.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(grad))
            painter.drawRect(rect)

        for c in self.candies:
            a = int(180 + 60 * math.sin(self.t * 5 * c['wobble'] + c['phase']))
            color = QColor(c['color'].red(), c['color'].green(), c['color'].blue(), a)
            painter.save()
            painter.translate(c['x'], c['y'])
            painter.rotate(c['rotation'] * 57.3)

            if c['type'] == 'bubble':
                painter.setPen(QPen(color, 1.5))
                painter.setBrush(QColor(color.red(), color.green(), color.blue(), 60))
                painter.drawEllipse(QPointF(0, 0), c['r'], c['r'])
                painter.setBrush(QColor(255, 255, 255, 150))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPointF(-c['r'] * 0.3, -c['r'] * 0.3),
                                    c['r'] * 0.3, c['r'] * 0.3)
            elif c['type'] == 'heart':
                painter.setPen(Qt.NoPen)
                painter.setBrush(color)
                path = QPainterPath()
                r = c['r']
                path.moveTo(0, r * 0.3)
                path.cubicTo(-r, -r * 0.5, -r * 0.5, -r * 1.2, 0, -r * 0.3)
                path.cubicTo(r * 0.5, -r * 1.2, r, -r * 0.5, 0, r * 0.3)
                painter.drawPath(path)
            elif c['type'] == 'star':
                painter.setPen(Qt.NoPen)
                painter.setBrush(color)
                pts = []
                for i in range(10):
                    ang = math.pi / 5 * i - math.pi / 2
                    rr = c['r'] if i % 2 == 0 else c['r'] * 0.4
                    pts.append(QPointF(rr * math.cos(ang), rr * math.sin(ang)))
                painter.drawPolygon(QPolygonF(pts))
            elif c['type'] == 'lollipop':
                painter.setPen(QPen(QColor(255, 255, 255, 180), 1.5))
                painter.drawLine(QPointF(0, c['r']), QPointF(0, c['r'] * 2.5))
                painter.setPen(Qt.NoPen)
                painter.setBrush(color)
                painter.drawEllipse(QPointF(0, 0), c['r'], c['r'])
                painter.setPen(QPen(QColor(255, 255, 255, 200), 1))
                painter.setBrush(Qt.NoBrush)
                for ring in range(3):
                    rr = c['r'] * (0.3 + ring * 0.25)
                    painter.drawArc(QRectF(-rr, -rr, rr * 2, rr * 2),
                                    int(c['rotation'] * 200) % (360 * 16), 270 * 16)
            else:
                painter.setPen(Qt.NoPen)
                painter.setBrush(color)
                painter.drawEllipse(QPointF(0, 0), c['r'], c['r'])
                painter.setBrush(QColor(255, 255, 255, 120))
                painter.drawEllipse(QPointF(-c['r'] * 0.3, -c['r'] * 0.3),
                                    c['r'] * 0.25, c['r'] * 0.25)
            painter.restore()


class OceanParticles:
    """🌊 深海秘境 - 上升气泡+水母+鱼+珊瑚剪影"""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.t = 0.0
        self.bubbles = []
        for _ in range(80):
            self.bubbles.append({
                'x': random.uniform(0, w), 'y': random.uniform(0, h),
                'vy': random.uniform(0.3, 1.2),
                'r': random.uniform(2, 8),
                'wobble': random.uniform(0.02, 0.06),
                'phase': random.uniform(0, math.pi * 2),
                'alpha': random.randint(80, 180),
            })
        self.jellyfish = []
        for _ in range(3):
            self.jellyfish.append({
                'x': random.uniform(50, w - 50), 'y': random.uniform(50, h - 100),
                'vx': random.uniform(-0.2, 0.2), 'vy': random.uniform(-0.15, 0.05),
                'r': random.uniform(20, 35),
                'phase': random.uniform(0, math.pi * 2),
                'pulse': random.uniform(0.03, 0.06),
                'color': random.choice([QColor(180, 130, 220), QColor(255, 180, 200),
                                         QColor(150, 220, 255)])
            })
        self.fish = []
        for _ in range(6):
            self.fish.append({
                'x': random.uniform(0, w), 'y': random.uniform(h * 0.3, h * 0.85),
                'vx': random.choice([-1, 1]) * random.uniform(0.6, 1.5),
                'size': random.uniform(8, 16),
                'phase': random.uniform(0, math.pi * 2),
                'color': random.choice([QColor(255, 180, 100), QColor(100, 200, 255),
                                         QColor(180, 255, 200), QColor(255, 200, 220)])
            })
        # 珊瑚（底部静态）
        self.corals = []
        for _ in range(8):
            self.corals.append({
                'x': random.uniform(0, w),
                'h': random.uniform(40, 80),
                'color': random.choice([QColor(255, 100, 100), QColor(255, 180, 80),
                                         QColor(180, 100, 200)]),
            })

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.02
        for b in self.bubbles:
            b['y'] -= b['vy']
            b['x'] += math.sin(self.t * 5 * b['wobble'] + b['phase']) * 0.6
            if b['y'] < -10:
                b['y'] = h + 10; b['x'] = random.uniform(0, w)
        for j in self.jellyfish:
            j['x'] += j['vx']; j['y'] += j['vy']
            if j['x'] < 30 or j['x'] > w - 30: j['vx'] *= -1
            if j['y'] < 30 or j['y'] > h - 80: j['vy'] *= -1
        for f in self.fish:
            f['x'] += f['vx']
            f['y'] += math.sin(self.t * 3 + f['phase']) * 0.3
            if f['vx'] > 0 and f['x'] > w + 50:
                f['x'] = -50
            elif f['vx'] < 0 and f['x'] < -50:
                f['x'] = w + 50

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        sea = QLinearGradient(0, 0, 0, h)
        sea.setColorAt(0, QColor(20, 80, 130, 150))
        sea.setColorAt(0.5, QColor(10, 50, 100, 180))
        sea.setColorAt(1.0, QColor(5, 20, 50, 220))
        painter.setBrush(QBrush(sea))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        for i in range(4):
            x = w * (0.15 + i * 0.25) + 30 * math.sin(self.t * 0.5 + i)
            ray_grad = QLinearGradient(x, 0, x + 60, h * 0.7)
            ray_grad.setColorAt(0, QColor(255, 250, 200, 50))
            ray_grad.setColorAt(1, QColor(255, 250, 200, 0))
            painter.setBrush(QBrush(ray_grad))
            pts = [QPointF(x - 30, 0), QPointF(x + 30, 0),
                   QPointF(x + 80, h * 0.7), QPointF(x - 20, h * 0.7)]
            painter.drawPolygon(QPolygonF(pts))

        # 珊瑚剪影
        for coral in self.corals:
            cx = coral['x']; ch = coral['h']
            painter.setPen(QPen(coral['color'].darker(140), 2))
            painter.setBrush(QColor(coral['color'].red(), coral['color'].green(),
                                     coral['color'].blue(), 120))
            for branch in range(3):
                bx = cx + (branch - 1) * 6
                by = h
                tx = bx + math.sin(self.t * 0.5 + branch) * 3
                ty = by - ch * (0.7 + branch * 0.15)
                painter.drawLine(QPointF(bx, by), QPointF(tx, ty))
                painter.drawEllipse(QPointF(tx, ty), 4, 4)

        for f in self.fish:
            painter.save()
            painter.translate(f['x'], f['y'])
            if f['vx'] < 0:
                painter.scale(-1, 1)
            painter.setPen(Qt.NoPen)
            painter.setBrush(f['color'])
            painter.drawEllipse(QPointF(0, 0), f['size'], f['size'] * 0.5)
            tail_phase = math.sin(self.t * 8 + f['phase']) * 0.5
            tail = [QPointF(-f['size'], 0),
                    QPointF(-f['size'] * 1.8, -f['size'] * 0.5 + tail_phase * 3),
                    QPointF(-f['size'] * 1.5, 0),
                    QPointF(-f['size'] * 1.8, f['size'] * 0.5 + tail_phase * 3)]
            painter.drawPolygon(QPolygonF(tail))
            painter.setBrush(QColor(0, 0, 0, 180))
            painter.drawEllipse(QPointF(f['size'] * 0.5, -f['size'] * 0.15), 1.5, 1.5)
            painter.restore()

        for j in self.jellyfish:
            pulse = 1.0 + 0.15 * math.sin(self.t * 5 * j['pulse'] + j['phase'])
            r = j['r'] * pulse
            cap_grad = QRadialGradient(j['x'], j['y'], r)
            c = j['color']
            cap_grad.setColorAt(0, QColor(c.red(), c.green(), c.blue(), 180))
            cap_grad.setColorAt(1, QColor(c.red(), c.green(), c.blue(), 80))
            painter.setBrush(QBrush(cap_grad))
            painter.setPen(Qt.NoPen)
            painter.drawChord(QRectF(j['x'] - r, j['y'] - r, r * 2, r * 2),
                              0, 180 * 16)
            painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(), 150), 1.5))
            for k in range(7):
                tx = j['x'] - r + k * (r * 2 / 6)
                path = QPainterPath()
                path.moveTo(tx, j['y'])
                for step in range(8):
                    sy = j['y'] + step * 6
                    sx = tx + math.sin(self.t * 3 + k + step * 0.5) * 4
                    path.lineTo(sx, sy)
                painter.drawPath(path)

        painter.setPen(Qt.NoPen)
        for b in self.bubbles:
            painter.setPen(QPen(QColor(200, 230, 255, b['alpha']), 1.0))
            painter.setBrush(QColor(200, 230, 255, b['alpha'] // 3))
            painter.drawEllipse(QPointF(b['x'], b['y']), b['r'], b['r'])
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 255, 255, b['alpha']))
            painter.drawEllipse(QPointF(b['x'] - b['r'] * 0.3, b['y'] - b['r'] * 0.3),
                                b['r'] * 0.25, b['r'] * 0.25)


class SakuraParticles:
    """🌸 樱花飞舞 - 飘落花瓣+月夜+灯笼+流萤"""
    def __init__(self, w, h, count=90):
        self.w, self.h = w, h
        self.t = 0.0
        self.petals = []
        for _ in range(count):
            self.petals.append({
                'x': random.uniform(-50, w + 50), 'y': random.uniform(-50, h),
                'vx': random.uniform(-0.5, 0.5), 'vy': random.uniform(0.4, 1.2),
                'r': random.uniform(4, 9),
                'rotation': random.uniform(0, math.pi * 2),
                'rot_speed': random.uniform(-0.05, 0.05),
                'phase': random.uniform(0, math.pi * 2),
                'sway': random.uniform(0.02, 0.05),
                'depth': random.uniform(0.4, 1.0),
                'color_idx': random.choice([0, 0, 0, 1, 2]),
            })
        self.moon_x = w * 0.78; self.moon_y = h * 0.22
        self.trees = []
        for i in range(5):
            self.trees.append({
                'x': w * (0.1 + i * 0.22),
                'y': h * (0.85 + random.uniform(0, 0.1)),
                'r': random.uniform(60, 110),
            })
        self.fireflies = [{'x': random.uniform(0, w), 'y': random.uniform(0, h),
                           'vx': random.uniform(-0.3, 0.3), 'vy': random.uniform(-0.3, 0.3),
                           'phase': random.uniform(0, math.pi * 2)} for _ in range(15)]

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.02
        self.moon_x = w * 0.78; self.moon_y = h * 0.22
        for p in self.petals:
            p['x'] += p['vx'] + math.sin(self.t * 5 * p['sway'] + p['phase']) * 0.8
            p['y'] += p['vy']
            p['rotation'] += p['rot_speed']
            if p['y'] > h + 20:
                p['y'] = -20; p['x'] = random.uniform(-50, w + 50)
        for f in self.fireflies:
            f['x'] += f['vx']; f['y'] += f['vy']
            if f['x'] < 0 or f['x'] > w: f['vx'] *= -1
            if f['y'] < 0 or f['y'] > h: f['vy'] *= -1

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        sky = QLinearGradient(0, 0, 0, h)
        sky.setColorAt(0, QColor(30, 15, 50, 220))
        sky.setColorAt(0.5, QColor(60, 30, 70, 180))
        sky.setColorAt(1.0, QColor(40, 20, 50, 220))
        painter.setBrush(QBrush(sky))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        moon_grad = QRadialGradient(self.moon_x, self.moon_y, 50)
        moon_grad.setColorAt(0, QColor(255, 250, 220, 240))
        moon_grad.setColorAt(0.7, QColor(255, 240, 200, 180))
        moon_grad.setColorAt(1.0, QColor(255, 230, 180, 0))
        painter.setBrush(QBrush(moon_grad))
        painter.drawEllipse(QPointF(self.moon_x, self.moon_y), 38, 38)
        for ring in range(3):
            r = 45 + ring * 25 + 3 * math.sin(self.t + ring)
            painter.setPen(QPen(QColor(255, 250, 220, 25 - ring * 5), 1.5))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(self.moon_x, self.moon_y), r, r)

        for tree in self.trees:
            tree_grad = QRadialGradient(tree['x'], tree['y'], tree['r'])
            tree_grad.setColorAt(0, QColor(255, 180, 200, 120))
            tree_grad.setColorAt(1, QColor(150, 80, 130, 0))
            painter.setBrush(QBrush(tree_grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(tree['x'], tree['y']),
                                tree['r'], tree['r'] * 0.7)

        # 流萤
        for f in self.fireflies:
            a = int(120 + 100 * math.sin(self.t * 5 + f['phase']))
            grad = QRadialGradient(f['x'], f['y'], 12)
            grad.setColorAt(0, QColor(255, 230, 180, a))
            grad.setColorAt(1, QColor(255, 230, 180, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(f['x'], f['y']), 12, 12)
            painter.setBrush(QColor(255, 255, 220, a))
            painter.drawEllipse(QPointF(f['x'], f['y']), 2, 2)

        for lx, ly in [(60, h - 50), (w - 60, h - 50)]:
            grad = QRadialGradient(lx, ly, 40)
            grad.setColorAt(0, QColor(255, 200, 150, 200 + int(30 * math.sin(self.t * 2))))
            grad.setColorAt(1, QColor(255, 100, 100, 0))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(lx, ly), 35, 35)
            painter.setBrush(QColor(220, 80, 80, 230))
            painter.setPen(QPen(QColor(180, 50, 50, 230), 1.5))
            painter.drawEllipse(QPointF(lx, ly), 14, 18)
            painter.setBrush(QColor(60, 30, 30, 230))
            painter.drawRect(QRectF(lx - 8, ly - 22, 16, 4))
            painter.drawRect(QRectF(lx - 8, ly + 18, 16, 4))
            painter.setPen(QPen(QColor(255, 200, 100, 200), 2))
            painter.drawLine(QPointF(lx, ly + 22), QPointF(lx, ly + 32))

        sorted_petals = sorted(self.petals, key=lambda x: x['depth'])
        colors = [QColor(255, 180, 200), QColor(255, 220, 230), QColor(220, 130, 180)]
        for p in sorted_petals:
            painter.save()
            painter.translate(p['x'], p['y'])
            painter.rotate(p['rotation'] * 57.3)
            c = colors[p['color_idx']]
            a = int(220 * p['depth'])
            painter.setPen(QPen(QColor(c.red() - 30, c.green() - 30, c.blue() - 30, a), 1))
            painter.setBrush(QColor(c.red(), c.green(), c.blue(), a))
            r = p['r'] * p['depth']
            path = QPainterPath()
            path.moveTo(0, 0)
            path.cubicTo(-r * 0.5, -r * 0.5, -r * 0.8, -r * 1.2, 0, -r)
            path.cubicTo(r * 0.8, -r * 1.2, r * 0.5, -r * 0.5, 0, 0)
            painter.drawPath(path)
            painter.restore()


class LavaParticles:
    """🔥 熔岩地狱 - 火焰+岩浆裂缝+灰烬+火球"""
    def __init__(self, w, h, count=140):
        self.w, self.h = w, h
        self.t = 0.0
        self.flames = []
        for _ in range(count):
            self.flames.append({
                'x': random.uniform(0, w),
                'y': random.uniform(h * 0.3, h + 50),
                'vy': random.uniform(-2.5, -0.8),
                'vx': random.uniform(-0.3, 0.3),
                'r': random.uniform(3, 10),
                'life': random.uniform(0.5, 1.0),
                'max_life': random.uniform(1.5, 3.0),
                'wobble': random.uniform(0.05, 0.12),
                'phase': random.uniform(0, math.pi * 2),
            })
        self.ashes = []
        for _ in range(50):
            self.ashes.append({
                'x': random.uniform(0, w), 'y': random.uniform(0, h),
                'vx': random.uniform(-0.4, 0.4), 'vy': random.uniform(-0.2, 0.3),
                'r': random.uniform(0.8, 2.0),
                'phase': random.uniform(0, math.pi * 2),
            })
        self.cracks = []
        for _ in range(8):
            sx = random.uniform(0, w)
            sy = random.uniform(h * 0.6, h)
            pts = [(sx, sy)]
            for _ in range(random.randint(3, 6)):
                sx += random.uniform(-30, 30)
                sy += random.uniform(-15, 5)
                pts.append((sx, sy))
            self.cracks.append({'pts': pts, 'phase': random.uniform(0, math.pi * 2)})
        # 飞行火球
        self.fireballs = []
        for _ in range(2):
            self.fireballs.append({
                'x': random.uniform(0, w), 'y': random.uniform(50, h * 0.4),
                'vx': random.uniform(-1.5, -0.5), 'vy': random.uniform(0.3, 0.8),
                'r': random.uniform(10, 18),
            })

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.04
        for f in self.flames:
            f['x'] += f['vx'] + math.sin(self.t * 5 * f['wobble'] + f['phase']) * 0.5
            f['y'] += f['vy']
            f['life'] -= 0.015
            if f['life'] <= 0 or f['y'] < -20:
                f['x'] = random.uniform(0, w)
                f['y'] = h + random.uniform(0, 30)
                f['life'] = f['max_life']
                f['vy'] = random.uniform(-2.5, -0.8)
        for a in self.ashes:
            a['x'] += a['vx']; a['y'] += a['vy']
            if a['x'] < 0 or a['x'] > w: a['vx'] *= -1
            if a['y'] < 0: a['y'] = h
            if a['y'] > h: a['y'] = 0
        for fb in self.fireballs:
            fb['x'] += fb['vx']; fb['y'] += fb['vy']
            if fb['x'] < -50 or fb['y'] > h:
                fb['x'] = w + 50; fb['y'] = random.uniform(50, h * 0.4)

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        bg = QLinearGradient(0, 0, 0, h)
        bg.setColorAt(0, QColor(20, 5, 5, 200))
        bg.setColorAt(0.6, QColor(60, 15, 5, 150))
        bg.setColorAt(1.0, QColor(180, 60, 20, 200))
        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        lava_grad = QRadialGradient(w / 2, h, w * 0.7)
        lava_grad.setColorAt(0, QColor(255, 100, 30, 180))
        lava_grad.setColorAt(0.5, QColor(255, 60, 20, 80))
        lava_grad.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(lava_grad))
        painter.drawRect(rect)

        for crack in self.cracks:
            glow = int(150 + 100 * math.sin(self.t * 2 + crack['phase']))
            glow = max(50, min(255, glow))
            for i in range(len(crack['pts']) - 1):
                p1, p2 = crack['pts'][i], crack['pts'][i + 1]
                painter.setPen(QPen(QColor(255, 100, 30, glow // 2), 6))
                painter.drawLine(QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1]))
                painter.setPen(QPen(QColor(255, 230, 150, glow), 2))
                painter.drawLine(QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1]))

        # 火球
        for fb in self.fireballs:
            grad = QRadialGradient(fb['x'], fb['y'], fb['r'] * 2)
            grad.setColorAt(0, QColor(255, 240, 150, 230))
            grad.setColorAt(0.4, QColor(255, 100, 30, 180))
            grad.setColorAt(1, QColor(255, 50, 10, 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(fb['x'], fb['y']), fb['r'] * 2, fb['r'] * 2)
            # 拖尾
            for k in range(8):
                tx = fb['x'] - fb['vx'] * k * 3
                ty = fb['y'] - fb['vy'] * k * 3
                a = 200 - k * 25
                if a <= 0: break
                painter.setBrush(QColor(255, 100, 30, a))
                painter.drawEllipse(QPointF(tx, ty), fb['r'] * (1 - k * 0.1),
                                    fb['r'] * (1 - k * 0.1))

        painter.setPen(Qt.NoPen)
        for f in self.flames:
            life_ratio = f['life'] / f['max_life']
            alpha = int(255 * life_ratio)
            outer_r = f['r'] * (1.5 + (1 - life_ratio) * 0.5)
            grad = QRadialGradient(f['x'], f['y'], outer_r)
            grad.setColorAt(0, QColor(255, 200, 80, alpha))
            grad.setColorAt(0.5, QColor(255, 100, 30, alpha // 2))
            grad.setColorAt(1, QColor(180, 30, 10, 0))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(f['x'], f['y']), outer_r, outer_r * 1.5)
            painter.setBrush(QColor(255, 240, 150, alpha))
            painter.drawEllipse(QPointF(f['x'], f['y']), f['r'] * 0.4, f['r'] * 0.6)

        for a in self.ashes:
            alpha = int(80 + 60 * math.sin(self.t + a['phase']))
            painter.setBrush(QColor(180, 100, 60, alpha))
            painter.drawEllipse(QPointF(a['x'], a['y']), a['r'], a['r'])


class ArcticParticles:
    """❄️ 极地冰雪 - 雪花+极光+冰晶+冷霜"""
    def __init__(self, w, h, count=120):
        self.w, self.h = w, h
        self.t = 0.0
        self.snow = []
        for _ in range(count):
            self.snow.append({
                'x': random.uniform(-20, w + 20), 'y': random.uniform(-20, h),
                'vx': random.uniform(-0.4, 0.4), 'vy': random.uniform(0.3, 1.2),
                'r': random.uniform(1.5, 4.0),
                'rotation': random.uniform(0, math.pi * 2),
                'rot_speed': random.uniform(-0.04, 0.04),
                'sway': random.uniform(0.02, 0.05),
                'phase': random.uniform(0, math.pi * 2),
                'is_crystal': random.random() < 0.3,
                'depth': random.uniform(0.3, 1.0),
            })
        self.aurora_phase = 0.0
        self.ice_crystals = []
        for _ in range(15):
            self.ice_crystals.append({
                'x': random.uniform(0, w), 'y': random.uniform(h * 0.7, h),
                'r': random.uniform(15, 30),
                'phase': random.uniform(0, math.pi * 2),
            })

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.02
        self.aurora_phase += 0.015
        for s in self.snow:
            s['x'] += s['vx'] + math.sin(self.t * 5 * s['sway'] + s['phase']) * 0.5
            s['y'] += s['vy'] * s['depth']
            s['rotation'] += s['rot_speed']
            if s['y'] > h + 10:
                s['y'] = -10; s['x'] = random.uniform(-20, w + 20)

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        sky = QLinearGradient(0, 0, 0, h)
        sky.setColorAt(0, QColor(5, 15, 40, 220))
        sky.setColorAt(0.5, QColor(15, 30, 60, 180))
        sky.setColorAt(1.0, QColor(30, 50, 80, 200))
        painter.setBrush(QBrush(sky))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        for layer in range(4):
            colors = [QColor(150, 220, 255, 50), QColor(180, 255, 220, 60),
                      QColor(220, 200, 255, 50), QColor(120, 255, 180, 40)]
            path = QPainterPath()
            path.moveTo(0, h * 0.4)
            for x_step in range(0, int(w) + 30, 20):
                wave_y = h * 0.25 + 40 * math.sin(
                    self.aurora_phase * (1 + layer * 0.3) + x_step * 0.015 + layer * 1.5
                ) + layer * 25
                path.lineTo(x_step, wave_y)
            path.lineTo(w, 0); path.lineTo(0, 0); path.closeSubpath()
            painter.setBrush(QBrush(colors[layer]))
            painter.drawPath(path)

        for ic in self.ice_crystals:
            grad = QRadialGradient(ic['x'], ic['y'], ic['r'])
            a = int(80 + 40 * math.sin(self.t + ic['phase']))
            grad.setColorAt(0, QColor(180, 230, 255, a))
            grad.setColorAt(1, QColor(100, 180, 220, 0))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(ic['x'], ic['y']), ic['r'], ic['r'])

        sorted_snow = sorted(self.snow, key=lambda s: s['depth'])
        for s in sorted_snow:
            painter.save()
            painter.translate(s['x'], s['y'])
            painter.rotate(s['rotation'] * 57.3)
            alpha = int(220 * s['depth'])
            r = s['r'] * s['depth']
            if s['is_crystal']:
                painter.setPen(QPen(QColor(220, 240, 255, alpha), 1.0))
                for i in range(6):
                    ang = math.pi / 3 * i
                    ex = r * 2 * math.cos(ang); ey = r * 2 * math.sin(ang)
                    painter.drawLine(QPointF(0, 0), QPointF(ex, ey))
                    bx = r * 1.2 * math.cos(ang); by = r * 1.2 * math.sin(ang)
                    for branch in [-0.5, 0.5]:
                        bang = ang + branch
                        sx = bx + r * 0.6 * math.cos(bang)
                        sy = by + r * 0.6 * math.sin(bang)
                        painter.drawLine(QPointF(bx, by), QPointF(sx, sy))
            else:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(255, 255, 255, alpha))
                painter.drawEllipse(QPointF(0, 0), r, r)
            painter.restore()


class RetroParticles:
    """🎮 复古像素 - 8bit方块+CRT扫描+像素雨+霓虹文字"""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.t = 0.0
        self.pixels = []
        cell = 12
        cols = int(w // cell) + 2
        rows = int(h // cell) + 2
        for r in range(rows):
            for c in range(cols):
                if random.random() < 0.04:
                    self.pixels.append({
                        'x': c * cell, 'y': r * cell, 'cell': cell,
                        'color': random.choice([QColor(80, 255, 100), QColor(255, 200, 60),
                                                 QColor(255, 100, 200), QColor(100, 200, 255)]),
                        'phase': random.uniform(0, math.pi * 2),
                        'life': random.uniform(0.5, 2.0),
                    })
        self.rain = []
        for _ in range(40):
            self.rain.append({
                'x': random.uniform(0, w), 'y': random.uniform(0, h),
                'vy': random.uniform(2, 6),
                'len': random.randint(3, 8), 'cell': 8,
            })
        self.scan_y = 0
        self.icons = []
        for _ in range(3):
            self.icons.append({
                'x': random.uniform(50, w - 50), 'y': random.uniform(50, h - 50),
                'vx': random.choice([-1, 1]) * 0.5, 'vy': random.choice([-1, 1]) * 0.5,
                'type': random.choice(['heart', 'invader', 'coin']),
                'size': 4,
            })

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.03
        for p in self.pixels:
            p['life'] -= 0.01
            if p['life'] <= 0:
                p['life'] = random.uniform(1, 3)
                p['phase'] = random.uniform(0, math.pi * 2)
        for r in self.rain:
            r['y'] += r['vy']
            if r['y'] > h + 30:
                r['y'] = -30; r['x'] = random.uniform(0, w)
        for icon in self.icons:
            icon['x'] += icon['vx']; icon['y'] += icon['vy']
            if icon['x'] < 30 or icon['x'] > w - 30: icon['vx'] *= -1
            if icon['y'] < 30 or icon['y'] > h - 30: icon['vy'] *= -1
        self.scan_y += 2
        if self.scan_y > h: self.scan_y = -20

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        bg = QLinearGradient(0, 0, 0, h)
        bg.setColorAt(0, QColor(8, 18, 12, 230))
        bg.setColorAt(1, QColor(5, 15, 8, 230))
        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        painter.setPen(QPen(QColor(80, 255, 100, 12), 1))
        cell = 24
        for x in range(0, int(w), cell):
            painter.drawLine(QPointF(x, 0), QPointF(x, h))
        for y in range(0, int(h), cell):
            painter.drawLine(QPointF(0, y), QPointF(w, y))

        for p in self.pixels:
            alpha = int(200 * (math.sin(self.t * 3 + p['phase']) * 0.5 + 0.5) * (p['life'] / 2))
            alpha = max(0, min(255, alpha))
            c = p['color']
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(c.red(), c.green(), c.blue(), alpha))
            painter.drawRect(QRectF(p['x'], p['y'], p['cell'], p['cell']))

        for r in self.rain:
            for i in range(r['len']):
                a = int(220 * (1 - i / r['len']))
                painter.setBrush(QColor(80, 255, 100, a))
                painter.setPen(Qt.NoPen)
                painter.drawRect(QRectF(r['x'], r['y'] - i * r['cell'],
                                        r['cell'] * 0.6, r['cell'] * 0.6))

        for icon in self.icons:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 200, 60, 200))
            sz = icon['size']
            x, y = icon['x'], icon['y']
            if icon['type'] == 'heart':
                pattern = [
                    [0, 1, 1, 0, 0, 1, 1, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                ]
            elif icon['type'] == 'invader':
                pattern = [
                    [0, 0, 1, 0, 0, 1, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 0, 1, 1, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 0, 0, 1, 0, 1],
                ]
            else:
                pattern = [
                    [0, 1, 1, 1, 1, 1, 1, 0],
                    [1, 1, 0, 1, 1, 0, 1, 1],
                    [1, 0, 1, 1, 1, 1, 0, 1],
                    [1, 1, 0, 1, 1, 0, 1, 1],
                    [1, 1, 0, 1, 1, 0, 1, 1],
                    [0, 1, 1, 1, 1, 1, 1, 0],
                ]
            for ry, row in enumerate(pattern):
                for rx, val in enumerate(row):
                    if val:
                        painter.drawRect(QRectF(x + rx * sz - 16, y + ry * sz - 12, sz, sz))

        painter.setPen(QPen(QColor(80, 255, 100, 15), 1))
        for y in range(0, int(h), 3):
            painter.drawLine(QPointF(0, y), QPointF(w, y))

        scan_grad = QLinearGradient(0, self.scan_y - 20, 0, self.scan_y + 20)
        scan_grad.setColorAt(0, QColor(80, 255, 100, 0))
        scan_grad.setColorAt(0.5, QColor(80, 255, 100, 60))
        scan_grad.setColorAt(1, QColor(80, 255, 100, 0))
        painter.setBrush(QBrush(scan_grad))
        painter.setPen(Qt.NoPen)
        painter.drawRect(QRectF(0, self.scan_y - 20, w, 40))


class ForestParticles:
    """🌿 森林秘境 - 萤火虫+落叶+月光+雾气"""
    def __init__(self, w, h, count=50):
        self.w, self.h = w, h
        self.t = 0.0
        self.fireflies = []
        for _ in range(count):
            self.fireflies.append({
                'x': random.uniform(0, w), 'y': random.uniform(0, h),
                'vx': random.uniform(-0.4, 0.4), 'vy': random.uniform(-0.4, 0.4),
                'r': random.uniform(2, 4),
                'phase': random.uniform(0, math.pi * 2),
                'pulse': random.uniform(0.04, 0.10),
                'target_x': random.uniform(0, w), 'target_y': random.uniform(0, h),
                'change_timer': random.randint(60, 200),
            })
        self.leaves = []
        leaf_colors = [QColor(140, 230, 130), QColor(180, 200, 80),
                       QColor(120, 200, 100), QColor(200, 180, 80)]
        for _ in range(30):
            self.leaves.append({
                'x': random.uniform(-50, w + 50), 'y': random.uniform(-50, h),
                'vx': random.uniform(-0.4, 0.4), 'vy': random.uniform(0.3, 0.9),
                'r': random.uniform(4, 8),
                'rotation': random.uniform(0, math.pi * 2),
                'rot_speed': random.uniform(-0.04, 0.04),
                'sway': random.uniform(0.02, 0.05),
                'phase': random.uniform(0, math.pi * 2),
                'color': random.choice(leaf_colors),
                'depth': random.uniform(0.4, 1.0),
            })
        self.trees = []
        for _ in range(8):
            self.trees.append({
                'x': random.uniform(0, w),
                'h': random.uniform(180, 280), 'w': random.uniform(40, 80),
            })

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.02
        for f in self.fireflies:
            dx = f['target_x'] - f['x']; dy = f['target_y'] - f['y']
            dist = math.sqrt(dx * dx + dy * dy) + 0.01
            f['vx'] += dx / dist * 0.04; f['vy'] += dy / dist * 0.04
            f['vx'] *= 0.95; f['vy'] *= 0.95
            f['x'] += f['vx']; f['y'] += f['vy']
            f['change_timer'] -= 1
            if f['change_timer'] <= 0:
                f['target_x'] = random.uniform(0, w)
                f['target_y'] = random.uniform(0, h)
                f['change_timer'] = random.randint(60, 200)
        for leaf in self.leaves:
            leaf['x'] += leaf['vx'] + math.sin(self.t * 5 * leaf['sway'] + leaf['phase']) * 0.6
            leaf['y'] += leaf['vy'] * leaf['depth']
            leaf['rotation'] += leaf['rot_speed']
            if leaf['y'] > h + 20:
                leaf['y'] = -20; leaf['x'] = random.uniform(-50, w + 50)

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        bg = QLinearGradient(0, 0, 0, h)
        bg.setColorAt(0, QColor(15, 30, 25, 220))
        bg.setColorAt(0.5, QColor(20, 40, 30, 180))
        bg.setColorAt(1.0, QColor(10, 25, 18, 220))
        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        moon_grad = QRadialGradient(w * 0.85, -50, w * 0.7)
        moon_grad.setColorAt(0, QColor(220, 240, 200, 80))
        moon_grad.setColorAt(1, QColor(220, 240, 200, 0))
        painter.setBrush(QBrush(moon_grad))
        painter.drawRect(rect)

        for tree in self.trees:
            tx = tree['x']; tw = tree['w']; th = tree['h']
            pts = [QPointF(tx, h - th), QPointF(tx - tw / 2, h),
                   QPointF(tx + tw / 2, h)]
            painter.setBrush(QColor(8, 18, 12, 220))
            painter.setPen(Qt.NoPen)
            painter.drawPolygon(QPolygonF(pts))
            for i in range(3):
                offset = i * 25
                pts2 = [QPointF(tx, h - th + offset),
                        QPointF(tx - tw / 2 + i * 5, h - 30 - i * 10),
                        QPointF(tx + tw / 2 - i * 5, h - 30 - i * 10)]
                painter.setBrush(QColor(15, 30, 22, 200))
                painter.drawPolygon(QPolygonF(pts2))

        for layer in range(3):
            mist_y = h * (0.55 + layer * 0.15)
            mist = QLinearGradient(0, mist_y - 30, 0, mist_y + 30)
            mist.setColorAt(0, QColor(180, 220, 200, 0))
            mist.setColorAt(0.5, QColor(180, 220, 200, 30 - layer * 5))
            mist.setColorAt(1, QColor(180, 220, 200, 0))
            painter.setBrush(QBrush(mist))
            painter.drawRect(QRectF(0, mist_y - 30, w, 60))

        sorted_leaves = sorted(self.leaves, key=lambda x: x['depth'])
        for leaf in sorted_leaves:
            painter.save()
            painter.translate(leaf['x'], leaf['y'])
            painter.rotate(leaf['rotation'] * 57.3)
            c = leaf['color']
            a = int(200 * leaf['depth'])
            painter.setPen(QPen(QColor(c.red() - 30, c.green() - 30, c.blue() - 30, a), 1))
            painter.setBrush(QColor(c.red(), c.green(), c.blue(), a))
            r = leaf['r'] * leaf['depth']
            path = QPainterPath()
            path.moveTo(0, -r)
            path.cubicTo(r * 0.7, -r * 0.5, r * 0.7, r * 0.5, 0, r)
            path.cubicTo(-r * 0.7, r * 0.5, -r * 0.7, -r * 0.5, 0, -r)
            painter.drawPath(path)
            painter.setPen(QPen(QColor(c.red() - 50, c.green() - 50, c.blue() - 50, a), 0.8))
            painter.drawLine(QPointF(0, -r), QPointF(0, r))
            painter.restore()

        painter.setPen(Qt.NoPen)
        for f in self.fireflies:
            glow_alpha = int(150 + 100 * math.sin(self.t * 10 * f['pulse'] + f['phase']))
            glow_alpha = max(40, min(255, glow_alpha))
            grad = QRadialGradient(f['x'], f['y'], f['r'] * 5)
            grad.setColorAt(0, QColor(255, 240, 100, glow_alpha // 2))
            grad.setColorAt(1, QColor(255, 240, 100, 0))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(f['x'], f['y']), f['r'] * 5, f['r'] * 5)
            painter.setBrush(QColor(255, 255, 200, glow_alpha))
            painter.drawEllipse(QPointF(f['x'], f['y']), f['r'], f['r'])


class NeonCityParticles:
    """🌆 赛博雨夜 - 倾斜雨滴+霓虹招牌+地面涟漪+车灯"""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.t = 0.0
        self.drops = []
        for _ in range(180):
            self.drops.append({
                'x': random.uniform(-50, w + 50), 'y': random.uniform(-50, h),
                'vy': random.uniform(8, 14), 'vx': random.uniform(2, 4),
                'len': random.uniform(8, 18),
                'alpha': random.randint(80, 180),
            })
        self.signs = []
        sign_texts = ['寿司', '拉面', 'OPEN', 'BAR', '居酒屋', '24H', 'NEON', '東京']
        for _ in range(8):
            self.signs.append({
                'x': random.uniform(20, w - 80), 'y': random.uniform(50, h - 100),
                'text': random.choice(sign_texts),
                'color': random.choice([QColor(255, 80, 180), QColor(80, 220, 255),
                                         QColor(255, 220, 100), QColor(180, 100, 255)]),
                'phase': random.uniform(0, math.pi * 2),
                'flicker': random.uniform(0.05, 0.15),
                'on': True,
            })
        self.ripples = []
        self.buildings = []
        bx = 0
        while bx < w:
            bw = random.uniform(40, 90); bh = random.uniform(120, 240)
            self.buildings.append({'x': bx, 'w': bw, 'h': bh, 'windows': []})
            for i in range(int(bh / 12)):
                if random.random() < 0.4:
                    self.buildings[-1]['windows'].append({
                        'wx': random.uniform(0, bw - 4), 'wy': i * 12,
                        'on': random.random() < 0.6,
                    })
            bx += bw

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.04
        for d in self.drops:
            d['y'] += d['vy']; d['x'] += d['vx']
            if d['y'] > h:
                if random.random() < 0.05 and len(self.ripples) < 30:
                    self.ripples.append({
                        'x': d['x'], 'y': h - 5,
                        'r': 0, 'max_r': random.uniform(20, 40),
                        'alpha': 200,
                    })
                d['y'] = -20; d['x'] = random.uniform(-50, w + 50)
        for r in self.ripples[:]:
            r['r'] += 0.8; r['alpha'] -= 5
            if r['alpha'] <= 0:
                self.ripples.remove(r)
        for s in self.signs:
            if random.random() < s['flicker']:
                s['on'] = not s['on']

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        bg = QLinearGradient(0, 0, 0, h)
        bg.setColorAt(0, QColor(10, 12, 30, 230))
        bg.setColorAt(0.5, QColor(20, 18, 45, 200))
        bg.setColorAt(1.0, QColor(15, 12, 35, 230))
        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        bx_acc = 0
        for b in self.buildings:
            painter.setBrush(QColor(8, 10, 22, 200))
            painter.setPen(Qt.NoPen)
            painter.drawRect(QRectF(bx_acc, h - b['h'], b['w'], b['h']))
            for win in b['windows']:
                if win['on']:
                    painter.setBrush(QColor(255, 220, 150, 120))
                    painter.drawRect(QRectF(bx_acc + win['wx'], h - b['h'] + win['wy'], 4, 6))
            bx_acc += b['w']

        for s in self.signs:
            if not s['on']: continue
            c = s['color']
            glow_alpha = int(180 + 60 * math.sin(self.t * 3 + s['phase']))
            glow_alpha = max(80, min(255, glow_alpha))
            grad = QRadialGradient(s['x'] + 30, s['y'] + 15, 50)
            grad.setColorAt(0, QColor(c.red(), c.green(), c.blue(), glow_alpha // 2))
            grad.setColorAt(1, QColor(c.red(), c.green(), c.blue(), 0))
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.NoPen)
            painter.drawRect(QRectF(s['x'] - 20, s['y'] - 20, 100, 60))
            painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(), glow_alpha), 2))
            painter.setBrush(QColor(0, 0, 0, 100))
            painter.drawRect(QRectF(s['x'], s['y'], 60, 30))
            painter.setPen(QColor(c.red(), c.green(), c.blue(), glow_alpha))
            font = painter.font()
            font.setBold(True); font.setPointSize(11)
            painter.setFont(font)
            painter.drawText(QRectF(s['x'], s['y'], 60, 30), Qt.AlignCenter, s['text'])

        painter.setBrush(Qt.NoBrush)
        for r in self.ripples:
            painter.setPen(QPen(QColor(255, 80, 180, r['alpha']), 1.0))
            painter.drawEllipse(QPointF(r['x'], r['y']), r['r'], r['r'] * 0.3)

        for d in self.drops:
            painter.setPen(QPen(QColor(150, 180, 240, d['alpha']), 1.2))
            painter.drawLine(QPointF(d['x'], d['y']),
                             QPointF(d['x'] - d['vx'] * 1.5, d['y'] - d['vy'] * 1.5))


class StormParticles:
    """⚡ 雷暴天空 - 闪电+暴雨+乌云"""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.t = 0.0
        self.rain = []
        for _ in range(220):
            self.rain.append({
                'x': random.uniform(-30, w + 30), 'y': random.uniform(-30, h),
                'vy': random.uniform(15, 22), 'vx': random.uniform(-3, -1),
                'len': random.uniform(15, 25),
                'alpha': random.randint(60, 140),
            })
        self.lightning_active = False
        self.lightning_alpha = 0
        self.lightning_path = []
        self.lightning_branches = []
        self.lightning_timer = 60
        self.clouds = []
        for _ in range(5):
            self.clouds.append({
                'x': random.uniform(-50, w), 'y': random.uniform(20, 100),
                'r': random.uniform(80, 140),
                'vx': random.uniform(0.2, 0.5),
                'phase': random.uniform(0, math.pi * 2),
            })

    def _gen_lightning(self, w, h):
        sx = random.uniform(w * 0.2, w * 0.8); sy = 0
        ex = sx + random.uniform(-w * 0.3, w * 0.3)
        ey = h * random.uniform(0.5, 0.9)
        pts = [(sx, sy)]
        steps = random.randint(8, 14)
        for i in range(1, steps):
            ratio = i / steps
            tx = sx + (ex - sx) * ratio + random.uniform(-30, 30)
            ty = sy + (ey - sy) * ratio + random.uniform(-15, 15)
            pts.append((tx, ty))
        pts.append((ex, ey))
        self.lightning_path = pts
        self.lightning_branches = []
        for _ in range(random.randint(2, 5)):
            idx = random.randint(1, len(pts) - 2)
            bsx, bsy = pts[idx]
            bpts = [(bsx, bsy)]
            for _ in range(random.randint(3, 6)):
                bsx += random.uniform(-40, 40); bsy += random.uniform(10, 30)
                bpts.append((bsx, bsy))
            self.lightning_branches.append(bpts)

    def update(self, w, h):
        self.w, self.h = w, h
        self.t += 0.03
        for d in self.rain:
            d['y'] += d['vy']; d['x'] += d['vx']
            if d['y'] > h:
                d['y'] = -20; d['x'] = random.uniform(-30, w + 30)
        for c in self.clouds:
            c['x'] += c['vx']
            if c['x'] > w + c['r']: c['x'] = -c['r']
        self.lightning_timer -= 1
        if self.lightning_timer <= 0:
            self.lightning_active = True
            self.lightning_alpha = 255
            self._gen_lightning(w, h)
            self.lightning_timer = random.randint(60, 200)
        if self.lightning_active:
            self.lightning_alpha -= 15
            if self.lightning_alpha <= 0:
                self.lightning_active = False
                self.lightning_alpha = 0

    def draw(self, painter, rect):
        w, h = rect.width(), rect.height()
        bg = QLinearGradient(0, 0, 0, h)
        flash = self.lightning_alpha / 255 * 50 if self.lightning_active else 0
        bg.setColorAt(0, QColor(int(20 + flash), int(22 + flash), int(40 + flash), 230))
        bg.setColorAt(0.5, QColor(int(30 + flash * 0.8), int(30 + flash * 0.8), int(50 + flash), 200))
        bg.setColorAt(1.0, QColor(int(35 + flash * 0.5), int(35 + flash * 0.5), int(55 + flash * 0.5), 220))
        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)

        for c in self.clouds:
            grad = QRadialGradient(c['x'], c['y'], c['r'])
            grad.setColorAt(0, QColor(40, 35, 60, 220))
            grad.setColorAt(1, QColor(30, 25, 50, 0))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(c['x'], c['y']), c['r'], c['r'] * 0.6)
            grad2 = QRadialGradient(c['x'] - c['r'] * 0.2, c['y'], c['r'] * 0.7)
            grad2.setColorAt(0, QColor(50, 45, 75, 200))
            grad2.setColorAt(1, QColor(30, 25, 50, 0))
            painter.setBrush(QBrush(grad2))
            painter.drawEllipse(QPointF(c['x'] - c['r'] * 0.2, c['y']),
                                c['r'] * 0.7, c['r'] * 0.4)

        if self.lightning_active and len(self.lightning_path) > 1:
            for i in range(len(self.lightning_path) - 1):
                p1 = self.lightning_path[i]; p2 = self.lightning_path[i + 1]
                painter.setPen(QPen(QColor(180, 200, 255, self.lightning_alpha // 2), 8))
                painter.drawLine(QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1]))
            for i in range(len(self.lightning_path) - 1):
                p1 = self.lightning_path[i]; p2 = self.lightning_path[i + 1]
                painter.setPen(QPen(QColor(255, 255, 255, self.lightning_alpha), 2.5))
                painter.drawLine(QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1]))
            for branch in self.lightning_branches:
                for i in range(len(branch) - 1):
                    p1 = branch[i]; p2 = branch[i + 1]
                    painter.setPen(QPen(QColor(180, 200, 255, self.lightning_alpha // 3), 3))
                    painter.drawLine(QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1]))
                    painter.setPen(QPen(QColor(255, 255, 255, int(self.lightning_alpha * 0.7)), 1.5))
                    painter.drawLine(QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1]))

        for d in self.rain:
            painter.setPen(QPen(QColor(180, 200, 255, d['alpha']), 1.4))
            painter.drawLine(QPointF(d['x'], d['y']),
                             QPointF(d['x'] - d['vx'] * 1.5, d['y'] - d['vy'] * 1.2))


_PARTICLE_REGISTRY = {
    'cyberpunk': CyberpunkParticles,
    'space': SpaceParticles,
    'wheat': WheatParticles,
    'candy': CandyParticles,
    'ocean': OceanParticles,
    'sakura': SakuraParticles,
    'lava': LavaParticles,
    'arctic': ArcticParticles,
    'retro': RetroParticles,
    'forest': ForestParticles,
    'neoncity': NeonCityParticles,
    'storm': StormParticles,
}


def create_particle_system(theme_id, w, h):
    cls = _PARTICLE_REGISTRY.get(theme_id, CyberpunkParticles)
    return cls(w, h)



# ═══════════════════════════════════════════════════════════════════
# 全局效果层（鼠标光圈 + 点击粒子爆炸 + 主题冲击波）
# ═══════════════════════════════════════════════════════════════════

class GlobalEffectLayer:
    """
    全局动效叠加层 - 由 MainWindow 在 paintEvent 中调用 draw()。
    管理：
      - 鼠标光圈跟随
      - 点击粒子爆炸
      - 主题切换冲击波
    """
    def __init__(self):
        self.mouse_x = -1000
        self.mouse_y = -1000
        self.mouse_visible = False
        self.mouse_phase = 0.0
        # 爆炸粒子: (x, y, vx, vy, life, max_life, color, size)
        self.explosions = []
        # 冲击波: (x, y, radius, max_radius, alpha, color)
        self.shockwaves = []

    def update(self):
        self.mouse_phase += 0.08
        # 爆炸粒子衰减
        new_exp = []
        for p in self.explosions:
            p['life'] -= 0.025
            if p['life'] > 0:
                p['x'] += p['vx']; p['y'] += p['vy']
                p['vy'] += 0.15  # 重力
                p['vx'] *= 0.97
                new_exp.append(p)
        self.explosions = new_exp
        # 冲击波扩散
        new_sw = []
        for s in self.shockwaves:
            s['radius'] += s['speed']
            s['alpha'] -= s['fade']
            if s['alpha'] > 0:
                new_sw.append(s)
        self.shockwaves = new_sw

    def set_mouse(self, x, y, visible=True):
        self.mouse_x = x
        self.mouse_y = y
        self.mouse_visible = visible

    def burst(self, x, y, color, count=14):
        """点击粒子爆炸"""
        for _ in range(count):
            ang = random.uniform(0, math.pi * 2)
            speed = random.uniform(2.0, 6.0)
            self.explosions.append({
                'x': x, 'y': y,
                'vx': math.cos(ang) * speed,
                'vy': math.sin(ang) * speed - 1.5,  # 向上偏向
                'life': 1.0,
                'max_life': 1.0,
                'color': color,
                'size': random.uniform(2.5, 5.0),
            })

    def shockwave(self, x, y, color, max_radius=400, speed=10, fade=4):
        """冲击波（主题切换/启动战网时用）"""
        self.shockwaves.append({
            'x': x, 'y': y,
            'radius': 0,
            'max_radius': max_radius,
            'alpha': 220,
            'speed': speed,
            'fade': fade,
            'color': color,
        })

    def draw(self, painter, rect):
        # 冲击波
        for s in self.shockwaves:
            c = s['color']
            painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(), int(s['alpha'])), 3))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(s['x'], s['y']), s['radius'], s['radius'])
            # 内圈淡光
            painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(),
                                       int(s['alpha'] * 0.4)), 2))
            painter.drawEllipse(QPointF(s['x'], s['y']),
                                s['radius'] * 0.85, s['radius'] * 0.85)

        # 爆炸粒子
        painter.setPen(Qt.NoPen)
        for p in self.explosions:
            ratio = max(0, p['life'] / p['max_life'])
            a = int(255 * ratio)
            c = p['color']
            r = p['size'] * ratio
            # 外发光
            grad = QRadialGradient(p['x'], p['y'], r * 3)
            grad.setColorAt(0, QColor(c.red(), c.green(), c.blue(), a))
            grad.setColorAt(1, QColor(c.red(), c.green(), c.blue(), 0))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(p['x'], p['y']), r * 3, r * 3)
            # 核心
            painter.setBrush(QColor(255, 255, 255, a))
            painter.drawEllipse(QPointF(p['x'], p['y']), r, r)

        # 鼠标光圈
        if self.mouse_visible and 0 < self.mouse_x < rect.width() and 0 < self.mouse_y < rect.height():
            theme = T()
            c = theme['primary']
            pulse = (math.sin(self.mouse_phase) + 1) / 2
            outer_r = 35 + 8 * pulse
            grad = QRadialGradient(self.mouse_x, self.mouse_y, outer_r)
            grad.setColorAt(0, QColor(c.red(), c.green(), c.blue(), 60))
            grad.setColorAt(0.6, QColor(c.red(), c.green(), c.blue(), 25))
            grad.setColorAt(1, QColor(c.red(), c.green(), c.blue(), 0))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(self.mouse_x, self.mouse_y), outer_r, outer_r)
            # 内核圈
            painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(), int(120 + 60 * pulse)), 1.5))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(self.mouse_x, self.mouse_y), 8, 8)


# ═══════════════════════════════════════════════════════════════════
# 通用 UI 组件（主题感知）
# ═══════════════════════════════════════════════════════════════════

class ThemedLineEdit(QLineEdit):
    """主题感知输入框 - 聚焦时主题色边框流光"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._glow_timer = QTimer(self)
        self._glow_timer.timeout.connect(self.update)
        self._phase = 0.0
        self._is_focused = False

    def focusInEvent(self, event):
        self._is_focused = True
        self._glow_timer.start(25)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self._is_focused = False
        self._glow_timer.stop()
        self.update()
        super().focusOutEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._is_focused:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            rect = self.rect()
            self._phase += 0.12
            theme = T()
            c1 = theme['primary']; c2 = theme['secondary']
            t = (math.sin(self._phase) + 1) / 2
            a = int(180 + 75 * math.sin(self._phase))
            grad = QLinearGradient(0, 0, rect.width(), 0)
            grad.setColorAt(0, QColor(c1.red(), c1.green(), c1.blue(), 0))
            grad.setColorAt(max(0, min(1, t - 0.15)),
                            QColor(c1.red(), c1.green(), c1.blue(), a))
            grad.setColorAt(t, QColor(c2.red(), c2.green(), c2.blue(), a))
            grad.setColorAt(max(0, min(1, t + 0.15)),
                            QColor(c1.red(), c1.green(), c1.blue(), a))
            grad.setColorAt(1, QColor(c1.red(), c1.green(), c1.blue(), 0))
            painter.setPen(QPen(QBrush(grad), 2.5))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect.adjusted(1, 1, -2, -2), 8, 8)


class ThemedIconBox(QFrame):
    """主题感知图标盒 - 旋转光环+图标"""
    def __init__(self, icon_char, color_hex):
        super().__init__()
        self.setFixedSize(44, 44)
        self.icon_char = icon_char
        self.color = QColor(color_hex)
        self._phase = random.uniform(0, math.pi * 2)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def _tick(self):
        self._phase += 0.05
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        cx, cy = rect.width() / 2, rect.height() / 2
        r = min(cx, cy) - 3
        conical = QConicalGradient(cx, cy, self._phase * 57.3)
        c1 = QColor(self.color); c1.setAlpha(200)
        c2 = QColor(self.color); c2.setAlpha(0)
        conical.setColorAt(0, c1); conical.setColorAt(0.5, c2); conical.setColorAt(1, c1)
        painter.setPen(QPen(QBrush(conical), 2.0))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), r, r)
        inner = QRadialGradient(cx, cy, r * 0.8)
        bg = QColor(self.color); bg.setAlpha(50)
        inner.setColorAt(0, bg)
        inner.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(inner))
        painter.drawEllipse(QPointF(cx, cy), r * 0.75, r * 0.75)
        painter.setPen(self.color)
        font = painter.font()
        font.setPointSize(14)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, self.icon_char)


class ThemedButton(QPushButton):
    """主题感知按钮 - 削角+霓虹悬停+点击触发全局粒子爆炸"""
    # 全局引用，让按钮在点击时通知主窗口的特效层
    _effect_callback = None

    @classmethod
    def set_effect_callback(cls, cb):
        """cb(x_global, y_global, color_qcolor)"""
        cls._effect_callback = cb

    def __init__(self, text, color_scheme='primary', parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.color_scheme = color_scheme
        self._hover = False
        self._phase = random.uniform(0, math.pi * 2)
        self._hover_anim = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)
        self.setMinimumHeight(36)

    def _get_color(self):
        theme = T()
        m = {
            'primary': theme['primary'],
            'secondary': theme['secondary'],
            'accent': theme['accent'],
            'cyan': QColor(0, 255, 255),
            'magenta': QColor(255, 0, 128),
            'purple': QColor(168, 85, 247),
            'red': QColor(255, 60, 60),
            'green': QColor(0, 255, 128),
            'orange': QColor(255, 165, 0),
            'blue': QColor(59, 130, 246),
            'gold': QColor(255, 215, 0),
            'pink': QColor(255, 150, 200),
        }
        return m.get(self.color_scheme, theme['primary'])

    def _tick(self):
        self._phase += 0.06
        target = 1.0 if self._hover else 0.0
        self._hover_anim += (target - self._hover_anim) * 0.15
        self.update()

    def enterEvent(self, event):
        self._hover = True
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        # 触发全局粒子爆炸
        if event.button() == Qt.LeftButton and ThemedButton._effect_callback:
            try:
                gp = self.mapToGlobal(event.position().toPoint())
                ThemedButton._effect_callback(gp.x(), gp.y(), self._get_color())
            except Exception:
                pass
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        c = self._get_color()
        cut = 8
        path = QPainterPath()
        path.moveTo(cut, 0)
        path.lineTo(rect.width() - cut, 0)
        path.lineTo(rect.width(), cut)
        path.lineTo(rect.width(), rect.height() - cut)
        path.lineTo(rect.width() - cut, rect.height())
        path.lineTo(cut, rect.height())
        path.lineTo(0, rect.height() - cut)
        path.lineTo(0, cut)
        path.closeSubpath()
        bg_a = int(30 + 70 * self._hover_anim)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(c.red(), c.green(), c.blue(), bg_a))
        painter.drawPath(path)
        border_a = int(150 + 105 * self._hover_anim)
        gw = 1.5 + 1.0 * self._hover_anim
        painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(), border_a), gw))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        if self._hover_anim > 0.1:
            scan_y = (math.sin(self._phase) + 1) / 2 * rect.height()
            sg = QLinearGradient(0, scan_y - 10, 0, scan_y + 10)
            sg.setColorAt(0, QColor(255, 255, 255, 0))
            sg.setColorAt(0.5, QColor(255, 255, 255, int(50 * self._hover_anim)))
            sg.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(sg))
            painter.drawPath(path)
        painter.setPen(QColor(255, 255, 255, int(220 + 35 * self._hover_anim)))
        font = painter.font()
        font.setBold(True); font.setPointSize(9)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, self.text())


class MegaLaunchButton(QPushButton):
    """主发射按钮 - 主题感知 + 大冲击波"""
    _effect_callback = None
    _shockwave_callback = None

    @classmethod
    def set_callbacks(cls, effect_cb, shockwave_cb):
        cls._effect_callback = effect_cb
        cls._shockwave_callback = shockwave_cb

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self._phase = 0.0
        self._hover = False
        self._ripples = []
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)

    def _tick(self):
        self._phase += 0.04
        self._ripples = [(r, a - 3) for r, a in self._ripples if a > 0]
        self.update()

    def enterEvent(self, event):
        self._hover = True
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._ripples.append((0, 255))
        if event.button() == Qt.LeftButton:
            theme = T()
            try:
                gp = self.mapToGlobal(event.position().toPoint())
                if MegaLaunchButton._effect_callback:
                    MegaLaunchButton._effect_callback(gp.x(), gp.y(), theme['accent'], 24)
                if MegaLaunchButton._shockwave_callback:
                    MegaLaunchButton._shockwave_callback(gp.x(), gp.y(), theme['primary'])
            except Exception:
                pass
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        w, h = rect.width(), rect.height()
        theme = T()
        c1, c2, c3 = theme['primary'], theme['secondary'], theme['accent']
        cut = 12
        path = QPainterPath()
        path.moveTo(cut, 0); path.lineTo(w - cut, 0); path.lineTo(w, cut)
        path.lineTo(w, h - cut); path.lineTo(w - cut, h); path.lineTo(cut, h)
        path.lineTo(0, h - cut); path.lineTo(0, cut); path.closeSubpath()
        bg = QLinearGradient(0, 0, w, 0)
        pulse = (math.sin(self._phase) + 1) / 2
        if self._hover:
            bg.setColorAt(0, QColor(c1.red(), c1.green(), c1.blue(), 100))
            bg.setColorAt(pulse, QColor(c2.red(), c2.green(), c2.blue(), 110))
            bg.setColorAt(1, QColor(c3.red(), c3.green(), c3.blue(), 100))
        else:
            bg.setColorAt(0, QColor(c1.red(), c1.green(), c1.blue(), 50))
            bg.setColorAt(pulse, QColor(c2.red(), c2.green(), c2.blue(), 60))
            bg.setColorAt(1, QColor(c3.red(), c3.green(), c3.blue(), 50))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawPath(path)
        border = QLinearGradient(0, 0, w, 0)
        shift = (math.sin(self._phase * 2) + 1) / 2
        border.setColorAt(0, QColor(c1.red(), c1.green(), c1.blue(), 220))
        border.setColorAt(shift, QColor(c2.red(), c2.green(), c2.blue(), 255))
        border.setColorAt(1, QColor(c1.red(), c1.green(), c1.blue(), 220))
        painter.setPen(QPen(QBrush(border), 2.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        scan_x = (self._phase * 80) % (w + 100) - 50
        sg = QLinearGradient(scan_x - 50, 0, scan_x + 50, 0)
        sg.setColorAt(0, QColor(255, 255, 255, 0))
        sg.setColorAt(0.5, QColor(255, 255, 255, 70))
        sg.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(sg))
        painter.drawPath(path)
        for radius, alpha in self._ripples:
            r = radius + (255 - alpha) * 0.5
            painter.setPen(QPen(QColor(c1.red(), c1.green(), c1.blue(), alpha // 3), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(w / 2, h / 2), r, r * 0.3)
        painter.setPen(QColor(255, 255, 255, 240))
        font = painter.font()
        font.setBold(True); font.setPointSize(11)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, self.text())


class FlipNumberLabel(QLabel):
    """
    数字翻牌标签 - 切号时数字滚动而非直接替换。
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._cur = 0
        self._target = 0
        self._anim_progress = 1.0
        self._old = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def set_value(self, value):
        try:
            v = int(value)
        except Exception:
            self.setText(str(value))
            return
        if v == self._target:
            return
        self._old = self._cur
        self._target = v
        self._anim_progress = 0.0

    def _tick(self):
        if self._anim_progress < 1.0:
            self._anim_progress = min(1.0, self._anim_progress + 0.12)
            # 缓动
            t = 1 - (1 - self._anim_progress) ** 3
            self._cur = int(self._old + (self._target - self._old) * t)
            self.setText(str(self._cur))
            self.update()
        elif self._cur != self._target:
            self._cur = self._target
            self.setText(str(self._cur))



# ═══════════════════════════════════════════════════════════════════
# 主题选择面板
# ═══════════════════════════════════════════════════════════════════

class ThemePickerPanel(QWidget):
    """主题选择浮动面板（分类+预览+滚动）"""
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(360, 540)
        self.setup_ui()

    def setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(15, 15, 15, 15)
        outer.setSpacing(10)

        title = QLabel("✨ 选择主题风格")
        title.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
        outer.addWidget(title)

        subtitle = QLabel(f"共 {len(THEMES)} 种风格 · 点击即可切换")
        subtitle.setStyleSheet("color: #B0B0C0; font-size: 11px;")
        outer.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                background: rgba(0,0,0,0.3); width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.4); border-radius: 4px; min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(8)

        groups = {}
        for tid, th in THEMES.items():
            cat = th.get('category', '其他')
            groups.setdefault(cat, []).append((tid, th))

        cat_order = ['赛博', '科幻', '自然', '梦幻', '极端', '复古', '其他']
        for cat in cat_order:
            if cat not in groups:
                continue
            cat_label = QLabel(f"  ── {cat} ──")
            cat_label.setStyleSheet(
                "color: #888; font-size: 10px; font-weight: bold; padding-top: 4px;"
            )
            layout.addWidget(cat_label)
            for tid, th in groups[cat]:
                btn = self._make_theme_button(tid, th)
                layout.addWidget(btn)

        layout.addStretch()
        scroll.setWidget(container)
        outer.addWidget(scroll)

    def _make_theme_button(self, theme_id, theme):
        btn = QPushButton()
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(50)
        c = theme['primary']; sec = theme['secondary']; acc = theme['accent']
        is_active = theme_id == CURRENT_THEME

        layout = QHBoxLayout(btn)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(10)

        lbl_name = QLabel(theme['name'])
        lbl_name.setStyleSheet(
            "color: white; font-size: 14px; font-weight: bold; background: transparent;"
        )
        layout.addWidget(lbl_name)
        layout.addStretch()

        for color in [c, sec, acc]:
            dot = QLabel()
            dot.setFixedSize(14, 14)
            dot.setStyleSheet(
                f"background: rgb({color.red()},{color.green()},{color.blue()});"
                f"border-radius: 7px; border: 1px solid rgba(255,255,255,0.4);"
            )
            layout.addWidget(dot)

        if is_active:
            check = QLabel("✓")
            check.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
            layout.addWidget(check)

        border_w = 2 if is_active else 1
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba({c.red()},{c.green()},{c.blue()},90),
                    stop:1 rgba({sec.red()},{sec.green()},{sec.blue()},90));
                border: {border_w}px solid rgba({c.red()},{c.green()},{c.blue()},220);
                border-radius: 10px;
                text-align: left;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba({c.red()},{c.green()},{c.blue()},170),
                    stop:1 rgba({sec.red()},{sec.green()},{sec.blue()},170));
                border: 2px solid white;
            }}
        """)
        btn.clicked.connect(lambda checked=False, tid=theme_id: self.select_theme(tid))
        return btn

    def select_theme(self, theme_id):
        global CURRENT_THEME
        CURRENT_THEME = theme_id
        save_config(theme=theme_id)
        signals.theme_changed.emit()
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.setBrush(QColor(20, 20, 35, 245))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 14, 14)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1.5))
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 14, 14)


# ═══════════════════════════════════════════════════════════════════
# 设置面板
# ═══════════════════════════════════════════════════════════════════

class SettingsDialog(QWidget):
    """设置：透明度 + 备份 + 批量操作 + 战网路径"""
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(460, 600)
        self._is_tracking = False
        self._start_pos = None
        self.setup_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        theme = T()
        painter.setBrush(QColor(15, 15, 30, 245))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 14, 14)
        c = theme['primary']
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(c.red(), c.green(), c.blue(), 150), 1.5))
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 14, 14)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() < 50:
            self._is_tracking = True
            self._start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._is_tracking:
            self.move(event.globalPosition().toPoint() - self._start_pos)

    def mouseReleaseEvent(self, event):
        self._is_tracking = False

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 20)
        layout.setSpacing(12)

        title_bar = QHBoxLayout()
        lbl_title = QLabel("⚙️ 设置中心")
        lbl_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        title_bar.addWidget(lbl_title)
        title_bar.addStretch()
        btn_close = ThemedButton("✕", 'red')
        btn_close.setFixedSize(32, 30)
        btn_close.clicked.connect(self.close)
        title_bar.addWidget(btn_close)
        layout.addLayout(title_bar)
        layout.addWidget(self._make_separator())

        # 透明度
        layout.addWidget(self._make_section_title("🎚️ 窗口透明度"))
        op_layout = QHBoxLayout()
        cfg = load_config()
        current_op = cfg.get('opacity', 100)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(40)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(current_op)
        self.opacity_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px; background: rgba(255,255,255,0.15); border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00D4FF, stop:1 #7C3AED);
                width: 18px; margin: -7px 0; border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00D4FF, stop:1 #7C3AED);
                border-radius: 3px;
            }
        """)
        self.opacity_slider.valueChanged.connect(self._on_opacity_change)
        op_layout.addWidget(self.opacity_slider)

        self.lbl_opacity_value = QLabel(f"{current_op}%")
        self.lbl_opacity_value.setStyleSheet("color: #00D4FF; font-weight: bold; font-size: 13px; min-width: 50px;")
        op_layout.addWidget(self.lbl_opacity_value)
        layout.addLayout(op_layout)

        layout.addWidget(self._make_separator())

        # 战网路径
        layout.addWidget(self._make_section_title("🎮 战网启动器路径"))
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit(cfg.get('bnet_path', DEFAULT_BNET_LAUNCHER))
        self.path_edit.setStyleSheet("""
            QLineEdit {
                background: rgba(0,0,0,0.4); color: #E0E0FF;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 5px; padding: 6px 10px; font-size: 11px;
            }
        """)
        path_layout.addWidget(self.path_edit, 1)
        btn_browse = ThemedButton("浏览", 'primary')
        btn_browse.setFixedSize(60, 30)
        btn_browse.clicked.connect(self._browse_bnet)
        path_layout.addWidget(btn_browse)
        btn_save_path = ThemedButton("保存", 'accent')
        btn_save_path.setFixedSize(60, 30)
        btn_save_path.clicked.connect(self._save_bnet_path)
        path_layout.addWidget(btn_save_path)
        layout.addLayout(path_layout)

        layout.addWidget(self._make_separator())

        # 备份
        layout.addWidget(self._make_section_title("💾 数据备份"))
        self.chk_auto_backup = QCheckBox("启动时自动备份账号文件 (保留最近14天)")
        self.chk_auto_backup.setChecked(cfg.get('auto_backup', True))
        self.chk_auto_backup.setStyleSheet("""
            QCheckBox { color: #E0E0E0; font-size: 12px; spacing: 8px; }
            QCheckBox::indicator {
                width: 16px; height: 16px;
                background: rgba(255,255,255,0.1);
                border: 1.5px solid rgba(255,255,255,0.3);
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background: #00D4FF; border: 1.5px solid #00D4FF;
            }
        """)
        self.chk_auto_backup.stateChanged.connect(
            lambda s: save_config(auto_backup=(int(s) == 2))
        )
        layout.addWidget(self.chk_auto_backup)

        bk_btns = QHBoxLayout()
        btn_open_backup = ThemedButton("📁 打开备份目录", 'primary')
        btn_open_backup.setFixedHeight(34)
        btn_open_backup.clicked.connect(self._open_backup_dir)
        bk_btns.addWidget(btn_open_backup)
        btn_backup_now = ThemedButton("💾 立即备份", 'accent')
        btn_backup_now.setFixedHeight(34)
        btn_backup_now.clicked.connect(self._backup_now)
        bk_btns.addWidget(btn_backup_now)
        layout.addLayout(bk_btns)

        layout.addWidget(self._make_separator())

        # 批量操作
        layout.addWidget(self._make_section_title("🔧 批量操作"))
        bulk_btns = QGridLayout()
        bulk_btns.setSpacing(8)

        btn_reset_all = ThemedButton("🔄 全部重置为待登", 'green')
        btn_reset_all.setFixedHeight(36)
        btn_reset_all.clicked.connect(self._reset_all_unused)
        bulk_btns.addWidget(btn_reset_all, 0, 0)

        btn_mark_all = ThemedButton("✅ 全部标为已用", 'orange')
        btn_mark_all.setFixedHeight(36)
        btn_mark_all.clicked.connect(self._mark_all_used)
        bulk_btns.addWidget(btn_mark_all, 0, 1)

        btn_export = ThemedButton("📤 导出账号列表", 'secondary')
        btn_export.setFixedHeight(36)
        btn_export.clicked.connect(self._export_accounts)
        bulk_btns.addWidget(btn_export, 1, 0)

        btn_clear_stats = ThemedButton("🗑️ 清空统计数据", 'red')
        btn_clear_stats.setFixedHeight(36)
        btn_clear_stats.clicked.connect(self._clear_stats)
        bulk_btns.addWidget(btn_clear_stats, 1, 1)

        layout.addLayout(bulk_btns)
        layout.addWidget(self._make_separator())

        about = QLabel(
            f"🛡️ 战网管家 Pro Max Ultra v6.0\n"
            f"账号总数: {len(self.parent_window.db)} 个 | "
            f"今日切换: {get_today_stat()} 次\n"
            f"12 种主题 · 剪贴板注入 · 最近使用追踪"
        )
        about.setStyleSheet("color: #888; font-size: 11px;")
        about.setAlignment(Qt.AlignCenter)
        layout.addWidget(about)
        layout.addStretch()

    def _make_separator(self):
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background: rgba(255,255,255,0.08);")
        return sep

    def _make_section_title(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #00D4FF; font-size: 13px; font-weight: bold; padding-top: 4px;")
        return lbl

    def _on_opacity_change(self, value):
        self.lbl_opacity_value.setText(f"{value}%")
        self.parent_window.setWindowOpacity(value / 100.0)
        save_config(opacity=value)

    def _browse_bnet(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择战网启动器",
            DEFAULT_BNET_DIR if os.path.exists(DEFAULT_BNET_DIR) else "",
            "Battle.net Launcher (Battle.net Launcher.exe);;All (*.*)"
        )
        if path:
            self.path_edit.setText(path)

    def _save_bnet_path(self):
        path = self.path_edit.text().strip()
        save_config(bnet_path=path)
        self.parent_window.set_status_text(f"✓ 战网路径已保存", T()['accent'].name())

    def _open_backup_dir(self):
        backup_dir = os.path.join(BASE_DIR, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        try:
            if sys.platform == 'win32':
                os.startfile(backup_dir)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', backup_dir])
            else:
                try:
                    subprocess.Popen(['xdg-open', backup_dir])
                except Exception:
                    self.parent_window.set_status_text(f"路径: {backup_dir}", T()['accent'].name())
        except Exception as e:
            self.parent_window.set_status_text(f"✗ 无法打开: {e}", "#FF3030")

    def _backup_now(self):
        if not os.path.exists(FILE_PATH):
            self.parent_window.set_status_text("✗ 没有账号文件", "#FF3030")
            return
        backup_dir = os.path.join(BASE_DIR, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"accounts_manual_{ts}.txt")
        try:
            shutil.copy2(FILE_PATH, backup_file)
            self.parent_window.set_status_text(f"✓ 已备份: accounts_manual_{ts}.txt", T()['accent'].name())
        except Exception as e:
            self.parent_window.set_status_text(f"✗ 备份失败: {e}", "#FF3030")

    def _reset_all_unused(self):
        if not self._confirm("确认操作", "确定要将所有账号重置为【待登】状态吗？\n（不会清除最近使用时间）"):
            return
        for acc in self.parent_window.db:
            acc['used'] = False
        save_accounts(self.parent_window.db)
        self.parent_window.update_main_ui()
        if self.parent_window.list_window and self.parent_window.list_window.isVisible():
            self.parent_window.list_window.refresh_table()
        self.parent_window.set_status_text(f"✓ 已重置 {len(self.parent_window.db)} 个账号为待登")

    def _mark_all_used(self):
        if not self._confirm("确认操作", "确定要将所有账号标记为【已用】吗？"):
            return
        now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        for acc in self.parent_window.db:
            acc['used'] = True
            if not acc.get('last_used'):
                acc['last_used'] = now_str
        save_accounts(self.parent_window.db)
        self.parent_window.update_main_ui()
        if self.parent_window.list_window and self.parent_window.list_window.isVisible():
            self.parent_window.list_window.refresh_table()
        self.parent_window.set_status_text(f"✓ 已标记 {len(self.parent_window.db)} 个账号为已用")

    def _export_accounts(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "导出账号列表",
            f"accounts_export_{datetime.now().strftime('%Y%m%d')}.txt",
            "Text Files (*.txt);;All (*.*)"
        )
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                for acc in self.parent_window.db:
                    f.write(
                        f"{acc['user']}----{acc['pwd']}----{acc['secret']}"
                        f"----{acc.get('remark', '')}"
                        f"----{('USED' if acc.get('used') else 'UNUSED')}"
                        f"----{acc.get('last_used', '')}\n"
                    )
            self.parent_window.set_status_text(
                f"✓ 已导出 {len(self.parent_window.db)} 个账号", T()['accent'].name()
            )
        except Exception as e:
            self.parent_window.set_status_text(f"✗ 导出失败: {e}", "#FF3030")

    def _clear_stats(self):
        if not self._confirm("确认清空", "确定要清空所有切号统计数据吗？"):
            return
        save_config(stats={})
        self.parent_window.set_status_text("✓ 统计数据已清空")

    def _confirm(self, title, msg):
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setText(msg)
        box.setIcon(QMessageBox.Question)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setStyleSheet("""
            QMessageBox { background: rgb(25,25,40); color: white; }
            QMessageBox QLabel { color: white; font-size: 13px; }
            QMessageBox QPushButton {
                background: rgba(255,255,255,0.1); color: white;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 6px; padding: 6px 18px; min-width: 60px;
            }
            QMessageBox QPushButton:hover {
                background: rgba(124,77,255,0.3);
            }
        """)
        return box.exec() == QMessageBox.Yes


# ═══════════════════════════════════════════════════════════════════
# 数据总览大屏 (新增 "转到当前" 按钮 + "最近使用" 列)
# ═══════════════════════════════════════════════════════════════════

class DataOverviewWindow(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(960, 580)
        self._is_tracking = False
        self._start_pos = None
        self.particles = create_particle_system(CURRENT_THEME, 960, 580)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(25)
        self.setup_ui()
        self.apply_qss()
        self.refresh_table()
        signals.theme_changed.connect(self.on_theme_changed)

    def on_theme_changed(self):
        self.particles = create_particle_system(CURRENT_THEME, self.width(), self.height())
        self.apply_qss()
        self.update()

    def _tick(self):
        self.particles.update(self.width(), self.height())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        theme = T()
        painter.setBrush(QColor(theme['bg_color']))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 12, 12)
        self.particles.draw(painter, rect)
        c1 = theme['primary']; c2 = theme['secondary']
        bg = QLinearGradient(0, 0, rect.width(), rect.height())
        bg.setColorAt(0, QColor(c1.red(), c1.green(), c1.blue(), 150))
        bg.setColorAt(0.5, QColor(c2.red(), c2.green(), c2.blue(), 150))
        bg.setColorAt(1, QColor(c1.red(), c1.green(), c1.blue(), 150))
        painter.setPen(QPen(QBrush(bg), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 12, 12)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() < 60:
            self._is_tracking = True
            self._start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._is_tracking:
            self.move(event.globalPosition().toPoint() - self._start_pos)

    def mouseReleaseEvent(self, event):
        self._is_tracking = False

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 25)
        layout.setSpacing(15)

        # 标题栏
        title_bar = QHBoxLayout()
        self.lbl_title = QLabel("⬡ 数据矩阵终端 (双击切号 | Home键切换)")
        title_bar.addWidget(self.lbl_title)
        title_bar.addStretch()

        # 统计信息
        self.lbl_stat = QLabel("")
        self.lbl_stat.setStyleSheet("color: #B0B0C0; font-size: 11px;")
        title_bar.addWidget(self.lbl_stat)
        title_bar.addSpacing(10)

        btn_close = ThemedButton("✕", 'red')
        btn_close.setFixedSize(35, 35)
        btn_close.clicked.connect(self.hide)
        title_bar.addWidget(btn_close)
        layout.addLayout(title_bar)

        # 搜索 + 转到当前
        search_bar = QHBoxLayout()
        search_bar.setSpacing(10)
        self.search_input = ThemedLineEdit()
        self.search_input.setPlaceholderText("🔍 输入关键词搜索（账号 / 备注 / 密码）...")
        self.search_input.setObjectName("SearchInput")
        self.search_input.textChanged.connect(self.refresh_table)
        self.search_input.setFixedHeight(42)
        search_bar.addWidget(self.search_input, 1)

        # 「转到当前」按钮
        btn_goto = ThemedButton("📍 转到当前", 'accent')
        btn_goto.setFixedSize(110, 42)
        btn_goto.clicked.connect(self.scroll_to_current)
        search_bar.addWidget(btn_goto)

        # 「重置筛选」
        btn_clear = ThemedButton("🗑 清搜", 'primary')
        btn_clear.setFixedSize(80, 42)
        btn_clear.clicked.connect(lambda: self.search_input.setText(""))
        search_bar.addWidget(btn_clear)

        layout.addLayout(search_bar)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["状态", "账号", "密码", "备注", "最近使用", "idx"])
        h = self.table.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.Interactive)
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        h.setSectionResizeMode(3, QHeaderView.Stretch)
        h.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.hideColumn(5)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.itemDoubleClicked.connect(self.on_double_click)
        layout.addWidget(self.table)

    def apply_qss(self):
        theme = T()
        c = theme['primary']; sec = theme['secondary']
        self.lbl_title.setStyleSheet(f"color: {theme['text_color']}; font-weight: bold; font-size: 15px;")
        self.setStyleSheet(f"""
            QLineEdit#SearchInput {{
                background: {theme['input_bg']};
                border: 2px solid {theme['border']};
                border-radius: 8px;
                padding: 10px 18px;
                color: {theme['input_text']};
                font-size: 13px;
            }}
            QLineEdit#SearchInput:focus {{
                border: 2px solid {theme['text_color']};
            }}
            QTableWidget {{
                background-color: transparent;
                border: none;
                color: {theme['input_text']};
                font-size: 13px;
                outline: none;
                gridline-color: rgba({c.red()},{c.green()},{c.blue()},0.1);
            }}
            QHeaderView::section {{
                background: rgba({c.red()},{c.green()},{c.blue()},0.12);
                color: {theme['text_color']};
                padding: 12px;
                border: none;
                border-bottom: 1px solid rgba({c.red()},{c.green()},{c.blue()},0.4);
                font-weight: bold;
                font-size: 12px;
            }}
            QTableWidget::item {{
                padding: 9px;
                border-bottom: 1px solid rgba({c.red()},{c.green()},{c.blue()},0.05);
            }}
            QTableWidget::item:selected {{
                background: rgba({c.red()},{c.green()},{c.blue()},0.3);
                color: white;
            }}
            QTableWidget::item:hover {{
                background: rgba({sec.red()},{sec.green()},{sec.blue()},0.18);
            }}
            QScrollBar:vertical {{
                background: rgba(0,0,0,0.3); width: 8px; border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba({c.red()},{c.green()},{c.blue()},0.5);
                border-radius: 4px; min-height: 30px;
            }}
        """)

    def refresh_table(self):
        self.table.setRowCount(0)
        keyword = self.search_input.text().lower().strip()
        total = len(self.parent_app.db)
        used_count = sum(1 for a in self.parent_app.db if a.get('used'))
        unused_count = total - used_count
        risk_count = sum(1 for a in self.parent_app.db
                         if any(k in a.get('remark', '') for k in RISK_KEYWORDS))
        self.lbl_stat.setText(
            f"总计 {total} | 待登 {unused_count} | 已用 {used_count} | 风控 {risk_count}"
        )

        accent_color = QColor(T()['accent'])
        for i, acc in enumerate(self.parent_app.db):
            if (keyword and keyword not in acc["user"].lower()
                    and keyword not in acc["remark"].lower()
                    and keyword not in acc["pwd"].lower()):
                continue

            is_current = (i == self.parent_app.current_idx)
            is_risk = any(k in acc.get('remark', '') for k in RISK_KEYWORDS)
            if is_current:
                status = "📍 当前"
            elif is_risk:
                status = "⚠️ 风控"
            elif acc.get("used"):
                status = "✅ 已用"
            else:
                status = "🆕 待登"

            row = self.table.rowCount()
            self.table.insertRow(row)
            cells = [
                QTableWidgetItem(status),
                QTableWidgetItem(acc["user"]),
                QTableWidgetItem(acc["pwd"]),
                QTableWidgetItem(acc["remark"]),
                QTableWidgetItem(format_last_used(acc.get('last_used', ''))),
                QTableWidgetItem(str(i)),
            ]
            for col, item in enumerate(cells):
                if is_current:
                    item.setForeground(QBrush(QColor(accent_color)))
                self.table.setItem(row, col, item)

    def scroll_to_current(self):
        """跳转到当前账号在表格中的位置"""
        # 清空搜索，确保当前行可见
        if self.search_input.text():
            self.search_input.blockSignals(True)
            self.search_input.setText("")
            self.search_input.blockSignals(False)
            self.refresh_table()

        cur = self.parent_app.current_idx
        for row in range(self.table.rowCount()):
            idx_item = self.table.item(row, 5)
            if idx_item and int(idx_item.text()) == cur:
                self.table.selectRow(row)
                self.table.scrollToItem(idx_item, QAbstractItemView.PositionAtCenter)
                return
        self.parent_app.set_status_text("⚠ 当前账号未找到", "#FF8800")

    def on_double_click(self, item):
        real_idx = int(self.table.item(item.row(), 5).text())
        self.parent_app.current_idx = real_idx
        save_config(current_idx=real_idx)
        self.parent_app.update_main_ui()
        self.hide()

    def showEvent(self, event):
        """打开总览时自动定位到当前账号"""
        super().showEvent(event)
        QTimer.singleShot(50, self.scroll_to_current)



# ═══════════════════════════════════════════════════════════════════
# 主窗口
# ═══════════════════════════════════════════════════════════════════

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.is_pinned = True
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 启用鼠标跟踪 -> 用于全局光圈
        self.setMouseTracking(True)

        self.db = load_accounts()
        cfg = load_config()
        self.current_idx = cfg.get("current_idx", 0)
        if self.current_idx >= len(self.db) and len(self.db) > 0:
            self.current_idx = len(self.db) - 1
        elif len(self.db) == 0:
            self.current_idx = 0

        self.is_updating = False
        self.is_mini_mode = False
        self.list_window = None
        self.theme_panel = None
        self.last_invite_code = ""
        self._theme_flash_alpha = 0
        self._is_injecting = False  # 防止注入并发

        # 备注延迟保存
        self._remark_save_timer = QTimer(self)
        self._remark_save_timer.setSingleShot(True)
        self._remark_save_timer.timeout.connect(self._do_save_remark)

        self.resize(740, 640)
        self._is_tracking = False
        self._start_pos = None

        self.particles = create_particle_system(CURRENT_THEME, 740, 640)
        self.effects = GlobalEffectLayer()

        # 注册按钮回调（点击触发粒子）
        ThemedButton.set_effect_callback(self._on_themed_btn_click)
        MegaLaunchButton.set_callbacks(self._on_mega_btn_click, self._on_mega_btn_shockwave)

        # 渲染定时器
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._render_tick)
        self.anim_timer.start(16)

        # 时钟
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)

        # 打字机
        self._typewriter_timer = QTimer(self)
        self._typewriter_timer.timeout.connect(self._typewriter_tick)
        self._full_status = ""
        self._typed_status = ""
        self._typewriter_idx = 0

        # 卡片呼吸
        self._card_breath = 0.0

        self.setup_ui()
        self.apply_qss()
        self.update_main_ui()

        signals.update_status.connect(self.set_status_text)
        signals.ui_refresh.connect(self.update_main_ui)
        signals.trigger_f4.connect(self.execute_f4_injection)
        signals.trigger_f2.connect(self.execute_f2_auto_fetch)
        signals.trigger_f3.connect(self.f3_copy_credentials)
        signals.trigger_mini.connect(self.toggle_mini_mode)
        signals.trigger_home.connect(self.toggle_overview_window)
        signals.token_fetched_manual.connect(self.on_token_fetched_manual)
        signals.token_fetched_auto.connect(self.on_token_fetched_auto)
        signals.theme_changed.connect(self.on_theme_changed)

        self._register_hotkeys_once()

        cfg2 = load_config()
        op = cfg2.get('opacity', 100)
        if op < 100:
            self.setWindowOpacity(op / 100.0)

        if cfg2.get('auto_backup', True):
            backup_accounts()

        try:
            self.setup_tray()
        except Exception:
            self.tray = None

        sc_search = QShortcut(QKeySequence("Ctrl+F"), self)
        sc_search.activated.connect(self.toggle_overview_window)

        self._settings_dlg = None

    # ── 全局效果回调 ───────────────────────────────────────────────
    def _global_pos_to_widget(self, gx, gy):
        local = self.mapFromGlobal(QPointF(gx, gy).toPoint())
        return local.x(), local.y()

    def _on_themed_btn_click(self, gx, gy, color):
        x, y = self._global_pos_to_widget(gx, gy)
        self.effects.burst(x, y, color, count=10)

    def _on_mega_btn_click(self, gx, gy, color, count=24):
        x, y = self._global_pos_to_widget(gx, gy)
        self.effects.burst(x, y, color, count=count)

    def _on_mega_btn_shockwave(self, gx, gy, color):
        x, y = self._global_pos_to_widget(gx, gy)
        self.effects.shockwave(x, y, color, max_radius=400, speed=12, fade=4)

    # ── 热键（一次注册，不再频繁解钩）──────────────────────────────
    def _register_hotkeys_once(self):
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
        try:
            keyboard.add_hotkey('f4', lambda: signals.trigger_f4.emit(), suppress=True)
            keyboard.add_hotkey('f2', lambda: signals.trigger_f2.emit(), suppress=True)
            keyboard.add_hotkey('f3', lambda: signals.trigger_f3.emit(), suppress=True)
            keyboard.add_hotkey('f8', lambda: signals.trigger_mini.emit(), suppress=True)
            keyboard.add_hotkey('home', lambda: signals.trigger_home.emit(), suppress=True)
        except Exception:
            pass

    # ── 渲染循环 ───────────────────────────────────────────────────
    def _render_tick(self):
        self.particles.update(self.width(), self.height())
        self.effects.update()
        self._card_breath += 0.04
        if self._theme_flash_alpha > 0:
            self._theme_flash_alpha = max(0, self._theme_flash_alpha - 8)
        self.update()

    # ── 主题切换 ───────────────────────────────────────────────────
    def on_theme_changed(self):
        self._theme_flash_alpha = 200
        self.particles = create_particle_system(CURRENT_THEME, self.width(), self.height())
        self.apply_qss()
        self.update_main_ui()
        self.lbl_title.setText("🛡️ " + T()['subtitle'])
        # 主题切换冲击波（从主题按钮位置）
        try:
            gp = self.btn_theme.mapToGlobal(QPointF(self.btn_theme.width() / 2,
                                                     self.btn_theme.height() / 2).toPoint())
            x, y = self._global_pos_to_widget(gp.x(), gp.y())
            self.effects.shockwave(x, y, T()['accent'], max_radius=900, speed=15, fade=3)
        except Exception:
            pass
        self.set_status_text(f"✨ 已切换到 {T()['name']} 主题", T()['text_color'])
        if self.list_window:
            self.list_window.on_theme_changed()
        self._update_tray_icon()
        self.update()

    def _update_tray_icon(self):
        if not (hasattr(self, 'tray') and self.tray):
            return
        try:
            pm = QPixmap(64, 64)
            pm.fill(Qt.transparent)
            pmt = QPainter(pm)
            pmt.setRenderHint(QPainter.Antialiasing)
            c = T()['primary']
            grad = QRadialGradient(32, 32, 30)
            grad.setColorAt(0, QColor(c.red(), c.green(), c.blue(), 255))
            grad.setColorAt(1, QColor(c.red() // 2, c.green() // 2, c.blue() // 2, 200))
            pmt.setBrush(QBrush(grad))
            pmt.setPen(QPen(QColor(255, 255, 255, 180), 2))
            pmt.drawEllipse(QPointF(32, 32), 28, 28)
            pmt.setPen(QColor(255, 255, 255))
            pmt.setFont(QFont("Microsoft YaHei", 22, QFont.Bold))
            pmt.drawText(pm.rect(), Qt.AlignCenter, "战")
            pmt.end()
            self.tray.setIcon(QIcon(pm))
            self.setWindowIcon(QIcon(pm))
        except Exception:
            pass

    # ── 绘制 ───────────────────────────────────────────────────────
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        theme = T()
        painter.setBrush(QColor(theme['bg_color']))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 14, 14)
        # 粒子
        self.particles.draw(painter, rect)
        # 全局效果（爆炸粒子+冲击波+鼠标光圈）
        self.effects.draw(painter, rect)
        # 外框
        c1 = theme['primary']; c2 = theme['secondary']
        bg = QLinearGradient(0, 0, rect.width(), rect.height())
        bg.setColorAt(0, QColor(c1.red(), c1.green(), c1.blue(), 130))
        bg.setColorAt(0.5, QColor(c2.red(), c2.green(), c2.blue(), 130))
        bg.setColorAt(1, QColor(c1.red(), c1.green(), c1.blue(), 130))
        painter.setPen(QPen(QBrush(bg), 1.5))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 14, 14)
        self._draw_corners(painter, rect)
        # 主题切换闪光
        if self._theme_flash_alpha > 0:
            theme_c = T()['primary']
            painter.setBrush(QColor(theme_c.red(), theme_c.green(), theme_c.blue(),
                                    self._theme_flash_alpha))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, 14, 14)

    def _draw_corners(self, painter, rect):
        w, h = rect.width(), rect.height()
        theme = T()
        c1 = theme['primary']; c2 = theme['secondary']
        # 角落装饰，加个跑光小点
        run = (math.sin(self._card_breath) + 1) / 2  # 0..1
        painter.setPen(QPen(QColor(c1.red(), c1.green(), c1.blue(), 200), 2))
        painter.drawLine(QPointF(8, 22), QPointF(8, 38))
        painter.drawLine(QPointF(8, 22), QPointF(22, 8))
        painter.drawLine(QPointF(22, 8), QPointF(50, 8))
        painter.drawLine(QPointF(w - 8, 22), QPointF(w - 8, 38))
        painter.drawLine(QPointF(w - 8, 22), QPointF(w - 22, 8))
        painter.drawLine(QPointF(w - 22, 8), QPointF(w - 50, 8))
        painter.setPen(QPen(QColor(c2.red(), c2.green(), c2.blue(), 200), 2))
        painter.drawLine(QPointF(8, h - 22), QPointF(8, h - 38))
        painter.drawLine(QPointF(8, h - 22), QPointF(22, h - 8))
        painter.drawLine(QPointF(22, h - 8), QPointF(50, h - 8))
        painter.drawLine(QPointF(w - 8, h - 22), QPointF(w - 8, h - 38))
        painter.drawLine(QPointF(w - 8, h - 22), QPointF(w - 22, h - 8))
        painter.drawLine(QPointF(w - 22, h - 8), QPointF(w - 50, h - 8))
        # 跑光小点 (沿顶部边)
        painter.setPen(Qt.NoPen)
        spot_x = 50 + (w - 100) * run
        painter.setBrush(QColor(c1.red(), c1.green(), c1.blue(), 220))
        painter.drawEllipse(QPointF(spot_x, 8), 3, 3)
        painter.setBrush(QColor(c2.red(), c2.green(), c2.blue(), 220))
        painter.drawEllipse(QPointF(w - spot_x, h - 8), 3, 3)

    # ── 鼠标 ───────────────────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() < 55:
            self._is_tracking = True
            self._start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_tracking:
            self.move(event.globalPosition().toPoint() - self._start_pos)
        else:
            self.effects.set_mouse(event.position().x(), event.position().y(), True)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._is_tracking = False
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event):
        self.effects.set_mouse(-1000, -1000, False)
        super().leaveEvent(event)

    # ── UI 构建 ────────────────────────────────────────────────────
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 18, 28, 25)
        main_layout.setSpacing(12)

        # 标题栏
        title_bar = QHBoxLayout()
        self.lbl_title = QLabel("🛡️ " + T()['subtitle'])
        title_bar.addWidget(self.lbl_title)
        title_bar.addStretch()

        self.btn_theme = ThemedButton("🎨 主题", 'accent')
        self.btn_theme.setFixedSize(70, 30)
        self.btn_theme.clicked.connect(self.show_theme_picker)
        title_bar.addWidget(self.btn_theme)

        self.btn_settings = ThemedButton("⚙", 'primary')
        self.btn_settings.setFixedSize(34, 30)
        self.btn_settings.clicked.connect(self.show_settings)
        title_bar.addWidget(self.btn_settings)

        self.btn_pin = ThemedButton("📌", 'primary')
        self.btn_pin.setFixedSize(34, 30)
        self.btn_pin.clicked.connect(self.toggle_pin_state)
        title_bar.addWidget(self.btn_pin)

        btn_mini = ThemedButton("⊟", 'primary')
        btn_min = ThemedButton("—", 'primary')
        btn_close = ThemedButton("✕", 'red')
        for btn in (btn_mini, btn_min, btn_close):
            btn.setFixedSize(36, 30)
        btn_mini.clicked.connect(self.toggle_mini_mode)
        btn_min.clicked.connect(self.hide_to_tray)
        btn_close.clicked.connect(self.close)
        title_bar.addWidget(btn_mini)
        title_bar.addWidget(btn_min)
        title_bar.addWidget(btn_close)
        main_layout.addLayout(title_bar)

        # 进度行（包装在容器中以便极简模式隐藏）
        self.header_widget = QWidget()
        header = QHBoxLayout(self.header_widget)
        header.setContentsMargins(0, 8, 0, 8)
        self.lbl_progress_curr = FlipNumberLabel("0")
        self.lbl_progress_curr.setObjectName("ProgCurrent")
        self.lbl_progress_sep = QLabel(" / ")
        self.lbl_progress_sep.setObjectName("ProgSep")
        self.lbl_progress_total = QLabel("0")
        self.lbl_progress_total.setObjectName("ProgTotal")
        self.lbl_badge = QLabel("[READY]")
        self.lbl_badge.setObjectName("StatusBadge")
        header.addWidget(self.lbl_progress_curr)
        header.addWidget(self.lbl_progress_sep)
        header.addWidget(self.lbl_progress_total)
        header.addWidget(self.lbl_badge)
        header.addStretch()

        btn_import = ThemedButton("☁️ 导入", 'secondary')
        btn_import.setFixedHeight(34)
        btn_import.clicked.connect(self.import_workflow)
        header.addWidget(btn_import)

        btn_overview = ThemedButton("📈 总览", 'primary')
        btn_overview.setFixedHeight(34)
        btn_overview.clicked.connect(self.toggle_overview_window)
        header.addWidget(btn_overview)
        main_layout.addWidget(self.header_widget)

        # 卡片
        self.card = QFrame()
        self.card.setObjectName("MainCard")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(10)
        card_grid = QGridLayout()
        card_grid.setVerticalSpacing(12)
        card_grid.setHorizontalSpacing(10)

        self.hideable_widgets = []
        self.shrinkable_buttons = []
        self.mini_hideable_icons_labels = []  # 极简模式隐藏备注/入队码行的图标和标签

        def build_row(row, icon, color, label, readonly, btn_cfgs):
            ibox = ThemedIconBox(icon, color)
            lbl = QLabel(label)
            lbl.setObjectName("RowLabel")
            card_grid.addWidget(ibox, row, 0, Qt.AlignCenter)
            card_grid.addWidget(lbl, row, 1, Qt.AlignLeft | Qt.AlignVCenter)
            if readonly:
                widget = QLineEdit(); widget.setReadOnly(True)
            else:
                widget = ThemedLineEdit()
            widget.setObjectName("RowInput")
            widget.setFixedHeight(38)
            card_grid.addWidget(widget, row, 2)
            box_w = QWidget()
            box = QHBoxLayout(box_w)
            box.setSpacing(6)
            box.setContentsMargins(6, 0, 0, 0)
            for text, scheme, cmd, ic in btn_cfgs:
                b = ThemedButton(f"{ic} {text}" if ic else text, scheme)
                b.setFixedHeight(36)
                b.clicked.connect(cmd)
                box.addWidget(b)
                if row in [3, 4]:
                    self.shrinkable_buttons.append((b, text, ic))
            card_grid.addWidget(box_w, row, 3)
            if row in [0, 1, 2]:
                self.hideable_widgets.extend([ibox, lbl, widget, box_w])
            if row in [3, 4]:
                self.mini_hideable_icons_labels.extend([ibox, lbl])
            return widget

        self.input_user = build_row(0, "👤", "#3B82F6", "账号", True,
            [("复制", "primary", lambda: self.copy_data(self.input_user.text()), "📋")])
        self.input_pwd = build_row(1, "🔒", "#A855F7", "密码", True,
            [("复制", "secondary", lambda: self.copy_data(self.input_pwd.text()), "📋")])
        self.input_token = build_row(2, "🛡️", "#10B981", "安全令", True,
            [("获取", "accent", self.manual_get_token_workflow, "⚡")])
        self.input_remark = build_row(3, "📝", "#F59E0B", "备注", False, [
            ("风控", "orange", lambda: self.input_remark.setText("风控"), "⚠️"),
            ("CNM", "magenta", lambda: self.input_remark.setText("狗鸡巴没有"), "✖"),
            ("清除", "red", lambda: self.input_remark.setText(""), "🗑️")
        ])
        self.input_remark.setPlaceholderText("可选, 添加备注...")
        self.input_remark.textChanged.connect(self.on_remark_changed)
        # 备注栏聚焦时自动切换中文输入法
        self.input_remark.focusInEvent = self._remark_focus_in_event

        self.input_invite = build_row(4, "👥", "#06B6D4", "入队码", False, [
            ("粘贴", "blue", self.paste_invite_logic, "📋"),
            ("复制", "orange", lambda: self.copy_data(self.input_invite.text()), "📋"),
            ("撤回", "green", self.undo_invite_logic, "↩")
        ])
        self.input_invite.setPlaceholderText("输入或粘入入队码...")
        self.input_invite.textChanged.connect(self.auto_extract_invite)

        card_layout.addLayout(card_grid)

        self.lbl_inner_status = QLabel("⟨ 系统就绪 :: 等待指令 ⟩")
        self.lbl_inner_status.setObjectName("InnerStatus")
        self.lbl_inner_status.setAlignment(Qt.AlignCenter)
        self.lbl_inner_status.setFixedHeight(22)
        card_layout.addWidget(self.lbl_inner_status)
        main_layout.addWidget(self.card, stretch=1)

        # 信息栏（包装在容器中以便极简模式隐藏）
        self.info_bar_widget = QWidget()
        info_bar = QHBoxLayout(self.info_bar_widget)
        info_bar.setContentsMargins(2, 0, 2, 0)
        info_bar.setSpacing(15)

        self.lbl_clock = QLabel("--:--:--")
        self.lbl_clock.setObjectName("ClockLabel")
        info_bar.addWidget(self.lbl_clock)

        self.lbl_today_stat = QLabel("今日切号: 0")
        self.lbl_today_stat.setObjectName("StatLabel")
        info_bar.addWidget(self.lbl_today_stat)

        info_bar.addStretch()

        self.lbl_hotkey_hint = QLabel(
            "F4 账密 · F2 安全令 · F3 复制账密 · F8 极简 · Home 总览 · Ctrl+F 搜索"
        )
        self.lbl_hotkey_hint.setObjectName("HotkeyHint")
        info_bar.addWidget(self.lbl_hotkey_hint)
        main_layout.addWidget(self.info_bar_widget)

        # 操作行
        action = QHBoxLayout()
        action.setSpacing(15)
        self.btn_prev = ThemedButton("◀ 上一号", 'primary')
        self.btn_prev.setFixedSize(110, 48)
        self.btn_prev.clicked.connect(self.go_prev)
        action.addWidget(self.btn_prev)
        self.btn_launch = MegaLaunchButton("◎ 一键切号登录 (F4 账密 | F2 安全令)")
        self.btn_launch.setFixedHeight(52)
        self.btn_launch.clicked.connect(self.launch_battlenet_workflow)
        action.addWidget(self.btn_launch, stretch=1)
        self.btn_next = ThemedButton("下一号 ▶", 'secondary')
        self.btn_next.setFixedSize(110, 48)
        self.btn_next.clicked.connect(self.go_next)
        action.addWidget(self.btn_next)
        main_layout.addLayout(action)

    def apply_qss(self):
        theme = T()
        c = theme['primary']; sec = theme['secondary']; acc = theme['accent']
        self.lbl_title.setStyleSheet(f"""
            color: {theme['text_color']};
            font-size: 13px;
            font-weight: bold;
            font-family: {theme['font']};
            letter-spacing: 1px;
        """)
        qss = f"""
        QWidget#MainWindow {{ background-color: transparent; }}
        QWidget {{ font-family: {theme['font']}; }}
        QLabel#ProgCurrent {{
            font-size: 42px;
            color: rgb({c.red()},{c.green()},{c.blue()});
            font-weight: bold; font-family: 'Consolas';
        }}
        QLabel#ProgSep {{
            font-size: 28px;
            color: rgb({sec.red()},{sec.green()},{sec.blue()});
            font-weight: bold; font-family: 'Consolas';
        }}
        QLabel#ProgTotal {{
            font-size: 28px;
            color: rgb({acc.red()},{acc.green()},{acc.blue()});
            font-weight: bold; font-family: 'Consolas';
        }}
        QLabel#StatusBadge {{
            background: rgba({c.red()},{c.green()},{c.blue()},0.15);
            color: {theme['text_color']};
            padding: 5px 16px;
            border-radius: 6px;
            border: 1px solid rgba({c.red()},{c.green()},{c.blue()},0.5);
            font-size: 11px; margin-left: 12px; font-weight: bold;
        }}
        QFrame#MainCard {{
            background: {theme['card_bg']};
            border-radius: 12px;
            border: 1px solid rgba({c.red()},{c.green()},{c.blue()},0.25);
        }}
        QLabel#RowLabel {{
            font-size: 13px; color: {theme['text_color']};
            padding-left: 8px; padding-right: 12px;
            font-weight: bold; letter-spacing: 1px;
        }}
        QLineEdit#RowInput {{
            background: {theme['input_bg']};
            border: 1.5px solid rgba({c.red()},{c.green()},{c.blue()},0.2);
            border-radius: 6px; padding: 8px 14px;
            color: {theme['input_text']}; font-size: 13px;
        }}
        QLineEdit#RowInput:focus {{
            border: 1.5px solid rgb({c.red()},{c.green()},{c.blue()});
        }}
        QLineEdit#RowInput:read-only {{ color: {theme['text_secondary']}; }}
        QLabel#InnerStatus {{
            font-size: 11px; color: {theme['text_color']};
            font-weight: bold; letter-spacing: 1px;
        }}
        QLabel#ClockLabel {{
            color: rgb({c.red()},{c.green()},{c.blue()});
            font-size: 12px; font-weight: bold; font-family: 'Consolas';
            padding: 2px 10px;
            background: rgba({c.red()},{c.green()},{c.blue()},0.10);
            border-radius: 4px;
            border: 1px solid rgba({c.red()},{c.green()},{c.blue()},0.3);
        }}
        QLabel#StatLabel {{
            color: rgb({acc.red()},{acc.green()},{acc.blue()});
            font-size: 11px; font-weight: bold; padding: 2px 10px;
            background: rgba({acc.red()},{acc.green()},{acc.blue()},0.10);
            border-radius: 4px;
            border: 1px solid rgba({acc.red()},{acc.green()},{acc.blue()},0.3);
        }}
        QLabel#HotkeyHint {{
            color: {theme['text_secondary']}; font-size: 10px;
        }}
        """
        self.setStyleSheet(qss)

    # ── 主题选择 ───────────────────────────────────────────────────
    def show_theme_picker(self):
        if self.theme_panel is not None:
            self.theme_panel.deleteLater()
        self.theme_panel = ThemePickerPanel(self)
        btn_pos = self.btn_theme.mapToGlobal(QPointF(0, self.btn_theme.height()).toPoint())
        self.theme_panel.move(btn_pos.x() - 200, btn_pos.y() + 5)
        self.theme_panel.show()

    # ── 状态系统 ───────────────────────────────────────────────────
    def set_status_text(self, text, color=None):
        if color is None:
            color = T()['text_color']
        self._typewriter_timer.stop()
        self._full_status = text
        self._typed_status = ""
        self._typewriter_idx = 0
        self.lbl_inner_status.setStyleSheet(
            f"color: {color}; font-size: 11px; font-weight: bold; letter-spacing: 1px;"
        )
        self._typewriter_timer.start(20)

    def _typewriter_tick(self):
        if self._typewriter_idx < len(self._full_status):
            self._typed_status += self._full_status[self._typewriter_idx]
            self.lbl_inner_status.setText(self._typed_status + "▊")
            self._typewriter_idx += 1
        else:
            self._typewriter_timer.stop()
            self.lbl_inner_status.setText(self._full_status)

    def copy_data(self, text, msg="已复制"):
        if not text:
            return
        QApplication.clipboard().setText(text)
        self.set_status_text(f"✓ {msg}: {text[:15]}...")

    # ── UI 更新 ────────────────────────────────────────────────────
    def update_main_ui(self):
        self.is_updating = True
        if not self.db:
            self.lbl_progress_curr.set_value(0)
            self.lbl_progress_total.setText("0")
            self.lbl_badge.setText("[空]")
            self.input_user.clear()
            self.input_pwd.clear()
            self.input_token.clear()
            self.input_remark.blockSignals(True)
            self.input_remark.clear()
            self.input_remark.blockSignals(False)
        else:
            acc = self.db[self.current_idx]
            self.lbl_progress_curr.set_value(self.current_idx + 1)
            self.lbl_progress_total.setText(str(len(self.db)))
            theme = T()
            c = theme['primary']
            remark = acc.get("remark", "")
            is_risk = any(k in remark for k in RISK_KEYWORDS)
            if is_risk:
                self.lbl_badge.setText("⚠️ 风控")
                self.lbl_badge.setStyleSheet("""
                    background: rgba(239,68,68,0.2);
                    color: #FCA5A5;
                    border: 1px solid rgba(239,68,68,0.6);
                    padding: 5px 16px; border-radius: 6px;
                    font-size: 11px; font-weight: bold;
                """)
            elif acc.get("used"):
                self.lbl_badge.setText("✅ 已用")
                self.lbl_badge.setStyleSheet("""
                    background: rgba(100,100,100,0.15);
                    color: #888;
                    border: 1px solid rgba(100,100,100,0.4);
                    padding: 5px 16px; border-radius: 6px;
                    font-size: 11px; font-weight: bold;
                """)
            else:
                self.lbl_badge.setText("🆕 待登")
                self.lbl_badge.setStyleSheet(f"""
                    background: rgba({c.red()},{c.green()},{c.blue()},0.2);
                    color: {theme['text_color']};
                    border: 1px solid rgba({c.red()},{c.green()},{c.blue()},0.6);
                    padding: 5px 16px; border-radius: 6px;
                    font-size: 11px; font-weight: bold;
                """)
            self.input_user.setText(acc["user"])
            self.input_pwd.setText(acc["pwd"])
            self.input_token.setText("")
            self.input_remark.blockSignals(True)
            self.input_remark.setText(acc["remark"])
            self.input_remark.blockSignals(False)
            self.set_status_text("⟨ 系统就绪 :: F4=账密 | F2=安全令 | F8=极简 | Home=总览 ⟩")
        self.is_updating = False

    # ── 窗口控制 ───────────────────────────────────────────────────
    def toggle_pin_state(self):
        self.is_pinned = not self.is_pinned
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self.is_pinned)
        self.show()
        self.set_status_text("📌 已开启窗口置顶" if self.is_pinned else "📌 已取消窗口置顶")

    def toggle_mini_mode(self):
        self.is_mini_mode = not self.is_mini_mode
        # ── 极简模式：只保留 备注+入队码+上下号+启动OW ──
        # 隐藏账号/密码/安全令行（rows 0,1,2）
        for w in self.hideable_widgets:
            w.setVisible(not self.is_mini_mode)
        # 隐藏备注/入队码行的图标和标签（极简模式下不需要）
        for w in self.mini_hideable_icons_labels:
            w.setVisible(not self.is_mini_mode)
        # 隐藏进度头部（序号/导入/总览按钮）
        self.header_widget.setVisible(not self.is_mini_mode)
        # 隐藏信息栏（时钟/统计/快捷键提示）
        self.info_bar_widget.setVisible(not self.is_mini_mode)
        # 隐藏卡片内状态文本
        self.lbl_inner_status.setVisible(not self.is_mini_mode)
        # 隐藏标题栏中的主题/设置/置顶按钮
        self.btn_theme.setVisible(not self.is_mini_mode)
        self.btn_settings.setVisible(not self.is_mini_mode)
        self.btn_pin.setVisible(not self.is_mini_mode)
        # 备注/入队码行按钮压缩
        for btn, text, icon in self.shrinkable_buttons:
            if self.is_mini_mode:
                btn.setText(icon); btn.setFixedWidth(26); btn.setFixedHeight(24)
            else:
                btn.setText(f"{icon} {text}" if icon else text)
                btn.setFixedWidth(70); btn.setFixedHeight(36)
        if self.is_mini_mode:
            # 压缩标题
            self.lbl_title.setText("⚔ 极简")
            # 压缩卡片内边距
            self.card.layout().setContentsMargins(8, 6, 8, 6)
            self.card.layout().setSpacing(5)
            # 压缩输入框高度
            self.input_remark.setFixedHeight(32)
            self.input_remark.setMinimumWidth(200)
            self.input_invite.setFixedHeight(32)
            self.input_invite.setMinimumWidth(200)
            # 压缩操作行按钮
            self.btn_prev.setFixedSize(58, 34)
            self.btn_prev.setText("◀ 上号")
            self.btn_next.setFixedSize(58, 34)
            self.btn_next.setText("下号 ▶")
            self.btn_launch.setFixedHeight(36)
            self.btn_launch.setText("◎ 登出账号")
            # 压缩主窗口边距
            self.layout().setContentsMargins(8, 6, 8, 8)
            self.layout().setSpacing(5)
            # 极限压缩窗口尺寸（加宽避免输入框文字截断）
            self.setMinimumSize(500, 195)
            self.resize(500, 195)
            self.set_status_text("⚔ 极简战斗模式")
        else:
            # 恢复标题
            self.lbl_title.setText("🛡️ " + T()['subtitle'])
            # 恢复卡片内边距
            self.card.layout().setContentsMargins(20, 18, 20, 18)
            self.card.layout().setSpacing(10)
            # 恢复输入框高度
            self.input_remark.setFixedHeight(38)
            self.input_remark.setMinimumWidth(0)
            self.input_invite.setFixedHeight(38)
            self.input_invite.setMinimumWidth(0)
            # 恢复操作行按钮
            self.btn_prev.setFixedSize(110, 48)
            self.btn_prev.setText("◀ 上一号")
            self.btn_next.setFixedSize(110, 48)
            self.btn_next.setText("下一号 ▶")
            self.btn_launch.setFixedHeight(52)
            self.btn_launch.setText("◎ 一键切号登录 (F4 账密 | F2 安全令)")
            # 恢复主窗口边距
            self.layout().setContentsMargins(28, 18, 28, 25)
            self.layout().setSpacing(12)
            # 恢复窗口尺寸
            self.setMinimumSize(0, 0)
            self.resize(740, 640)
            self.set_status_text("✨ 完全视图已恢复")

    def toggle_overview_window(self):
        if self.list_window is None:
            self.list_window = DataOverviewWindow(self)
            self.list_window.show()
            self.list_window.raise_()
            self.list_window.activateWindow()
        elif self.list_window.isVisible():
            self.list_window.hide()
        else:
            self.list_window.refresh_table()
            self.list_window.show()
            self.list_window.raise_()
            self.list_window.activateWindow()

    # ── 时钟+统计 ──────────────────────────────────────────────────
    def _update_clock(self):
        now = datetime.now()
        weekdays = ['一', '二', '三', '四', '五', '六', '日']
        wd = weekdays[now.weekday()]
        self.lbl_clock.setText(f"⏰ {now.strftime('%H:%M:%S')}  周{wd}")
        self.lbl_today_stat.setText(f"📊 今日切号: {get_today_stat()} 次")

    # ── F3 复制账密 ────────────────────────────────────────────────
    def f3_copy_credentials(self):
        if not self.db:
            return
        acc = self.db[self.current_idx]
        clip_text = f"{acc['user']}\n{acc['pwd']}"
        QApplication.clipboard().setText(clip_text)
        self.set_status_text(
            f"✓ F3: 账号+密码已复制 ({acc['user'][:20]})", T()['accent'].name()
        )

    # ── 设置 ───────────────────────────────────────────────────────
    def show_settings(self):
        if self._settings_dlg is not None:
            self._settings_dlg.deleteLater()
        self._settings_dlg = SettingsDialog(self)
        self._settings_dlg.show()
        self._settings_dlg.raise_()
        self._settings_dlg.activateWindow()

    # ── 系统托盘 ───────────────────────────────────────────────────
    def setup_tray(self):
        pm = QPixmap(64, 64)
        pm.fill(Qt.transparent)
        pmt = QPainter(pm)
        pmt.setRenderHint(QPainter.Antialiasing)
        c = T()['primary']
        grad = QRadialGradient(32, 32, 30)
        grad.setColorAt(0, QColor(c.red(), c.green(), c.blue(), 255))
        grad.setColorAt(1, QColor(c.red() // 2, c.green() // 2, c.blue() // 2, 200))
        pmt.setBrush(QBrush(grad))
        pmt.setPen(QPen(QColor(255, 255, 255, 180), 2))
        pmt.drawEllipse(QPointF(32, 32), 28, 28)
        pmt.setPen(QColor(255, 255, 255))
        pmt.setFont(QFont("Microsoft YaHei", 22, QFont.Bold))
        pmt.drawText(pm.rect(), Qt.AlignCenter, "战")
        pmt.end()
        icon = QIcon(pm)
        self.setWindowIcon(icon)

        self.tray = QSystemTrayIcon(icon, self)
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background: rgba(20,20,35,250);
                color: white;
                border: 1px solid rgba(255,255,255,80);
                border-radius: 8px;
                padding: 6px;
            }
            QMenu::item { padding: 8px 20px; border-radius: 4px; }
            QMenu::item:selected { background: rgba(124,77,255,150); }
        """)
        act_show = QAction("🪟 显示主窗口", self)
        act_show.triggered.connect(self.show_from_tray)
        menu.addAction(act_show)
        act_overview = QAction("📈 数据总览", self)
        act_overview.triggered.connect(self.toggle_overview_window)
        menu.addAction(act_overview)
        menu.addSeparator()
        act_launch = QAction("🚀 启动战网", self)
        act_launch.triggered.connect(self.launch_battlenet_workflow)
        menu.addAction(act_launch)
        menu.addSeparator()
        act_quit = QAction("✕ 退出", self)
        act_quit.triggered.connect(QApplication.quit)
        menu.addAction(act_quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_clicked)
        self.tray.setToolTip("🛡️ 战网管家 - 双击呼出")
        self.tray.show()

    def _tray_clicked(self, reason):
        if reason in (QSystemTrayIcon.DoubleClick, QSystemTrayIcon.Trigger):
            self.show_from_tray()

    def show_from_tray(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.setWindowState(Qt.WindowActive)

    def hide_to_tray(self):
        self.hide()
        if hasattr(self, 'tray') and self.tray:
            self.tray.showMessage(
                "战网管家",
                "已最小化到系统托盘，双击图标可恢复",
                QSystemTrayIcon.Information, 2000
            )

    # ═══════════════════════════════════════════════════════════════
    # F4 / F2 注入（重写：剪贴板法 + IME切英文 + 子线程）
    # ═══════════════════════════════════════════════════════════════
    def execute_f4_injection(self):
        if not self.db or self._is_injecting:
            return
        self._is_injecting = True
        acc = self.db[self.current_idx]
        self.set_status_text(f"⚡ F4触发：键入 {acc['user'][:20]}...")
        # 清焦点（避免注入到本窗口）
        self.clearFocus()
        for w in (self.input_invite, self.input_remark):
            if w.hasFocus():
                w.clearFocus()
        # 子线程执行键入（不切换窗口，用户自行点击目标输入框）
        threading.Thread(target=self._inject_credentials, args=(acc['user'], acc['pwd']),
                         daemon=True).start()

    def _inject_credentials(self, user, pwd):
        """
        通过模拟键盘逐字输入账密到当前焦点输入框（不动剪贴板）。
        不切换窗口，用户需要先点击浏览器账号输入框。
        """
        try:
            # 让 F4 按键完全释放
            time.sleep(0.08)
            # 切英文输入法
            force_english_ime()
            time.sleep(0.05)

            # 账号 - 清空当前框并逐字输入
            clear_focused_input()
            time.sleep(0.03)
            pyautogui.typewrite(user, interval=0.02)
            time.sleep(0.08)
            pyautogui.press('tab')
            time.sleep(0.12)
            # 密码 - 清空当前框并逐字输入
            clear_focused_input()
            time.sleep(0.03)
            pyautogui.typewrite(pwd, interval=0.02)
            time.sleep(0.08)
            pyautogui.press('enter')
            signals.update_status.emit(
                "✓ 账密注入完成！等待安全令页面后按 F2", T()['accent'].name()
            )
        except Exception as e:
            signals.update_status.emit(f"✗ 注入失败: {e}", "#FF3030")
        finally:
            self._is_injecting = False

    def execute_f2_auto_fetch(self):
        if not self.db or self._is_injecting:
            return
        acc = self.db[self.current_idx]
        self.set_status_text("⏳ F2触发：请求安全令...")
        self.clearFocus()
        threading.Thread(target=self._bg_f2, args=(acc['secret'],), daemon=True).start()

    def _bg_f2(self, secret):
        code = get_token_from_api(secret)
        if code and len(code) == 6 and code.isdigit():
            signals.token_fetched_auto.emit(code)
        else:
            signals.update_status.emit(f"✗ 获取失败: {code}", "#FF3030")

    def on_token_fetched_auto(self, code):
        if self._is_injecting:
            return
        self._is_injecting = True
        self.input_token.setText(code)
        threading.Thread(target=self._inject_token, args=(code,), daemon=True).start()

    def _inject_token(self, code):
        """
        通过模拟键盘逐字输入安全令到当前焦点输入框（不动剪贴板）。
        不切换窗口，用户需要先点击浏览器安全令输入框。
        """
        try:
            time.sleep(0.08)
            force_english_ime()
            time.sleep(0.05)
            clear_focused_input()
            time.sleep(0.03)
            pyautogui.typewrite(code, interval=0.02)
            time.sleep(0.08)
            pyautogui.press('enter')
            signals.update_status.emit(f"✓ 安全令 [{code}] 注入成功", T()['accent'].name())
        except Exception as e:
            signals.update_status.emit(f"✗ 注入失败: {e}", "#FF3030")
        finally:
            self._is_injecting = False

    def manual_get_token_workflow(self):
        if not self.db:
            return
        acc = self.db[self.current_idx]
        self.set_status_text("⏳ 请求令牌服务器...")
        threading.Thread(target=self._bg_manual, args=(acc['secret'],), daemon=True).start()

    def _bg_manual(self, secret):
        code = get_token_from_api(secret)
        if code and len(code) == 6 and code.isdigit():
            signals.token_fetched_manual.emit(code)
        else:
            signals.update_status.emit(f"✗ 获取失败: {code}", "#FF3030")

    def on_token_fetched_manual(self, code):
        self.input_token.setText(code)
        QApplication.clipboard().setText(code)
        self.set_status_text(f"🛡️ 安全令 [{code}] 已复制")

    # ═══════════════════════════════════════════════════════════════
    # 备注 / 入队码（debounce 保存 + 简化标志）
    # ═══════════════════════════════════════════════════════════════
    def _remark_focus_in_event(self, event):
        """备注栏聚焦时自动切换到中文输入法"""
        force_chinese_ime()
        # 调用原始 ThemedLineEdit 的 focusInEvent
        ThemedLineEdit.focusInEvent(self.input_remark, event)

    def on_remark_changed(self):
        if self.is_updating or not self.db:
            return
        # 立即更新内存
        self.db[self.current_idx]["remark"] = self.input_remark.text().replace("----", " ")
        # 延迟 300ms 写文件
        self._remark_save_timer.start(300)

    def _do_save_remark(self):
        save_accounts(self.db)
        if self.list_window and self.list_window.isVisible():
            self.list_window.refresh_table()
        # 风控状态可能变化，刷新徽章
        self.update_main_ui()

    def auto_extract_invite(self):
        text = self.input_invite.text()
        if len(text) > 10 and re.search(r'[\u4e00-\u9fa5]', text):
            match = re.search(r'入队码[：:\s]*([A-Za-z0-9]+)', text)
            if match:
                new_text = match.group(1)
            else:
                found = re.findall(r'[A-Za-z0-9]{8,}', text)
                new_text = found[0] if found else text
            if new_text != text:
                self.last_invite_code = text
                self.input_invite.blockSignals(True)
                self.input_invite.setText(new_text)
                self.input_invite.blockSignals(False)

    def paste_invite_logic(self):
        text = QApplication.clipboard().text().strip()
        if not text:
            return
        self.last_invite_code = self.input_invite.text()
        self.input_invite.blockSignals(True)
        self.input_invite.setText(text)
        self.input_invite.blockSignals(False)
        self.auto_extract_invite()
        self.set_status_text("✓ 已粘贴并提取入队码")

    def undo_invite_logic(self):
        self.input_invite.blockSignals(True)
        self.input_invite.setText(self.last_invite_code)
        self.input_invite.blockSignals(False)
        self.set_status_text("✓ 已撤回")

    # ═══════════════════════════════════════════════════════════════
    # 切号
    # ═══════════════════════════════════════════════════════════════
    def go_next(self):
        if not self.db:
            return
        # 标记当前账号已用 + 时间戳
        if not self.db[self.current_idx].get("used"):
            mark_account_used_now(self.db[self.current_idx])
        else:
            # 已用账号也更新时间（重新登录）
            self.db[self.current_idx]['last_used'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        save_accounts(self.db)
        # 每次切号都计数（无论账号是否首次使用）
        increment_today_stat()
        if self.current_idx < len(self.db) - 1:
            self.current_idx += 1
            save_config(current_idx=self.current_idx)
            self.update_main_ui()
        if self.list_window and self.list_window.isVisible():
            self.list_window.refresh_table()

    def go_prev(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            save_config(current_idx=self.current_idx)
            self.update_main_ui()
        if self.list_window and self.list_window.isVisible():
            self.list_window.refresh_table()

    # ═══════════════════════════════════════════════════════════════
    # 导入
    # ═══════════════════════════════════════════════════════════════
    def import_workflow(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择数据", "",
                                              "Text Files (*.txt);;All (*.*)")
        if not path:
            return
        existing = {acc["user"] for acc in self.db}
        new_count = 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    parts = line.split("----CN")[0].split("----")
                    if len(parts) >= 3 and parts[0].strip() not in existing:
                        self.db.append({
                            "user": parts[0].strip(),
                            "pwd": parts[1].strip(),
                            "secret": parts[2].strip(),
                            "remark": parts[3].strip() if len(parts) >= 4 else "",
                            "used": False,
                            "last_used": "",
                        })
                        new_count += 1
            if new_count > 0:
                save_accounts(self.db)
                self.update_main_ui()
                self.set_status_text(f"✓ 导入成功: +{new_count} 新账号")
            else:
                self.set_status_text("⟨ 无新账号 ⟩")
        except Exception as e:
            self.set_status_text(f"✗ 错误: {e}", "#FF3030")

    # ═══════════════════════════════════════════════════════════════
    # 启动战网
    # ═══════════════════════════════════════════════════════════════
    def launch_battlenet_workflow(self):
        # 主线程发出冲击波（按钮点击已触发，这里再补一次大的）
        try:
            self.effects.shockwave(self.width() / 2, self.height() / 2,
                                   T()['accent'], max_radius=600, speed=14, fade=4)
        except Exception:
            pass

        def workflow():
            signals.update_status.emit("⏳ 正在清理战网进程...", T()['accent'].name())
            os.system('taskkill /f /im "Battle.net.exe" /t >nul 2>&1')
            os.system('taskkill /f /im "Agent.exe" /t >nul 2>&1')
            time.sleep(1.0)
            config_dirs = []
            if os.environ.get('APPDATA'):
                config_dirs.append(os.environ.get('APPDATA'))
            if os.environ.get('LOCALAPPDATA'):
                config_dirs.append(os.environ.get('LOCALAPPDATA'))
            modified_any = False
            for root_dir in config_dirs:
                cf = os.path.join(root_dir, 'Battle.net', 'Battle.net.config')
                if os.path.exists(cf):
                    try:
                        with open(cf, 'r', encoding='utf-8') as f:
                            cd = json.load(f)
                        modified = False
                        if "Client" in cd:
                            if "ClientLogin" in cd["Client"]:
                                del cd["Client"]["ClientLogin"]; modified = True
                            if "SavedAccountNames" in cd["Client"]:
                                del cd["Client"]["SavedAccountNames"]; modified = True
                        if modified:
                            with open(cf, 'w', encoding='utf-8') as f:
                                json.dump(cd, f, indent=4)
                            modified_any = True
                    except Exception:
                        pass
            if modified_any:
                signals.update_status.emit("🔥 登录缓存已清除", T()['accent'].name())
                time.sleep(0.3)

            cfg = load_config()
            bnet_path = cfg.get('bnet_path', DEFAULT_BNET_LAUNCHER)
            if not os.path.exists(bnet_path):
                # 尝试默认路径回退
                if os.path.exists(DEFAULT_BNET_LAUNCHER):
                    bnet_path = DEFAULT_BNET_LAUNCHER
                else:
                    signals.update_status.emit(
                        f"✗ 未找到战网路径，请到设置中配置", "#FF3030"
                    )
                    return
            try:
                subprocess.Popen([bnet_path])
                signals.update_status.emit(
                    "✅ 战网已启动！按 F4 开始注入", T()['primary'].name()
                )
            except Exception as e:
                signals.update_status.emit(f"✗ 启动失败: {e}", "#FF3030")

        threading.Thread(target=workflow, daemon=True).start()

    # ═══════════════════════════════════════════════════════════════
    # 关闭事件
    # ═══════════════════════════════════════════════════════════════
    def closeEvent(self, event):
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
        if hasattr(self, 'tray') and self.tray:
            self.tray.hide()
        super().closeEvent(event)


# ═══════════════════════════════════════════════════════════════════
# 程序入口
# ═══════════════════════════════════════════════════════════════════

def main():
    os.environ["QT_LOGGING_RULES"] = "qt.qpa.window=false"

    # Windows DPI
    if sys.platform == 'win32':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass

    # 加载主题配置
    global CURRENT_THEME
    cfg = load_config()
    if 'theme' in cfg and cfg['theme'] in THEMES:
        CURRENT_THEME = cfg['theme']

    app = QApplication(sys.argv)
    font = QFont("Microsoft YaHei", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
