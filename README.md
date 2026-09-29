# DouyinDownloader

# 抖音视频下载工具

## 项目简介

本项目是一个基于 Windows 平台，结合 Playwright 与 FFmpeg 技术构建的抖音视频下载工具。程序提供简洁的图形化操作界面，用户只需输入抖音视频链接并选择保存目录，即可自动完成解析与下载。针对抖音常见的"视频流与音频流分离"机制，程序会在下载完成后调用 FFmpeg 自动合并，生成完整的可播放视频文件。

- **开发者**：CAT是猫不是喵
- **问题反馈邮箱**：catmiao14514@163.com

---

## Introduction

This project is a Douyin (TikTok China) video downloader built for the Windows platform, leveraging Playwright and FFmpeg. The application provides a user-friendly graphical interface that allows users to automatically parse and download videos by simply inputting a Douyin video URL and selecting a save directory. To handle Douyin's common mechanism of separating video and audio streams, the program automatically invokes FFmpeg upon download completion to merge the streams into a single, playable video file.

- **Developer**: CAT是猫不是喵
- **Bug Report Email**: catmiao14514@163.com

---

## 核心功能

- **抖音视频链接解析**：输入抖音视频页面 URL，自动解析实际视频地址及音频地址。
- **视频与音频下载**：分别下载视频流与音频流。
- **自动合并**：使用 FFmpeg 将视频与音频合并，输出最终可播放的视频文件。支持 4 种合并策略自动降级（直接复制 -> 流复制 -> 重新编码 -> 自动流选择 -> 仅视频流）。
- **自定义保存目录**：支持在程序界面中选择视频文件的保存位置。
- **视频名称自定义**：可输入自定义视频名称作为子文件夹名，不填则自动按日期时间命名。
- **子文件夹隔离**：每次下载自动创建独立子文件夹，避免多次下载文件互相覆盖。同名文件夹自动追加 _1、_2 后缀。
- **打开保存文件夹按钮**：一键弹出 Windows 资源管理器，直接打开当前设置的视频保存目录。
- **下载完成自动打开文件夹**：下载完成后自动弹出资源管理器，直接显示下载好的三个文件（合并视频 + 原始视频流 + 原始音频流）。
- **下载重试机制**：网络波动时自动重试（最多 3 次），无需手动重新下载。
- **用户协议记忆**：勾选"不再提醒"后，下次启动自动跳过协议页。
- **JSON 配置持久化**：保存路径、协议状态等配置自动保存到 config.json，换机器迁移方便。
- **FFmpeg 健康检查**：启动合并前自动检测 ffmpeg.exe 是否存在、文件头是否有效、能否正常执行。
- **Windows 图形化界面**：无需手动执行复杂命令，运行程序后按照界面提示操作即可。
- **Playwright 辅助解析**：程序目录内提供 ms-playwright 运行所需资源，确保网页解析的稳定性。

---

## Core Features

- **Douyin Video URL Parsing**: Automatically extracts the actual video and audio URLs from a provided Douyin video page URL.
- **Video & Audio Download**: Downloads both video and audio streams separately.
- **Automatic Merging**: Utilizes FFmpeg to merge video and audio streams into a final, playable video file. Supports 4 fallback strategies (direct copy -> stream copy -> re-encode -> auto stream selection -> video-only).
- **Custom Save Directory**: Allows users to select the destination folder for downloaded videos via the GUI.
- **Custom Video Name**: Enter a custom name for the download folder. If left blank, the folder is auto-named with the current date/time.
- **Sub-folder Isolation**: Each download creates an independent sub-folder to prevent file overwrites. If a folder with the same name exists, _1, _2 suffixes are auto-appended.
- **Open Save Folder Button**: One-click open Windows Explorer to the configured download directory.
- **Auto-open Folder on Completion**: Automatically opens the download sub-folder in Explorer after download finishes, showing all three generated files.
- **Download Retry Mechanism**: Automatically retries failed downloads (up to 3 attempts) on network issues.
- **Agreement Memory**: Check "Do not remind again" to skip the agreement screen on future launches.
- **JSON Config Persistence**: Save path, agreement status, and other settings are automatically persisted in config.json.
- **FFmpeg Health Check**: Automatically verifies ffmpeg.exe existence, file header validity, and executability before merging.
- **Windows Graphical Interface**: Eliminates the need for complex command-line operations; simply follow the on-screen prompts.
- **Playwright-Assisted Parsing**: Includes the necessary ms-playwright runtime resources within the program directory to ensure stable web parsing.

