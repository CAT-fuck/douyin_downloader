import os
import sys

# 程序根目录（兼容 PyInstaller）
if getattr(sys, "frozen", False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

os.chdir(base_path)

# 配置文件路径（与exe同级目录）
CONFIG_FILE = os.path.join(base_path, "config.json")
DEFAULT_DIR = os.path.join(base_path, "视频存放处")


def load_config():
    """加载配置，文件不存在或损坏时返回默认值"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return {"download_dir": DEFAULT_DIR}


def save_config(download_dir):
    """保存配置（保留已有字段不被覆盖）"""
    try:
        existing = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing["download_dir"] = download_dir
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
    except IOError as e:
        pass


def ensure_dir(path):
    """目录不存在则自动创建"""
    os.makedirs(path, exist_ok=True)
    return path


def retry(max_attempts=3, delay=1.5):
    """重试装饰器：网络操作失败时自动重试"""
    import functools
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        print(f"第{attempt}次尝试失败: {e}，{delay}秒后重试...")
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator


os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(base_path, "ms-playwright")

import subprocess
import time
import threading
import requests
import json
import shutil
from PyQt5.QtGui import QTextBlockFormat, QTextCursor
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QTextEdit, QTextBrowser, QFileDialog, QVBoxLayout, QStackedLayout, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtCore import QTimer
from playwright.sync_api import sync_playwright
from datetime import datetime


class DouyinDownloader(QWidget):

    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finish_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Douyin Downloader")
        self.resize(600, 480)

        # 加载配置
        self.config = load_config()

        # 栈布局：协议页和主页面
        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.folder = self.config.get("download_dir", os.getcwd())

        # 检查协议是否已接受
        self.agreement_accepted = self.config.get("agreement_accepted", False)

        # 默认显示协议页
        self.create_agreement_page()
        self.create_main_page()

        if self.agreement_accepted:
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

        self.log_signal.connect(self.write)
        self.finish_signal.connect(self._on_download_finished)

    def _on_download_finished(self):
        self.start_btn.setEnabled(True)
        # 下载完成后自动打开下载文件夹（显示三个文件）
        if hasattr(self, 'download_subdir'):
            self._open_download_folder(self.download_subdir)
        # 恢复下载目录
        if hasattr(self, '_old_folder'):
            self.folder = self._old_folder

# ---------------- 协议页 ----------------
    def create_agreement_page(self):

        page = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # ===== 标题 =====
        title = QLabel("用户协议")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size:26px; font-weight:bold; margin-bottom:10px;"
        )
        layout.addWidget(title)

        # ===== 文本框 =====
        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setReadOnly(True)
        text.setLineWrapMode(QTextBrowser.WidgetWidth)

        text.setStyleSheet("""
            QTextBrowser {
                border: 2px solid #2aa198;
                border-radius: 8px;
                padding: 8px;
                background-color: #fefefe;
            }
        """)
        hint = QLabel("请滚动到底部以启用同意按钮!")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)

        # ===== 协议内容 =====
        agreement_text = [
            {"type": "title", "text": "使用条款"},

            {"type": "para", "text": "抖音平台高度重视知识产权保护，尊重原创，鼓励用户创作有价值的作品。为此，平台一方面保障用户对自己作品享有的知识产权，另一方面也严格要求用户不应上传侵犯他人知识产权的作品。如果用户在平台上传侵犯他人知识产权的内容，抖音平台将根据相关法律法规要求进行处理。"},

            {"type": "para", "text": "抖音平台禁止发布、传播以下侵犯他人知识产权的内容或实施以下侵犯他人知识产权的行为："},

            {"type": "para", "text": "未经许可，非法使用他人拥有知识产权的内容，包括但不限于文字作品、影音作品、商标等；"},
            {"type": "para", "text": "冒用他人名义发布他人拥有知识产权的内容；"},
            {"type": "para", "text": "其他任何侵犯第三方知识产权等合法权益的行为；"},

            {"type": "para", "text": "用户在抖音平台上发布的所有原创内容和信息都归用户所有，用户可以通过隐私和应用设置控制这些内容和信息的分享方式。但是用户在分享内容之前，须确保拥有发布和分享这些内容的权利，不能侵犯他人合法享有的著作权、商标权等合法权益。"},

            {"type": "para", "text": "详细规则请见:"},
            {"type": "link", "text": "https://www.douyin.com/rule/policy?activeId=self_decipline#heading-9"},


            {"type": "para", "text": "中国民法典对网络侵权行为有系统规定，核心条款集中在第七编“侵权责任”中，明确了责任主体、构成要件、权利救济路径及平台义务等关键内容。"},

            {"type": "para", "text": "盗窃视频行为的法律分析文献综述"},
            {"type": "para", "text": "一、行为定性与法律依据"},
            {"type": "para", "text": "核心法律条款："},

            {"type": "para", "text": "《刑法》第二百一十七条：以营利为目的，未经著作权人许可复制、发行或通过信息网络传播视听作品，违法所得数额较大或有其他严重情节的，构成侵犯著作权罪。"},

            {"type": "para", "text": "《民法典》第一千一百六十五条：行为人因过错侵害他人民事权益造成损害的，应承担侵权责任。"},

            {"type": "para", "text": "《治安管理处罚法》第四十二条：偷拍、散布他人隐私的，处五日以下拘留或五百元以下罚款；情节较重的，处五日以上十日以下拘留。"},

            {"type": "para", "text": "行为分类："},
            {"type": "para", "text": "营利性盗摄：如影院屏摄后传播牟利，直接触犯刑法。"},
            {"type": "para", "text": "非营利性侵权：如个人录制电影片段上传社交平台，可能构成民事侵权。"},

            {"type": "para", "text": "二、刑事责任与量刑标准"},
            {"type": "para", "text": "入罪条件："},
            {"type": "para", "text": "违法所得数额较大（通常为一千元至三千元以上）或存在多次盗窃、入户盗窃等加重情节。"},

            {"type": "para", "text": "情节严重时（如涉及国家秘密、商业秘密），可能构成更严重的犯罪。"},

            {"type": "para", "text": "量刑幅度："},
            {"type": "para", "text": "数额较大：处三年以下有期徒刑、拘役或管制，并处或单处罚金。"},
            {"type": "para", "text": "数额巨大（三万元以上）：处三年以上十年以下有期徒刑，并处罚金。"},
            {"type": "para", "text": "数额特别巨大（三十万元以上）：处十年以上有期徒刑或无期徒刑，并处罚金或没收财产。"},

            {"type": "para", "text": "三、民事责任与权利救济"},
            {"type": "para", "text": "被侵权人权利："},
            {"type": "para", "text": "根据《民法典》第一千一百六十七条，可要求侵权人承担停止侵害、赔偿损失、赔礼道歉等责任。"},

            {"type": "para", "text": "平台连带责任："},
            {"type": "para", "text": "网络服务提供者若未及时采取删除措施，需对损害扩大部分承担连带责任。"},

            {"type": "para", "text": "四、研究趋势与实务建议"},
            {"type": "para", "text": "立法完善方向："},
            {"type": "para", "text": "明确“合理使用”边界，如个人学习、研究目的的小范围使用可免责。"},
            {"type": "para", "text": "建立视频内容审核机制，避免因用户上传侵权内容而承担连带责任。"},
        ]

        cursor = text.textCursor()
        cursor.movePosition(QTextCursor.Start)

        for block in agreement_text:
            block_format = QTextBlockFormat()

            if block["type"] == "title":
                block_format.setAlignment(Qt.AlignCenter)
                cursor.setBlockFormat(block_format)
                cursor.insertHtml(f'<span style="font-weight:bold; font-size:18pt;">{block["text"]}</span>')
                cursor.insertBlock()
                cursor.insertBlock()

            elif block["type"] == "para":
                block_format.setAlignment(Qt.AlignLeft)

                if block["text"].startswith(("一、", "二、", "三、", "四、")) or block["text"].endswith("："):
                    cursor.setBlockFormat(block_format)
                else:
                    block_format.setTextIndent(20)
                    cursor.setBlockFormat(block_format)

                if block["text"].startswith(("一、", "二、", "三、", "四、")):
                    cursor.insertHtml(f'<span style="font-weight:bold; font-size:12pt;">{block["text"]}</span>')
                elif block["text"].endswith("："):
                    cursor.insertHtml(f'<span style="font-weight:bold; font-size:11pt;">{block["text"]}</span>')
                elif block["text"].startswith("《"):
                    cursor.insertHtml(f'<span style="font-size:10pt; color:#333;">{block["text"]}</span>')
                else:
                    cursor.insertHtml(f'<span style="font-size:10pt;">{block["text"]}</span>')

                cursor.insertBlock()
                cursor.insertBlock()

            elif block["type"] == "link":
                block_format.setAlignment(Qt.AlignLeft)
                block_format.setTextIndent(20)
                cursor.setBlockFormat(block_format)
                cursor.insertHtml(f'<a href="{block["text"]}" style="font-size:10pt; color:#2aa198;">{block["text"]}</a>')
                cursor.insertBlock()
                cursor.insertBlock()

        layout.addWidget(text)

        # 等布局完成再滚动到顶部
        QTimer.singleShot(0, lambda: text.verticalScrollBar().setValue(0))

        # ===== 同意按钮 =====
        btn = QPushButton("我知晓，我同意")
        btn.setEnabled(False)
        btn.setMinimumHeight(36)

        layout.addWidget(btn)

        # ===== 滚动到底才允许点击 =====
        def check_scroll():
            bar = text.verticalScrollBar()
            if bar.value() == bar.maximum():
                btn.setEnabled(True)

        text.verticalScrollBar().valueChanged.connect(check_scroll)

        # ===== "不再提醒"复选框 =====
        checkbox = QCheckBox("不再提醒此协议")
        checkbox.setStyleSheet("font-size: 11px; color: #2aa198;")
        layout.addWidget(checkbox)
        # ===== 点击进入主界面 =====
        def on_agree():
            # 保存协议接受状态
            if checkbox.isChecked():
                self.config["agreement_accepted"] = True
                try:
                    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                        json.dump(self.config, f, ensure_ascii=False, indent=2)
                except IOError:
                    pass
            self.stack.setCurrentIndex(1)
        btn.clicked.connect(on_agree)

        page.setLayout(layout)
        self.stack.addWidget(page)

    # ---------------- 主界面 ----------------
    def create_main_page(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        logo = QLabel("""
██████╗  ██████╗ ██╗   ██╗██╗   ██╗██╗███╗   ██╗
██╔══██╗██╔═══██╗██║   ██║╚██╗ ██╔╝██║████╗  ██║
██║  ██║██║   ██║██║   ██║ ╚████╔╝ ██║██╔██╗ ██║
██║  ██║██║   ██║██║   ██║  ╚██╔╝  ██║██║╚██╗██║
██████╔╝╚██████╔╝╚██████╔╝   ██║   ██║██║ ╚████║
╚═════╝  ╚═════╝  ╚═════╝    ╚═╝   ╚═╝╚═╝  ╚═══╝

⚡ Douyin Video Downloader ⚡
作者：CAT是猫不是喵  BUG反馈：catmiao14514@163.com (小兽太也可以通过这个邮箱找我扩列哦🐾)
""")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            QLabel{
                color: #2aa198;
                font-family: Consolas;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        layout.addWidget(logo)

        self.label = QLabel("请输入抖音视频链接喵～")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.name_label = QLabel("视频名称(可选):")
        self.name_label.setStyleSheet("font-size: 12px; color: #2aa198;")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("不填则按当前日期命名")
        layout.addWidget(self.name_input)

        self.folder_btn = QPushButton("选择保存文件夹(当前默认保存路径是: " + self.folder + ")")
        layout.addWidget(self.folder_btn)

        self.open_folder_btn = QPushButton("打开用来保存下载视频的文件夹")
        layout.addWidget(self.open_folder_btn)

        self.start_btn = QPushButton("让修猫立刻下载!")
        layout.addWidget(self.start_btn)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2aa198;
                border-radius: 8px;
                padding: 5px;
                background-color: #fefefe;
            }
        """)

        # 下载进度条
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFormat("修猫正在搬运视频… %p%")
        layout.addWidget(self.progress)

        self.progress_signal.connect(self.progress.setValue)

        layout.addWidget(self.log)

        main_widget.setLayout(layout)
        self.stack.addWidget(main_widget)

        # 绑定事件
        self.folder_btn.clicked.connect(self.choose_folder)
        self.open_folder_btn.clicked.connect(self.open_save_folder)
        self.start_btn.clicked.connect(self.start_download)

    # ---------------- 工具函数 ----------------
    def write(self, text):
        self.log.append(text)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹(默认保存路径)", self.folder)
        if folder:
            self.folder = folder
            save_config(folder)
            self.write("保存路径: " + folder)

    def open_save_folder(self):
        """打开保存文件夹（资源管理器）"""
        import subprocess
        folder = self.folder
        if os.path.exists(folder):
            try:
                subprocess.Popen(['explorer', folder])
                self.write("已打开文件夹: " + folder)
            except Exception as e:
                self.write("打开文件夹失败: " + str(e))
        else:
            self.write("文件夹不存在: " + folder + "，请先选择保存文件夹喵!")

    def _open_download_folder(self, folder_path):
        """下载完成后自动打开下载子文件夹"""
        import subprocess
        if os.path.exists(folder_path):
            try:
                subprocess.Popen(['explorer', folder_path])
                self.write("下载完成，已自动打开文件夹: " + folder_path)
            except Exception as e:
                self.write("自动打开文件夹失败: " + str(e))
        else:
            self.write("下载文件夹不存在: " + folder_path)

    def normalize_url(self, url):
        if "/video/" in url:
            return url
        if "modal_id=" in url:
            vid = url.split("modal_id=")[1].split("&")[0]
            return f"https://www.douyin.com/video/{vid}"
        try:
            r = requests.get(url, allow_redirects=True, timeout=10)
            final = r.url
            if "/video/" in final:
                return final
            if "modal_id=" in final:
                vid = final.split("modal_id=")[1].split("&")[0]
                return f"https://www.douyin.com/video/{vid}"
        except:
            pass
        return None

    def get_headers(self, page):
        cookies = page.context.cookies()
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        return {
            "User-Agent": page.evaluate("navigator.userAgent"),
            "Referer": "https://www.douyin.com/",
            "Cookie": cookie_str
        }

    @retry(max_attempts=3, delay=1.5)
    def download_file(self, url, name, page, start=0, end=100):

        self.progress_signal.emit(0)

        headers = self.get_headers(page)
        r = requests.get(url, headers=headers, stream=True, timeout=30)
        r.raise_for_status()

        path = os.path.join(self.folder, name)

        total = int(r.headers.get('Content-Length', 0))
        downloaded = 0
        last = -1

        if total == 0:
            self.progress_signal.emit(0)

        with open(path, "wb") as f:
            for chunk in r.iter_content(1024 * 32):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total > 0:
                        percent = start + int(downloaded / total * (end - start))
                        if percent != last:
                            self.progress_signal.emit(percent)
                            last = percent

        self.log_signal.emit("\n下载完成喵～: \n" + path)

        self.progress_signal.emit(100)
        time.sleep(0.3)
        self.progress_signal.emit(0)

        return path

    # ===================== V1.1.4 新增：FFmpeg 诊断与合并 =====================
    def check_ffmpeg_health(self, ffmpeg_path):
        """检查 FFmpeg 是否可正常运行"""
        self.log_signal.emit("\n===== FFmpeg 健康检查 =====")
        self.log_signal.emit(f"ffmpeg.exe 路径: {ffmpeg_path}")
        self.log_signal.emit(f"文件存在: {os.path.exists(ffmpeg_path)}")
        if os.path.exists(ffmpeg_path):
            self.log_signal.emit(f"文件大小: {os.path.getsize(ffmpeg_path)} 字节")
            # 检查文件头（判断是否是有效可执行文件）
            with open(ffmpeg_path, "rb") as f:
                header = f.read(4)
            self.log_signal.emit(f"文件头(HEX): {header.hex()}")
            if header[:2] == b"MZ":
                self.log_signal.emit("文件头确认: Windows PE 可执行文件 (MZ)")
            else:
                self.log_signal.emit("警告: 文件头不是 MZ，可能不是有效的 Windows 可执行文件喵!")

        # 尝试运行 ffmpeg --version
        try:
            result = subprocess.run(
                [ffmpeg_path, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                cwd=base_path
            )
            if result.returncode == 0:
                version_info = result.stdout.decode("utf-8", errors="replace")
                self.log_signal.emit(f"FFmpeg 版本检查通过:\n{version_info[:500]}")
                return True
            else:
                stderr_raw = result.stderr
                stderr_str = stderr_raw.decode("utf-8", errors="replace") if stderr_raw else "(空)"
                self.log_signal.emit(f"FFmpeg --version 返回码: {result.returncode}")
                self.log_signal.emit(f"FFmpeg stderr: {stderr_str}")
                return False
        except subprocess.TimeoutExpired:
            self.log_signal.emit("FFmpeg --version 超时喵!")
            return False
        except Exception as e:
            self.log_signal.emit(f"FFmpeg --version 异常: {e}")
            return False

    def get_file_type(self, filepath):
        """通过文件头判断实际文件类型"""
        try:
            with open(filepath, "rb") as f:
                header = f.read(16)
            if header[:4] == b"\x00\x00\x00\x18" or header[:4] == b"ftyp":
                return "MP4"
            elif header[:4] == b"\x00\x00\x01\x00" or header[:3] == b"\x00\x00\x01":
                return "H.264/ES"
            elif header[:4] == b"ID3" or header[:4] == b"\xff\xfb":
                return "MP3/Audio"
            elif header[:4] == b"RIFF":
                return "AVI"
            elif header[:8] == b"\x1a\x45\xdf\xa3" or header[:4] == b"\x1a\x45\xdf\xa3":
                return "WebM"
            elif header[:4] == b"\x7f" + b"ELF":
                return "ELF(Linux)"
            elif header[:2] == b"MZ":
                return "DOS/Windows EXE"
            else:
                return f"未知(头:{header[:8].hex()})"
        except Exception as e:
            return f"读取失败: {e}"

    def merge_with_ffmpeg_v2(self, ffmpeg_path, video_file, audio_file, out_file):
        """V1.1.4 改进版合并：先诊断再合并，多种降级策略"""

        # 0. 健康检查
        if not self.check_ffmpeg_health(ffmpeg_path):
            self.log_signal.emit("FFmpeg 无法正常运行，修猫正在尝试备用方案...")
            return False

        # 0.5. 检查文件类型
        v_type = self.get_file_type(video_file)
        a_type = self.get_file_type(audio_file) if audio_file else "N/A"
        self.log_signal.emit(f"视频文件类型: {v_type} ({os.path.getsize(video_file)} bytes)")
        if audio_file:
            self.log_signal.emit(f"音频文件类型: {a_type} ({os.path.getsize(audio_file)} bytes)")

        # 1. 先尝试用 ffprobe 探测视频信息
        try:
            probe_result = subprocess.run(
                [ffmpeg_path, "-hide_banner", "-i", video_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                cwd=base_path
            )
            probe_stderr = probe_result.stderr.decode("utf-8", errors="replace") if probe_result.stderr else ""
            if probe_stderr:
                self.log_signal.emit(f"ffprobe探测视频信息:\n{probe_stderr[:800]}")
        except Exception as e:
            self.log_signal.emit(f"ffprobe探测失败: {e}")

        # 2. 打印完整命令供调试
        self.log_signal.emit(f"\n输出文件路径: {out_file}")
        self.log_signal.emit(f"视频文件: {video_file}")
        if audio_file:
            self.log_signal.emit(f"音频文件: {audio_file}")

        # 策略列表（按优先级从高到低）
        # 注意：抖音下载的视频文件本身已包含音频流，所以最直接的方式就是复制原文件
        strategies = [
            ("直接复制视频文件(自带音频)", [
                ffmpeg_path, "-y", "-i", video_file, "-c", "copy", out_file
            ]),
            ("流复制(copy)", [
                ffmpeg_path, "-y",
                "-i", video_file,
                "-i", audio_file if audio_file else video_file,
                "-c:v", "copy",
                "-c:a", "copy",
                "-map", "0:v:0",
                "-map", ("1:a:0" if audio_file else "0:v:0"),
                out_file
            ]),
            ("重新编码(libx264+aac)", [
                ffmpeg_path, "-y",
                "-i", video_file,
                "-i", audio_file if audio_file else video_file,
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                "-map", "0:v:0",
                "-map", ("1:a:0" if audio_file else "0:v:0"),
                out_file
            ]),
            ("自动流选择(最简命令)", [
                ffmpeg_path, "-y",
                "-i", video_file,
                "-i", audio_file if audio_file else video_file,
                out_file
            ]),
            ("仅复制视频流(跳过音频)", [
                ffmpeg_path, "-y",
                "-i", video_file,
                "-c:v", "copy",
                out_file
            ]),
        ]

        for strategy_name, cmd in strategies:
            if getattr(self, '_stop_flag', False):
                return False
            self.log_signal.emit(f"\n尝试合并策略: {strategy_name}...")
            self.log_signal.emit(f"命令: {' '.join(cmd)}")

            try:
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=120,
                    cwd=base_path
                )
                if result.returncode == 0:
                    self.log_signal.emit(f"合并成功(策略: {strategy_name}): {out_file}")
                    # 保留临时文件并重命名为可识别名称（不删除）
                    for fpath in [video_file, audio_file]:
                        if fpath and os.path.exists(fpath):
                            try:
                                if fpath.endswith('.mp4'):
                                    new_name = fpath.replace('.mp4', '_视频流.mp4')
                                elif fpath.endswith('.mp3'):
                                    new_name = fpath.replace('.mp3', '_音频流.mp3')
                                else:
                                    new_name = fpath + '_原始'
                                if os.path.exists(new_name):
                                    os.remove(new_name)
                                os.rename(fpath, new_name)
                                self.log_signal.emit(f"保留文件: {os.path.basename(new_name)}")
                            except Exception:
                                pass
                    return True
                else:
                    # 用 replace 避免编码错误
                    stderr_str = result.stderr.decode("utf-8", errors="replace") if result.stderr else "(空)"
                    stdout_str = result.stdout.decode("utf-8", errors="replace") if result.stdout else "(空)"
                    self.log_signal.emit(f"策略[{strategy_name}]失败, 返回码: {result.returncode}")
                    if stderr_str.strip():
                        self.log_signal.emit(f"FFmpeg stderr: {stderr_str}")
                    if stdout_str.strip():
                        self.log_signal.emit(f"FFmpeg stdout: {stdout_str}")
            except subprocess.TimeoutExpired:
                self.log_signal.emit(f"策略[{strategy_name}]超时")
            except FileNotFoundError:
                self.log_signal.emit("错误: ffmpeg.exe 文件不存在或无法执行，请检查路径是否正确喵～")
                return False
            except Exception as e:
                self.log_signal.emit(f"策略[{strategy_name}]异常: {type(e).__name__}: {e}")

        # 所有策略失败，返回视频文件路径让用户知道至少视频下载成功了
        self.log_signal.emit("\n所有合并策略均失败")
        self.log_signal.emit(f"视频文件(未合并，但可直接播放): {video_file}")
        if audio_file:
            self.log_signal.emit(f"音频文件: {audio_file}")
        self.log_signal.emit("\n提示: 下载的视频文件本身已包含音频，可以直接用播放器打开视频文件观看喵～")
        return False

    # ---------------- 下载逻辑 ----------------
    def start_download(self):
        self.start_btn.setEnabled(False)
        video_input = self.url_input.text().strip()
        if not video_input:
            self.write("\n请输入链接喵～")
            self.start_btn.setEnabled(True)
            return
        video_page = self.normalize_url(video_input)
        if not video_page:
            self.write("\n无法解析链接喵～ 请检查链接是否正确哦!")
            self.start_btn.setEnabled(True)
            return

        # 获取自定义名称
        custom_name = self.name_input.text().strip()
        # 清理文件名中的非法字符
        illegal_chars = r'\/*?:"<>|,'
        if custom_name:
            clean_name = ''.join(c for c in custom_name if c not in illegal_chars)
            folder_name = clean_name
            self.file_prefix = clean_name
        else:
            folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.file_prefix = folder_name

        # 防止同名覆盖：如果文件夹已存在，自动加 _1 _2 后缀
        original_folder_name = folder_name
        counter = 1
        self.download_subdir = os.path.join(self.folder, folder_name)
        while os.path.exists(self.download_subdir):
            folder_name = f"{original_folder_name}_{counter}"
            self.download_subdir = os.path.join(self.folder, folder_name)
            counter += 1
            # 防止极端情况（文件夹名被手动创建到几千），加个上限
            if counter > 999:
                raise Exception("下载文件夹名称冲突过多，请检查保存目录喵!")

        # 创建子文件夹
        ensure_dir(self.download_subdir)
        
        # 如果因为重名自动加了后缀，提醒用户
        if folder_name != original_folder_name:
            self.write(f"注意: 文件夹 '{original_folder_name}' 已存在，自动重命名为 '{folder_name}'")

        # 临时切换下载目录到子文件夹
        self._old_folder = self.folder
        self.folder = self.download_subdir

        self.write("\n下载文件夹: " + self.download_subdir)
        self.write("\n解析后链接: " + video_page)
        threading.Thread(target=self.run, args=(video_page,), daemon=True).start()

    def run(self, video_page):
        browser = None
        try:
            # 查找 chromium 路径（兼容不同版本）
            ms_playwright_dir = os.path.join(base_path, "ms-playwright")
            chromium_path = None
            if os.path.exists(ms_playwright_dir):
                chromium_dirs = [d for d in os.listdir(ms_playwright_dir)
                                if d.startswith("chromium-") and os.path.isdir(os.path.join(ms_playwright_dir, d))]
                if chromium_dirs:
                    chromium_dirs.sort(key=lambda x: int(x.split("-")[1]) if x.split("-")[1].isdigit() else 0, reverse=True)
                    chromium_dir = os.path.join(ms_playwright_dir, chromium_dirs[0])
                    chrome_exe = os.path.join(chromium_dir, "chrome-win64", "chrome.exe")
                    if os.path.exists(chrome_exe):
                        chromium_path = chrome_exe

            if chromium_path is None:
                chromium_path = os.path.join(
                    base_path,
                    "ms-playwright",
                    "chromium-1208",
                    "chrome-win64",
                    "chrome.exe"
                )

            # ffmpeg 路径
            ffmpeg_path = os.path.join(base_path, "ffmpeg.exe")

            with sync_playwright() as p:

                browser = p.chromium.launch(
                    executable_path=chromium_path,
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-infobars",
                        "--start-maximized"
                    ]
                )

                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; Win64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
                    viewport={"width": 1280, "height": 800}
                )

                page = context.new_page()

                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """)

                found = {"ok": False}
                video_url = [None]
                audio_url = [None]

                def handle_response(resp):
                    try:
                        if found["ok"]:
                            return

                        if "aweme/v1/web/aweme/detail" in resp.url:
                            found["ok"] = True

                            data = resp.json()
                            detail = data.get("aweme_detail", {})
                            video = detail.get("video", {})

                            # 安全获取视频URL
                            v_url = None
                            play_addr = video.get("play_addr", {})
                            if play_addr and play_addr.get("url_list"):
                                v_url = play_addr["url_list"][0]
                            else:
                                download_addr = video.get("download_addr", {})
                                if download_addr and download_addr.get("url_list"):
                                    v_url = download_addr["url_list"][0]

                            video_url[0] = v_url

                            # 安全获取音频URL
                            a_url = None
                            music = detail.get("music", {})
                            music_play = music.get("play_url", {})
                            if music_play and music_play.get("url_list"):
                                a_url = music_play["url_list"][0]
                            audio_url[0] = a_url

                            self.log_signal.emit("\n视频地址:")
                            self.log_signal.emit(str(v_url))
                            self.log_signal.emit("\n音频地址:")
                            self.log_signal.emit(str(a_url))
                            self.log_signal.emit("\n")

                            if not v_url:
                                self.log_signal.emit("错误: 修猫并没有找到视频地址!竟敢耍本喵!")
                                return

                            # 使用自定义名称或日期作为文件名前缀
                            prefix = getattr(self, 'file_prefix', datetime.now().strftime("%Y%m%d_%H%M%S"))

                            self.log_signal.emit("开始下载视频流...")
                            video_file = self.download_file(v_url, f"video_{prefix}.mp4", page, 0, 50)
                            self.log_signal.emit("开始下载音频流...")

                            if a_url:
                                audio_file = self.download_file(a_url, f"audio_{prefix}.mp3", page, 50, 100)
                            else:
                                self.log_signal.emit("无音频流，仅保存视频喵!")
                                audio_file = None

                            # 检查文件完整性
                            file_ok = True
                            for name, fpath in [("视频", video_file), ("音频", audio_file)]:
                                if fpath and os.path.exists(fpath):
                                    size = os.path.getsize(fpath)
                                    self.log_signal.emit(f"{name}文件大小: {size} 字节")
                                    if size == 0:
                                        self.log_signal.emit(f"合并失败: {name}文件为0字节")
                                        file_ok = False
                                elif fpath is None:
                                    pass
                                else:
                                    self.log_signal.emit(f"合并失败: {name}文件不存在: {fpath}")
                                    file_ok = False
                                    break

                            if file_ok:
                                out_file = os.path.join(self.folder, f"__merge_tmp_{prefix}.mp4")

                                if os.path.exists(ffmpeg_path):
                                    # 使用 V1.1.4 改进版合并
                                    success = self.merge_with_ffmpeg_v2(ffmpeg_path, video_file, audio_file, out_file)
                                    if success:
                                        # 合并成功 - 重命名合并输出文件
                                        final_name = f"video_{prefix}.mp4"
                                        final_path = os.path.join(self.folder, final_name)
                                        if os.path.exists(out_file):
                                            if os.path.exists(final_path):
                                                os.remove(final_path)
                                            os.replace(out_file, final_path)
                                            self.log_signal.emit("合并完成: " + final_path)
                                        else:
                                            self.log_signal.emit("最终文件: " + out_file)
                                        # 列出文件夹中所有文件
                                        files_in_dir = os.listdir(self.folder)
                                        self.log_signal.emit("\n下载文件夹中的文件:")
                                        for f in files_in_dir:
                                            fpath = os.path.join(self.folder, f)
                                            if os.path.isfile(fpath):
                                                size = os.path.getsize(fpath)
                                                self.log_signal.emit(f"  {f} ({size} 字节)")
                                    else:
                                        self.log_signal.emit("FFmpeg合并失败，请查看上方错误信息喵!")
                                        self.log_signal.emit(f"视频路径: {video_file}")
                                        if audio_file:
                                            self.log_signal.emit(f"音频路径: {audio_file}")
                                else:
                                    self.log_signal.emit("合并失败: 未找到 ffmpeg.exe")
                                    self.log_signal.emit(f"视频文件(未合并): {video_file}")

                    except Exception as e:
                        self.log_signal.emit("解析异常: " + str(e))

                page.on("response", handle_response)

                self.log_signal.emit("\n正在打开页面喵～")
                page.goto(video_page)
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000)

                # 模拟点击播放
                page.mouse.click(640, 360)

                # 等待API响应
                timeout = time.time() + 30
                while not found["ok"] and time.time() < timeout:
                    time.sleep(0.2)

                if not found["ok"]:
                    self.log_signal.emit("超时: 未获取到视频信息喵!真的不是修猫笨!呜呜呜～")
                else:
                    # 等待下载线程完成
                    time.sleep(2)
                    # 再等一会儿确保文件写入完成
                    time.sleep(1)

        except Exception as e:
            self.log_signal.emit("错误: " + str(e))
        finally:
            if browser:
                try:
                    browser.close()
                except Exception:
                    pass

        self.finish_signal.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DouyinDownloader()
    win.show()
    sys.exit(app.exec_())
