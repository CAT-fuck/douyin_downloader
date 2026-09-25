# douyin_downloader
# 抖音视频下载工具

## 项目简介

本项目是一个基于 Windows 平台，结合 Playwright 与 FFmpeg 技术构建的抖音视频下载工具。程序提供简洁的图形化操作界面，用户只需输入抖音视频链接并选择保存目录，即可自动完成解析与下载。针对抖音常见的"视频流与音频流分离"机制，程序会在下载完成后调用 FFmpeg 自动合并，生成完整的可播放视频文件。

- **开发者**：CAT
- **问题反馈邮箱**：15658109225@163.com

---

## Introduction

This project is a Douyin (TikTok China) video downloader built for the Windows platform, leveraging Playwright and FFmpeg. The application provides a user-friendly graphical interface that allows users to automatically parse and download videos by simply inputting a Douyin video URL and selecting a save directory. To handle Douyin's common mechanism of separating video and audio streams, the program automatically invokes FFmpeg upon download completion to merge the streams into a single, playable video file.

- **Developer**: CAT
- **Bug Report Email**: 15658109225@163.com

---

## 核心功能

- **抖音视频链接解析**：输入抖音视频页面 URL，自动解析实际视频地址及音频地址。
- **视频与音频下载**：分别下载视频流与音频流。
- **自动合并**：使用 FFmpeg 将视频与音频合并，输出最终可播放的视频文件。
- **自定义保存目录**：支持在程序界面中选择视频文件的保存位置。
- **Windows 图形化界面**：无需手动执行复杂命令，运行程序后按照界面提示操作即可。
- **Playwright 辅助解析**：程序目录内提供 ms-playwright 运行所需资源，确保网页解析的稳定性。

---

## Core Features

- **Douyin Video URL Parsing**: Automatically extracts the actual video and audio URLs from a provided Douyin video page URL.
- **Video & Audio Download**: Downloads both video and audio streams separately.
- **Automatic Merging**: Utilizes FFmpeg to merge video and audio streams into a final, playable video file.
- **Custom Save Directory**: Allows users to select the destination folder for downloaded videos via the GUI.
- **Windows Graphical Interface**: Eliminates the need for complex command-line operations; simply follow the on-screen prompts.
- **Playwright-Assisted Parsing**: Includes the necessary ms-playwright runtime resources within the program directory to ensure stable web parsing.

---

## 程序目录结构

```
Douyin Downloader/
├─ douyin_downloader完整源版窗口.exe
├─ ffmpeg.exe
├─ ms-playwright/
└─ 视频存放处/
```

### 文件说明

| 文件/文件夹名称 | 说明 |
| :--- | :--- |
| douyin_downloader完整源版窗口.exe | 主程序可执行文件 |
| ffmpeg.exe | 用于视频与音频流的合并处理 |
| ms-playwright/ | Playwright 浏览器运行环境 |
| 视频存放处/ | 默认的视频输出目录 |

> **注意**：ffmpeg.exe 和 ms-playwright/ 属于程序运行所必需的辅助组件。请勿随意删除或移动这些文件，否则可能导致解析、下载或合并功能异常。

---

## Directory Structure

```
Douyin Downloader/
├─ douyin_downloader完整源版窗口.exe
├─ ffmpeg.exe
├─ ms-playwright/
└─ 视频存放处/
```

### File Description

| File/Folder Name | Description |
| :--- | :--- |
| douyin_downloader完整源版窗口.exe | Main executable file |
| ffmpeg.exe | Used for merging video and audio streams |
| ms-playwright/ | Playwright browser runtime environment |
| 视频存放处/ | Default output directory for videos |

> **Warning**: ffmpeg.exe and the ms-playwright/ directory are essential auxiliary components required for the program to function correctly. Do not delete or move these files arbitrarily, as doing so may cause parsing, downloading, or merging functionalities to fail.

---

## 使用方法

