# Space Live MCP Test - Web Interface

## 🚀 功能概述

這是一個簡潔的 Web 介面，允許您透過瀏覽器輸入指令，系統會自動執行 `gemini CLI` 命令並即時顯示結果。

## 🏗️ 系統架構

```
前端 (HTML/JavaScript) ← WebSocket → Flask 後端 → 執行 gemini CLI
                                ↓
                        即時回傳執行結果
```

## 📦 安裝步驟

### 1. 確保虛擬環境已啟動

```bash
# 如果尚未啟動虛擬環境，請先啟動
source venv/bin/activate
```

### 2. 安裝依賴包

```bash
pip install -r requirements.txt
```

### 3. 確認 gemini CLI 可用

```bash
# 測試 gemini CLI 是否正常運作
gemini --help
```

## 🎯 使用方法

### 1. 啟動 Web 服務器

```bash
python app.py
```

系統會顯示以下訊息：
```
🚀 Space Live MCP Test Web Interface
📡 服務器啟動中...
🌐 訪問 http://localhost:5000
📝 輸入您的指令，系統將執行 gemini CLI
==================================================
```

### 2. 開啟瀏覽器

訪問 `http://localhost:5000`

### 3. 使用介面

1. **命令輸入區**：
   - 在輸入框中輸入您的指令
   - 按 Enter 或點擊「執行」按鈕

2. **即時輸出區**：
   - 顯示 gemini CLI 的即時執行結果
   - 綠色文字：標準輸出
   - 紅色文字：錯誤輸出
   - 藍色文字：系統訊息

3. **執行狀態**：
   - 🟠 執行中
   - 🟢 執行完成
   - 🔴 執行失敗

4. **執行歷史**：
   - 點擊「執行歷史」查看所有執行記錄
   - 可展開查看詳細輸出

## 🔧 系統運作原理

### 執行流程

1. 用戶在前端輸入指令
2. 前端透過 WebSocket 傳送至 Flask 後端
3. 後端構建完整的 gemini CLI 命令：
   ```bash
   gemini -y -p "@mcpclientprompt.md user_line='使用者輸入'"
   ```
4. 在背景執行程序並即時回傳輸出
5. 前端即時顯示執行結果

### 技術特點

- **即時通信**：使用 WebSocket 確保即時性
- **背景執行**：不會阻塞用戶介面
- **狀態追蹤**：完整記錄執行狀態和結果
- **歷史記錄**：持久化保存執行歷史
- **響應式設計**：支援各種螢幕尺寸

## 🎨 功能特色

### 主要功能

- ✅ **即時輸出**：gemini CLI 的輸出即時顯示
- ✅ **狀態監控**：清楚顯示執行狀態
- ✅ **歷史記錄**：完整保存執行歷史
- ✅ **錯誤處理**：完善的錯誤提示和處理
- ✅ **響應式設計**：美觀的現代化界面

### 安全特性

- 🔒 **本地執行**：僅在本地網路運行
- 🔒 **輸入驗證**：基本的輸入驗證機制
- 🔒 **進程隔離**：每個命令在獨立進程中執行

## 📊 使用範例

### 範例指令

```
開始一個太空主題的表演
```

系統會執行：
```bash
gemini -y -p "@mcpclientprompt.md user_line='開始一個太空主題的表演'"
```

### 預期輸出

前端會即時顯示 gemini CLI 的所有輸出，包括：
- MCP 工具的執行過程
- 系統回應訊息
- 錯誤訊息（如果有）

## 🛠️ 疑難排解

### 常見問題

1. **服務器啟動失敗**
   ```bash
   # 確認虛擬環境已啟動
   source venv/bin/activate
   
   # 重新安裝依賴包
   pip install -r requirements.txt
   ```

2. **gemini CLI 無法執行**
   ```bash
   # 確認 gemini CLI 已安裝並可用
   gemini --help
   
   # 檢查 mcpclientprompt.md 檔案是否存在
   ls -la mcpclientprompt.md
   ```

3. **WebSocket 連接失敗**
   - 確認防火牆設定
   - 檢查 5000 端口是否被占用
   - 嘗試重新啟動服務器

### 錯誤代碼

- **返回碼 0**：執行成功
- **返回碼 非0**：執行失敗，檢查錯誤輸出

## 📝 開發說明

### 檔案結構

```
space_live_mcp_test/
├── app.py                    # Flask 後端主程式
├── requirements.txt          # Python 依賴包
├── mcpclientprompt.md       # gemini CLI 的 prompt 檔案
├── templates/
│   ├── index.html           # 主頁面模板
│   └── history.html         # 歷史記錄頁面
└── venv/                    # Python 虛擬環境
```

### 擴展功能

如需增加功能，可以修改：
- `app.py`：後端邏輯
- `templates/index.html`：前端界面
- `templates/history.html`：歷史記錄頁面

## 🎉 開始使用

1. 啟動虛擬環境：`source venv/bin/activate`
2. 安裝依賴：`pip install -r requirements.txt`
3. 啟動服務器：`python app.py`
4. 開啟瀏覽器：`http://localhost:5000`
5. 輸入指令並享受即時的 gemini CLI 體驗！

---

**注意**: 這個系統設計為本地使用，請勿在生產環境中直接使用。如需部署到網路環境，請先進行安全性評估和加固。 