---

## 项目目录结构（源码仓库）

以下为 GitHub 源码仓库中的文件结构：

```
douyin_downloader/
├── 许可证                     # 项目许可证文件
├── README.md                   # 项目说明文档（本文件）
├── config.example.json         # 配置文件示例模板（不含敏感信息，可公开上传）
├── main.py                     # Python 源码（V1.2.0）
└── requirements.txt            # Python 依赖包列表
```

### 文件说明

| 文件/文件夹名称 | 说明 |
| :--- | :--- |
| 许可证 | 项目许可证文件 |
| README.md | 项目说明文档（本文件） |
| config.example.json | 配置文件示例模板（供用户参考，不含个人敏感信息） |
| main.py | Python 源代码文件（开发/修改用） |
| requirements.txt | Python 依赖包列表（pip install -r requirements.txt 安装） |

---

## 发行版目录结构（用户运行目录）

以下为下载解压后的发行版程序目录结构：

```
douyin_downloader_V1.2.0/
├── douyin_downloader_V1.2.0.exe   # 打包后的主程序可执行文件（PyInstaller --onedir）
├── ffmpeg.exe                      # 用于视频与音频流的合并处理
├── ms-playwright/                  # Playwright 浏览器运行环境
├── _internal/                      # PyInstaller 自动生成的运行时目录（勿删）
├── config.json                     # 程序配置文件（首次运行自动生成，存储保存路径等）
└── 视频存放处/                      # 默认的视频输出目录
```

### 文件说明

| 文件/文件夹名称 | 说明 |
| :--- | :--- |
| douyin_downloader_V1.2.0.exe | 主程序可执行文件（PyInstaller --onedir 打包产物） |
| ffmpeg.exe | 用于视频与音频流的合并处理 |
| ms-playwright/ | Playwright 浏览器运行环境 |
| _internal/ | PyInstaller --onedir 模式自动生成的运行时目录，包含 Python 运行库和第三方依赖 |
| config.json | 程序配置文件（首次运行自动生成，存储保存路径、协议状态等） |
| 视频存放处/ | 默认的视频输出目录 |

> **注意**：ffmpeg.exe 和 ms-playwright/ 属于程序运行所必需的辅助组件。请勿随意删除或移动这些文件，否则可能导致解析、下载或合并功能异常。_internal/ 目录由 PyInstaller 自动生成，请勿手动修改。

---

## Project Directory Structure (Source Repository)

The following is the file structure in the GitHub source repository:

```
douyin_downloader/
├── LICENSE                     # Project license file
├── README.md                   # Project documentation (this file)
├── config.example.json         # Config file template (no sensitive info, safe to push to GitHub)
├── main.py                     # Python source code (V1.2.0)
└── requirements.txt            # Python dependency list
```

### File Description

| File/Folder Name | Description |
| :--- | :--- |
| LICENSE | Project license file |
| README.md | Project documentation (this file) |
| config.example.json | Config file template (for reference, contains no sensitive information) |
| main.py | Python source code file (for development/modification) |
| requirements.txt | Python dependency list (install with pip install -r requirements.txt) |

---

## Distribution Directory Structure (Runtime Directory)

The following is the directory structure after extracting the downloaded release:

```
douyin_downloader_V1.2.0/
├── douyin_downloader_V1.2.0.exe   # Packaged main executable (PyInstaller --onedir)
├── ffmpeg.exe                      # Used for merging video and audio streams
├── ms-playwright/                  # Playwright browser runtime environment
├── _internal/                      # Auto-generated runtime directory by PyInstaller (do not delete)
├── config.json                     # Program config file (auto-created on first run, stores save path etc.)
└── 视频存放处/                      # Default output directory for videos
```

### File Description

