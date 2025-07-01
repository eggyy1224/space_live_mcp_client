# Space Live MCP Client

## 什麼是 MCP (Model Context Protocol)？

MCP (Model Context Protocol) 是一個標準化的協議，讓 AI 模型能夠透過統一的介面與外部工具和系統進行交互。這個協議讓 AI 能夠：
- 呼叫外部 API 和工具
- 存取資料庫和檔案系統
- 控制應用程式和硬體設備
- 與其他服務進行即時通訊

## 專案架構

這是一個透過 **Gemini CLI** 所驅動的應用程式，採用了創新的 AI 導演模式：

### 🎬 AI 導演腦 (Gemini CLI + ReAct)
- **核心引擎**：使用 Gemini CLI 作為 AI 大腦
- **ReAct 能力**：結合推理 (Reasoning) 和行動 (Acting)，讓 AI 能夠：
  - 分析當前情況
  - 制定行動計劃
  - 執行具體操作
  - 根據結果調整策略

### 🛠️ 自建 MCP 工具集
我們開發了一套專門的 MCP 工具，讓 AI 導演能夠完全控制前端表演：

**角色控制工具**
- `set_emotion` - 控制角色情緒表情
- `set_main_character_animation` - 執行角色動畫
- `set_character_morph` - 調整角色外觀
- `set_body_shape` - 改變體型
- `set_head_size` - 調整頭部大小

**場景控制工具**
- `set_camera_preset` - 切換攝影機視角
- `set_light_intensity` - 調整燈光強度
- `set_monitor_content` - 控制場景螢幕內容

**多媒體生成工具**
- `send_message` - 生成對話內容
- `generate_sound_effect` - 即時產生音效
- `generate_image_overlay` - 創建圖片浮層
- `generate_background_image` - 生成背景圖片
- `play_song` - 播放音樂

**資訊整合工具**
- `GoogleSearch` - 即時搜尋網路資訊

### 🎭 運作流程

1. **AI 導演決策**：Gemini CLI 分析當前狀況，決定下一步行動
2. **MCP 工具呼叫**：透過我們的 MCP 工具集執行具體操作
3. **前端渲染**：接收 MCP 指令並即時渲染視覺效果
4. **反饋循環**：根據執行結果，AI 導演調整後續策略

## 技術特色

- **標準化協議**：基於 MCP 標準，確保工具的可擴展性和互操作性
- **AI 自主性**：透過 ReAct 框架，AI 能夠自主規劃和執行複雜的表演序列
- **即時互動**：所有操作都能即時反映到前端，創造流暢的使用者體驗
- **模組化設計**：每個 MCP 工具都是獨立模組，易於維護和擴展

## 開始使用

1. 確保已安裝 Gemini CLI
2. 啟動 MCP 伺服器
3. 連接前端渲染客戶端
4. 讓 AI 導演開始創作！

這個專案展示了 MCP 協議的強大潛力，以及 AI 在創意內容生成領域的無限可能性。 