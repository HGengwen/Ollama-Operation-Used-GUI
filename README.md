# Ollama Operation Used GUI V1.0

## 项目简介

Ollama Operation Used GUI 是一个基于Python开发的图形用户界面软件，用于与Ollama服务端进行交互。它支持多种操作，包括与模型对话、列出可用模型、拉取模型、删除模型等。该软件旨在为用户提供一个直观、易用的操作界面，同时优化用户体验。

## 系统要求

- 操作系统：Windows 11
- Python版本：Python 3.12.3（其他版本的Python没有测试过）
- Ollama服务：已在本地运行（默认IP地址：127.0.0.1，端口号：11434）

## 功能特性

**多页显示**：

- 模型对话页面（`chat_with_model`）
- 模型操作页面（列出、拉取、删除模型等）

**交互功能**：

- 与模型对话时支持输入IP地址或网址
- 模型列表显示
- 拉取模型时支持进度条显示

**用户体验**：

- 页面标签互斥显示，当前页面标签加粗
- 操作输出区域支持自动换行和滚动条
- 对话框支持链接跳转（如Ollama官网）

## 安装指南

1. **克隆仓库**：
   
   ```bash
   git clone https://github.com/your-username/olama-gui-interface.git
   cd olama-gui-interface
   ```

2. **安装依赖**：
   
   ```bash
   pip install -r requirements.txt
   ```

3. **运行软件**：
   
   ```bash
   python main.py
   ```

## 使用方法

1. **启动软件**：
   
   - 软件启动后，默认显示模型对话页面，IP地址和端口号已预设为本地Ollama服务的默认值。

2. **模型对话**：
   
   - 在对话输入框中输入内容，按`Enter`键或点击发送按钮进行对话。
   - 对话结果将显示在对话结果框中。

3. **模型操作**：
   
   - 切换到模型操作页面，点击“列出模型”按钮查看可用模型。
   - 拉取模型时，输入模型名称并确认，进度条将显示拉取进度。
   - 删除模型时，从下拉列表中选择模型并确认删除。

4. **其他功能**：
   
   - 点击“显示版本信息”按钮查看Ollama服务端的版本号。
   - 点击“退出程序”按钮关闭软件。

## 开发说明

1. **代码结构**：
   
   - start.py： 启动脚本：主要功能是启动 Ollama GUI的主程序main.py
   - main.py：主程序入口，负责界面初始化和事件绑定。

2. **依赖库**：
   
   - `tkinter`：用于构建图形用户界面。
   - `requests`：用于与Ollama服务进行HTTP交互。

3. **开发建议**：
   
   - 在开发过程中，使用了ython 3.12.3，应该在Python3.8以上都能运行，但没有测试过。
   - 界面布局使用`grid`布局管理器，方便调整控件位置和大小。

#### 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本项目。
2. 创建新分支：`git checkout -b feature/your-feature-name`。
3. 提交更改：`git commit -m "Add some feature"`。
4. 推送到远程仓库：`git push origin feature/your-feature-name`。
5. 提交Pull Request。

## 联系方式

- 项目维护者：HGengwen
- 邮箱：hgwquxianyou_github@2925.com

## 版权声明

 Ollama Operation Used GUI是开源软件，遵循Apache许可证 2.0。