| File/Folder Name | Description |
| :--- | :--- |
| douyin_downloader_V1.2.0.exe | Main executable file (PyInstaller --onedir build output) |
| ffmpeg.exe | Used for merging video and audio streams |
| ms-playwright/ | Playwright browser runtime environment |
| _internal/ | Auto-generated runtime directory by PyInstaller --onedir, contains Python runtime and third-party dependencies |
| config.json | Program configuration file (auto-created on first run, stores save path, agreement status, etc.) |
| 视频存放处/ | Default output directory for videos |

> **Warning**: ffmpeg.exe and the ms-playwright/ directory are essential auxiliary components required for the program to function correctly. Do not delete or move these files arbitrarily, as doing so may cause parsing, downloading, or merging functionalities to fail. The _internal/ directory is auto-generated by PyInstaller - do not modify it manually.

---

## 使用方法

1. **启动程序**：双击 douyin_downloader_V1.2.0.exe。首次启动时将显示用户协议与使用条款，请仔细阅读后根据实际情况选择是否继续使用。可勾选"不再提醒此协议"以跳过后续启动时的协议页。
2. **获取抖音视频链接**：在浏览器中打开需要下载的抖音视频页面（例如：https://www.douyin.com/jingxuan?modal_id=xxxxxxxxxxxxxxxx），并复制该视频页面的完整 URL。建议直接复制视频播放页地址，避免复制搜索页面、个人主页或其他无关链接。
3. **粘贴链接**：将复制的 URL 粘贴到程序界面的"请输入抖音视频链接"输入框中。
4. **（可选）输入视频名称**：在"视频名称"输入框中填写自定义名称，下载任务将以此命名子文件夹。不填则自动按"YYYYMMDD_HHMMSS"格式命名。
5. **选择保存目录**：点击"选择保存文件夹"，指定下载文件的存放路径（例如：D:\Douyin\Downloads）。程序会自动记住上次选择的目录。
6. **（可选）打开保存文件夹**：点击"打开保存文件夹"按钮，可直接弹出 Windows 资源管理器打开当前设置的视频保存目录，方便查看已下载的文件。
7. **开始下载**：确认链接与保存目录无误后，点击"让修猫立刻下载"。程序将自动执行以下流程：解析抖音链接 -> 打开视频页面 -> 获取视频地址 -> 获取音频地址 -> 下载视频流 -> 下载音频流 -> 调用 FFmpeg 合并 -> 生成最终视频文件。
8. **下载完成**：下载完成后程序会自动打开下载子文件夹，直接显示生成的三个文件（合并后的视频 + 原始视频流 + 原始音频流）。

---

## Usage Instructions

