"""
启动脚本：主要功能是启动 Ollama GUI 程序并抑制所有不必要的警告输出
实现目标：
1. 配置环境变量以控制程序输出
2. 使用子进程方式启动主程序
3. 完全抑制所有标准输出和错误输出
4. 确保程序能够正常退出
"""
import os
import sys
import subprocess

"""
环境变量配置块1：
设置基本的Python解释器编码环境
- PYTHONIOENCODING：确保Python的输入输出使用UTF-8编码
- PYTHONLEGACYWINDOWSSTDIO：处理Windows系统的特殊编码需求
"""
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'

"""
环境变量配置块2：
设置扩展的环境变量，用于抑制特定警告
- PYTHONIOENCODING：确保编码一致性
- PYTHONLEGACYWINDOWSSTDIO：Windows系统兼容性
- PILLOW_WARNINGS：抑制PIL库的警告信息
"""
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
os.environ['PILLOW_WARNINGS'] = 'FALSE'

# 构建主程序路径：获取当前脚本的绝对路径，并找到主程序文件
current_dir = os.path.dirname(os.path.abspath(__file__))
main_script = os.path.join(current_dir, 'main.py')

"""
主程序启动块：
使用subprocess.run启动主程序，具有以下特点：
1. 使用with语句管理devnull文件句柄
2. 完全重定向stdout和stderr到空设备
3. 设置UTF-8编码确保文本处理正确
4. 使用errors='ignore'忽略潜在的编码错误
"""
with open(os.devnull, 'w', encoding='utf-8') as devnull:
    process = subprocess.run(
        [sys.executable, main_script],
        stdout=devnull,
        stderr=devnull,
        encoding='utf-8',
        errors='ignore'
    )

# 程序结束提示：使用flush=True确保消息立即显示在终端
print("程序已退出。", flush=True)