1. **启动程序**：双击 douyin_downloader完整源版窗口.exe。首次启动时将显示用户协议与使用条款，请仔细阅读后根据实际情况选择是否继续使用。
2. **获取抖音视频链接**：在浏览器中打开需要下载的抖音视频页面（例如：https://www.douyin.com/jingxuan?modal_id=xxxxxxxxxxxxxxxx），并复制该视频页面的完整 URL。建议直接复制视频播放页地址，避免复制搜索页面、个人主页或其他无关链接。
3. **粘贴链接**：将复制的 URL 粘贴到程序界面的"输入抖音视频链接"输入框中。
4. **选择保存目录**：点击"选择保存文件夹"，指定下载文件的存放路径（例如：D:\Douyin\Downloads）。
5. **开始下载**：确认链接与保存目录无误后，点击"开始下载"。程序将自动执行以下流程：解析抖音链接 -> 打开视频页面 -> 获取视频地址 -> 获取音频地址 -> 下载视频流 -> 下载音频流 -> 调用 FFmpeg 合并 -> 生成最终视频文件。

---

## Usage Instructions

1. **Launch the Program**: Double-click douyin_downloader完整源版窗口.exe. Upon first launch, the User Agreement and Terms of Use will be displayed. Please read them carefully and decide whether to proceed based on your actual situation.
2. **Obtain the Douyin Video URL**: Open the desired Douyin video page in your browser (e.g., https://www.douyin.com/jingxuan?modal_id=xxxxxxxxxxxxxxxx) and copy the full URL. It is recommended to copy the direct video playback page URL rather than search pages, profile pages, or other irrelevant links.
3. **Paste the URL**: Paste the copied URL into the "Input Douyin Video URL" field in the program interface.
4. **Select Save Directory**: Click "Select Save Folder" to specify the destination path for downloaded files (e.g., D:\Douyin\Downloads).
5. **Start Download**: After confirming that the URL and save directory are correct, click "Start Download". The program will automatically execute the following workflow: Parse Douyin URL -> Open video page -> Extract video URL -> Extract audio URL -> Download video stream -> Download audio stream -> Invoke FFmpeg to merge -> Generate final video file.

---

## 文件合并机制

部分抖音视频采用视频与音频分离的方式提供媒体资源。在下载过程中，程序可能会先生成 video_20260223_203904_060316.mp4 和 audio_20260223_203904_060316.mp3。随后，程序将自动调用 FFmpeg 进行合并，生成 merge_20260223_203904_060316.mp4。最终的 merge_*.mp4 即为合并完成的完整视频文件。

- **处理流程**：视频流 + 音频流 -> FFmpeg 合并 -> merge_*.mp4

---

## File Merging Mechanism

Some Douyin videos provide media resources with separated video and audio streams. During the download process, the program may first generate video_20260223_203904_060316.mp4 and audio_20260223_203904_060316.mp3. Subsequently, the program will automatically invoke FFmpeg to merge them into merge_20260223_203904_060316.mp4. The final merge_*.mp4 file is the fully merged video.

- **Processing Workflow**: Video Stream + Audio Stream -> FFmpeg Merge -> merge_*.mp4

---

## 日志信息

程序运行过程中会在窗口中实时显示处理状态，包括：保存路径、解析后的链接、页面打开状态、视频地址、音频地址、下载完成及合成完成等信息。这些日志可用于判断当前程序的执行进度。若出现错误，建议保留完整日志以便后续排查。

---

## Log Information

During execution, the program displays real-time processing status in the window, including: save path, parsed URLs, page loading status, video URL, audio URL, download completion, and merge completion. These logs can be used to track the current execution progress. In case of errors, it is recommended to retain the complete log for troubleshooting.

---

## 常见问题

1. **出现 403 Forbidden**：若程序成功解析出视频地址，但在下载时提示 403 Forbidden，通常表示当前媒体地址的访问受到服务端限制。可能原因包括：媒体地址具有时效性、地址与请求环境绑定、CDN/服务端访问限制、链接失效或当前网络环境不满足服务端要求。这并不一定代表解析失败。建议：重新复制最新的视频页面 URL、重新解析并尽快下载。若仍失败，请保存日志后反馈。
2. **只有视频没有声音**：若下载目录中存在 video_*.mp4 和 audio_*.mp3 但缺少最终的 merge_*.mp4，请优先检查：ffmpeg.exe 是否存在、是否被杀毒软件隔离、程序目录是否被移动、FFmpeg 是否具备执行权限。
3. **程序无法启动**：请检查程序目录是否完整。至少应确认 douyin_downloader完整源版窗口.exe、ffmpeg.exe 及 ms-playwright/ 均存在。请勿仅复制 .exe 文件单独运行。
4. **解析失败**：可尝试：确认复制的是抖音视频页面 URL、重新打开视频后再次复制链接、重启程序、检查网络连接或尝试其他公开可访问的视频。若仍失败，请提交完整日志。

---

## Frequently Asked Questions

1. **403 Forbidden Error**: If the program successfully parses the video URL but encounters a 403 Forbidden error during download, it usually indicates that access to the media URL is restricted by the server. Possible reasons include: URL expiration, environment binding, CDN/server access restrictions, invalid links, or network environment mismatches. This does not necessarily mean parsing has failed. Suggested actions: Copy the latest video page URL again, re-parse, and download promptly. If it still fails, save the log and report the issue.
2. **Video Without Audio**: If video_*.mp4 and audio_*.mp3 exist in the download directory but the final merge_*.mp4 is missing, please check: whether ffmpeg.exe exists, whether it has been quarantined by antivirus software, whether the program directory has been moved, and whether FFmpeg has execution permissions.
3. **Program Fails to Launch**: Verify that the program directory is complete. Ensure that douyin_downloader完整源版窗口.exe, ffmpeg.exe, and the ms-playwright/ directory are all present. Do not copy and run the .exe file alone.
4. **Parsing Failure**: Try: confirming that the copied URL is a valid Douyin video page URL, reopening the video and copying the link again, restarting the program, checking the network connection, or trying another publicly accessible video. If the issue persists, please submit the complete log.

---

## 技术栈

根据当前打包版本的运行结构，本项目主要涉及以下技术：

- **Python / Windows GUI**
- **Playwright**：用于辅助访问与解析网页环境。程序目录中的 ms-playwright/ 为 Playwright 浏览器运行环境。
- **FFmpeg**：用于处理媒体文件，将分离的视频流和音频流合并为最终视频。
- **HTTP / Web 请求**
- **抖音网页媒体资源解析**

---

## Tech Stack

Based on the runtime structure of the current packaged version, this project primarily involves the following technologies:

- **Python / Windows GUI**
- **Playwright**: Used to assist in accessing and parsing web environments. The ms-playwright/ directory contains the Playwright browser runtime.
- **FFmpeg**: Used for media file processing, specifically merging separated video and audio streams into the final video.
- **HTTP / Web Requests**
- **Douyin Web Media Resource Parsing**

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
2. 程序版本号
3. 使用的视频链接类型
4. 程序完整运行日志
5. 错误截图
6. 是否能够正常在浏览器中打开该视频页面

**反馈邮箱**：15658109225@163.com

---

## Bug Reporting

If you encounter any issues, please provide the following information to facilitate troubleshooting:

1. Windows OS version
2. Program version number
3. Type of video URL used
4. Complete program runtime log
5. Screenshot of the error
6. Whether the video page can be opened normally in a browser

**Feedback Email**: 15658109225@163.com

---

## 项目状态

当前版本为 Windows 打包测试版本。程序核心流程已完整覆盖：URL 输入 -> 页面解析 -> 视频/音频地址提取 -> 视频下载 -> 音频下载 -> FFmpeg 合并 -> 生成最终 MP4 文件。若遇到媒体服务器返回 403 或链接失效等情况，需根据具体日志进一步排查。

---

## Project Status

The current version is a Windows packaged test release. The core workflow is fully implemented: URL Input -> Page Parsing -> Video/Audio URL Extraction -> Video Download -> Audio Download -> FFmpeg Merge -> Final MP4 Generation. In cases of 403 responses from media servers or invalid links, further investigation based on specific logs is required.

---

## 致谢

感谢所有参与测试和反馈问题的用户。如果您发现任何 BUG，欢迎随时反馈。

**Developer**: CAT

---

## Acknowledgments

We extend our gratitude to everyone who participated in testing and provided feedback. If you discover any bugs, your reports are highly welcome.

**Developer**: CAT