1. **Launch the Program**: Double-click douyin_downloader_V1.2.0.exe. Upon first launch, the User Agreement and Terms of Use will be displayed. Please read them carefully and decide whether to proceed. You can check "Do not remind again" to skip the agreement screen on future launches.
2. **Obtain the Douyin Video URL**: Open the desired Douyin video page in your browser (e.g., https://www.douyin.com/jingxuan?modal_id=xxxxxxxxxxxxxxxx) and copy the full URL. It is recommended to copy the direct video playback page URL rather than search pages, profile pages, or other irrelevant links.
3. **Paste the URL**: Paste the copied URL into the "Input Douyin Video URL" field in the program interface.
4. **(Optional) Enter Video Name**: Enter a custom name in the "Video Name" field. The download task will use this as the sub-folder name. If left blank, it auto-names using "YYYYMMDD_HHMMSS" format.
5. **Select Save Directory**: Click "Select Save Folder" to specify the destination path for downloaded files (e.g., D:\Douyin\Downloads). The program remembers the last selected directory.
6. **(Optional) Open Save Folder**: Click the "Open Save Folder" button to directly open Windows Explorer at the configured download directory, making it easy to view downloaded files.
7. **Start Download**: After confirming the URL and save directory are correct, click "Start Download". The program will automatically execute: Parse Douyin URL -> Open video page -> Extract video URL -> Extract audio URL -> Download video stream -> Download audio stream -> Invoke FFmpeg to merge -> Generate final video file.
8. **Download Complete**: After download finishes, the program automatically opens the download sub-folder in Explorer, showing all three generated files (merged video + original video stream + original audio stream).

---

## 文件合并机制

部分抖音视频采用视频与音频分离的方式提供媒体资源。在下载过程中，程序可能会先生成 video_时间戳.mp4 和 audio_时间戳.mp3。随后，程序将自动调用 FFmpeg 进行合并，生成 merge_时间戳.mp4。

合并策略按优先级依次尝试（任一成功即停止）：

1. **直接复制视频文件**（抖音下载的视频文件本身已包含音频流，最直接高效）
2. **流复制（copy）**：不重新编码，直接复制音视频流
3. **重新编码（libx264 + aac）**：对音视频重新编码合并
4. **自动流选择**：FFmpeg 自动选择最佳流
5. **仅复制视频流**：跳过音频，仅复制视频

最终的 merge_*.mp4 即为合并完成的完整视频文件。所有中间文件（原始视频流、原始音频流）会保留在子文件夹中供排查使用。

- **处理流程**：视频流 + 音频流 -> FFmpeg 智能合并（4种策略降级） -> merge_*.mp4

---

## File Merging Mechanism

Some Douyin videos provide media resources with separated video and audio streams. During the download process, the program may first generate video_timestamp.mp4 and audio_timestamp.mp3. Subsequently, the program automatically invokes FFmpeg to merge them.

Merge strategies are tried in priority order (stops on first success):

1. **Direct copy of video file** (Douyin downloaded videos already contain audio streams internally - most efficient)
2. **Stream copy (copy)**: No re-encoding, directly copies audio/video streams
3. **Re-encode (libx264 + aac)**: Re-encodes and merges audio/video
4. **Auto stream selection**: FFmpeg auto-selects best streams
5. **Video-only copy**: Skips audio, copies video stream only

The final merge_*.mp4 is the fully merged video file. All intermediate files (original video stream, original audio stream) are retained in the sub-folder for troubleshooting.

- **Processing Workflow**: Video Stream + Audio Stream -> FFmpeg Smart Merge (4 fallback strategies) -> merge_*.mp4

---

## 日志信息

程序运行过程中会在窗口中实时显示处理状态，包括：保存路径、解析后的链接、页面打开状态、视频地址、音频地址、下载进度、FFmpeg 健康检查结果、合并策略尝试信息及合成完成等信息。这些日志可用于判断当前程序的执行进度。若出现错误，建议保留完整日志以便后续排查。

---

## Log Information

During execution, the program displays real-time processing status in the window, including: save path, parsed URLs, page loading status, video URL, audio URL, download progress, FFmpeg health check results, merge strategy attempts, and merge completion. These logs can be used to track the current execution progress. In case of errors, it is recommended to retain the complete log for troubleshooting.

---

## 常见问题

1. **出现 403 Forbidden**：若程序成功解析出视频地址，但在下载时提示 403 Forbidden，通常表示当前媒体地址的访问受到服务端限制。可能原因包括：媒体地址具有时效性、地址与请求环境绑定、CDN/服务端访问限制、链接失效或当前网络环境不满足服务端要求。这并不一定代表解析失败。建议：重新复制最新的视频页面 URL、重新解析并尽快下载。若仍失败，请保存日志后反馈。
2. **只有视频没有声音**：若下载目录中存在 video_*.mp4 和 audio_*.mp3 但缺少最终的 merge_*.mp4，请优先检查：ffmpeg.exe 是否存在、是否被杀毒软件隔离、程序目录是否被移动、FFmpeg 是否具备执行权限。也可查看日志中的 FFmpeg 健康检查结果和合并策略失败原因。
3. **程序无法启动**：请检查程序目录是否完整。至少应确认 douyin_downloader_V1.2.0.exe、ffmpeg.exe 及 ms-playwright/ 均存在。请勿仅复制 .exe 文件单独运行。
4. **解析失败**：可尝试：确认复制的是抖音视频页面 URL、重新打开视频后再次复制链接、重启程序、检查网络连接或尝试其他公开可访问的视频。若仍失败，请提交完整日志。
5. **下载文件被覆盖**：程序已内置文件夹名称冲突检测机制。如果两次下载使用相同名称，程序会自动在文件夹名后追加 _1、_2 等后缀，不会覆盖已有文件。日志中会打印提醒信息。

---

## Frequently Asked Questions

1. **403 Forbidden Error**: If the program successfully parses the video URL but encounters a 403 Forbidden error during download, it usually indicates that access to the media URL is restricted by the server. Possible reasons include: URL expiration, environment binding, CDN/server access restrictions, invalid links, or network environment mismatches. This does not necessarily mean parsing has failed. Suggested actions: Copy the latest video page URL again, re-parse, and download promptly. If it still fails, save the log and report the issue.
2. **Video Without Audio**: If video_*.mp4 and audio_*.mp3 exist in the download directory but the final merge_*.mp4 is missing, please check: whether ffmpeg.exe exists, whether it has been quarantined by antivirus software, whether the program directory has been moved, and whether FFmpeg has execution permissions. Also check the log for FFmpeg health check results and merge strategy failure reasons.
3. **Program Fails to Launch**: Verify that the program directory is complete. Ensure that douyin_downloader_V1.2.0.exe, ffmpeg.exe, and the ms-playwright/ directory are all present. Do not copy and run the .exe file alone.
4. **Parsing Failure**: Try: confirming that the copied URL is a valid Douyin video page URL, reopening the video and copying the link again, restarting the program, checking the network connection, or trying another publicly accessible video. If the issue persists, please submit the complete log.
5. **Downloaded Files Overwritten**: The program includes built-in folder name conflict detection. If two downloads use the same name, the program automatically appends _1, _2 suffixes to the folder name, preventing file overwrites. A reminder message will be printed in the log.

---

## 技术栈

根据当前打包版本的运行结构，本项目主要涉及以下技术：

- **Python / PyQt5**：Windows GUI 图形界面
- **Playwright**：用于辅助访问与解析网页环境。程序目录中的 ms-playwright/ 为 Playwright 浏览器运行环境。
- **FFmpeg**：用于处理媒体文件，将分离的视频流和音频流合并为最终视频。支持 4 种合并策略自动降级。
- **HTTP / Web 请求**：requests 库进行视频/音频流下载，内置重试装饰器。
- **JSON 配置持久化**：用户设置自动保存到 config.json。
- **抖音网页媒体资源解析**：通过 Playwright 模拟浏览器环境提取媒体地址。

---

## Tech Stack

Based on the runtime structure of the current packaged version, this project primarily involves the following technologies:

- **Python / PyQt5**: Windows GUI graphical interface
- **Playwright**: Used to assist in accessing and parsing web environments. The ms-playwright/ directory contains the Playwright browser runtime.
- **FFmpeg**: Used for media file processing, specifically merging separated video and audio streams into the final video. Supports 4 fallback merge strategies.
- **HTTP / Web Requests**: requests library for video/audio stream download with built-in retry decorator.
- **JSON Config Persistence**: User settings automatically saved to config.json.
- **Douyin Web Media Resource Parsing**: Extracts media URLs by simulating browser environment via Playwright.

---

## 使用说明与免责声明

本工具仅用于学习、研究以及对本人拥有合法使用权的公开内容进行处理。使用本工具时，请严格遵守：

- 抖音相关用户协议及平台规则
- 著作权、知识产权等相关法律法规
- 视频作者及版权所有者的合法权益

**请勿利用本工具：**

- 下载、传播未经授权的受版权保护内容
- 绕过平台访问控制或安全措施
- 批量抓取或滥用平台资源
- 将下载内容用于违法或侵权用途

用户需自行承担使用本工具产生的所有相关法律责任。

---

## Usage Guidelines & Disclaimer

This tool is strictly intended for educational, research purposes, and processing publicly available content for which the user holds legal usage rights. When using this tool, you must strictly comply with:

- Douyin's User Agreement and platform rules
- Relevant laws and regulations regarding copyright and intellectual property
- The legitimate rights and interests of video authors and copyright holders

**Do NOT use this tool to:**

- Download or distribute unauthorized copyrighted content
- Bypass platform access controls or security measures
- Conduct mass scraping or abuse platform resources
- Use downloaded content for illegal or infringing purposes

Users assume full legal responsibility for any consequences arising from the use of this tool.

---

## BUG 反馈

如果遇到问题，请尽量提供以下信息以便排查：

1. Windows 操作系统版本
2. 程序版本号（如 V1.2.0）
3. 使用的视频链接类型
4. 程序完整运行日志
5. 错误截图
6. 是否能够正常在浏览器中打开该视频页面

**反馈邮箱**：catmiao14514@163.com

---

## Bug Reporting

If you encounter any issues, please provide the following information to facilitate troubleshooting:

1. Windows OS version
2. Program version number (e.g., V1.2.0)
3. Type of video URL used
4. Complete program runtime log
5. Screenshot of the error
6. Whether the video page can be opened normally in a browser

**Feedback Email**: catmiao14514@163.com

---

## 更新日志

### V1.2.0（当前版本 · Stable Release）

> 这是整合 v1.0.0 ~ v1.1.9 所有改进的稳定版发布。v1.1.9 作为测试版经过验证后升级为 v1.2.0 正式发行版。

- **新增**：文件夹名称冲突检测机制，防止同名下载任务覆盖已有文件（自动追加 _1、_2 后缀）
- **新增**：视频名称自定义输入框，支持自定义下载子文件夹名称
- **新增**：每次下载自动创建独立子文件夹，文件管理更清晰
- **新增**："打开保存文件夹"按钮，一键弹出资源管理器打开保存目录
- **新增**：下载完成后自动打开下载子文件夹（直接显示三个生成文件）
- **新增**：视频名称输入框功能
- **新增**：JSON 配置持久化（保存路径、协议状态自动保存）
- **新增**："不再提醒"复选框（协议页记住用户选择）
- **新增**：@retry 下载重试装饰器（网络失败自动重试 3 次）
- **新增**：FFmpeg 健康检查（文件存在性、文件头检测、版本执行测试）
- **新增**：文件头类型检测（自动识别 MP4/MP3/H.264 等格式）
- **新增**：ffprobe 编码信息探测
- **新增**：原始字节捕获 stderr（避免编码错误导致日志丢失）
- **新增**：4 种合并策略降级机制（直接复制 -> 流复制 -> 重新编码 -> 自动流选择 -> 仅视频流）
- **新增**：直接复制自带音频视频策略（FFmpeg 合并优化）
- **修复**：Python 三元表达式优先级错误导致的逻辑异常
- **修复**：输出文件名与输入文件名相同时的文件冲突问题
- **修复**：同名文件夹重复下载导致文件覆盖的 Bug
- **修复**：import shutil 缺失导致的运行错误
- **修复**：JSON 配置文件加载异常问题
- **更新**：邮箱地址更新为 catmiao14514@163.com
- **更新**：作者名更新为 CAT是猫不是喵
- **更新**：打包文件名更新为 douyin_downloader_V1.2.0.exe

### V1.1.9（测试版）

- **新增**：文件夹名称冲突检测机制，防止同名下载任务覆盖已有文件（自动追加 _1、_2 后缀）
- **新增**：视频名称自定义输入框，支持自定义下载子文件夹名称
- **新增**：每次下载自动创建独立子文件夹，文件管理更清晰
- **修复**：同名文件夹重复下载导致文件覆盖的 Bug

---

## Project Status

The current version (V1.2.0) is a Windows packaged stable release, integrating all improvements from v1.0.0 through v1.1.9. The core workflow is fully implemented: URL Input -> Page Parsing -> Video/Audio URL Extraction -> Video Download -> Audio Download -> FFmpeg Merge -> Final MP4 Generation. In cases of 403 responses from media servers or invalid links, further investigation based on specific logs is required.

---

## Acknowledgments

We extend our gratitude to everyone who participated in testing and provided feedback. If you discover any bugs, your reports are highly welcome.

**Developer**: CAT是猫不是喵

---

## 致谢

感谢所有参与测试和反馈问题的用户。如果您发现任何 BUG，欢迎随时反馈。

**开发者**：CAT是猫不是喵
