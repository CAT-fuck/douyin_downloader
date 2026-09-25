import sys
import os
import time
import threading
import requests
import subprocess
import shutil
from PyQt5.QtGui import QTextBlockFormat, QTextCursor
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QTextEdit, QTextBrowser, QFileDialog, QVBoxLayout, QStackedLayout
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

        # 栈布局：协议页和主页面
        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.folder = os.getcwd()

        # 默认显示协议页
        self.create_agreement_page()
        self.create_main_page()
        self.stack.setCurrentIndex(0)

        self.log_signal.connect(self.write)
        self.finish_signal.connect(lambda: self.start_btn.setEnabled(True))

# ---------------- 协议页 ----------------
    def create_agreement_page(self):

        page = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # 外边距
        layout.setSpacing(12)                      # 控件间距


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
        hint = QLabel("请滚动到底部以启用同意按钮")
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
                block_format.setAlignment(Qt.AlignCenter)  # 大标题居中
                cursor.setBlockFormat(block_format)
                cursor.insertHtml(f'<span style="font-weight:bold; font-size:18pt;">{block["text"]}</span>')
                cursor.insertBlock()
                cursor.insertBlock()

            elif block["type"] == "para":
                block_format.setAlignment(Qt.AlignLeft)  # 文本左对齐
                
                # 章节标题/小标题不缩进
                if block["text"].startswith(("一、", "二、", "三、", "四、")) or block["text"].endswith("："):
                    cursor.setBlockFormat(block_format)
                else:
                    # 普通段落首行缩进
                    block_format.setTextIndent(20)
                    cursor.setBlockFormat(block_format)

                # 不同段落样式
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
                block_format.setTextIndent(20)  # 链接也首行缩进
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


        # ===== 点击进入主界面 =====
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))


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
作者：CAT  BUG反馈：15658109225@163.com
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

        self.label = QLabel("输入抖音视频链接")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.folder_btn = QPushButton("选择保存文件夹")
        layout.addWidget(self.folder_btn)

        self.start_btn = QPushButton("开始下载")
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
        self.progress.setFormat("猫咪正在搬运视频… %p%")
        layout.addWidget(self.progress)
        
        self.progress_signal.connect(self.progress.setValue)

        layout.addWidget(self.log)

        main_widget.setLayout(layout)
        self.stack.addWidget(main_widget)

        # 绑定事件
        self.folder_btn.clicked.connect(self.choose_folder)
        self.start_btn.clicked.connect(self.start_download)

    # ---------------- 工具函数 ----------------
    def write(self, text):
        self.log.append(text)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.folder = folder
            self.write("保存路径: " + folder)

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

        self.log_signal.emit("下载完成: " + path)

        self.progress_signal.emit(100)
        time.sleep(0.3)
        self.progress_signal.emit(0)

        return path

    # ---------------- 下载逻辑 ----------------
    def start_download(self):
        self.start_btn.setEnabled(False)
        video_input = self.url_input.text().strip()
        if not video_input:
            self.write("\n请输入链接")
            self.start_btn.setEnabled(True)
            return
        video_page = self.normalize_url(video_input)
        if not video_page:
            self.write("\n无法解析链接")
            self.start_btn.setEnabled(True)
            return
        self.write("\n解析后链接: " + video_page)
        threading.Thread(target=self.run, args=(video_page,), daemon=True).start()

    def run(self, video_page):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-infobars",
                        "--start-maximized"
                    ]
                )        #浏览器模式更改
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
                    viewport={"width":1280,"height":800}
                )
                page = context.new_page()
                found = {"ok": False}

                page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """)

                def handle_response(resp):
                    if found["ok"]:
                        return
                    if "aweme/v1/web/aweme/detail" in resp.url:
                        found["ok"] = True
                        try:
                            data = resp.json()
                            detail = data["aweme_detail"]
                            video = detail["video"]
                            video_url = None
                            if "play_addr" in video:
                                video_url = video["play_addr"]["url_list"][0]
                            elif "download_addr" in video:
                                video_url = video["download_addr"]["url_list"][0]
                            audio_url = detail["music"]["play_url"]["url_list"][0]
                        except Exception as e:
                            self.log_signal.emit(str(e))
                            return

                        self.log_signal.emit("\n视频地址:")
                        self.log_signal.emit(video_url)
                        self.log_signal.emit("\n音频地址:")
                        self.log_signal.emit(audio_url)
                        self.log_signal.emit("\n")


                        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        video_file = self.download_file(video_url, f"video_{ts}.mp4", page, 0, 50)
                        audio_file = self.download_file(audio_url, f"audio_{ts}.mp3", page, 50, 100)

                        out_file = os.path.join(self.folder, f"video_{ts}.mp4")

                        if shutil.which("ffmpeg"):

                            out_file = os.path.join(self.folder, f"video_{ts}.mp4")

                            cmd = [
                                "ffmpeg",
                                "-y",
                                "-i", video_file,
                                "-i", audio_file,
                                "-c", "copy",
                                out_file
                            ]

                            try:
                                subprocess.run(cmd, check=True)
                                print("视频合并完成")
                            except subprocess.CalledProcessError:
                                print("FFmpeg 运行失败")

                            self.log_signal.emit("完成: " + out_file)
                        else:
                            self.log_signal.emit("\n未检测到 ffmpeg")

                page.on("response", handle_response)
                self.log_signal.emit("\n打开页面...")
                page.goto(video_page)
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000)
                page.mouse.click(640, 360)
                start = time.time()
                timeout = time.time() + 30

                while not found["ok"] and time.time() < timeout:
                    time.sleep(0.2)

                browser.close()
        except Exception as e:
            self.log_signal.emit("错误: " + str(e))
        self.finish_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DouyinDownloader()
    win.show()
    sys.exit(app.exec_())


