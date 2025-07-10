#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Space Live MCP Test - Web Interface
簡潔的前端介面，用於執行 gemini CLI 命令
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess
import os
import threading
import json
import signal
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'space-live-mcp-test'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# 記錄執行歷史和當前進程
execution_history = []
current_processes = {}  # 保存當前執行的進程
process_lock = threading.Lock()

def load_prompt_content():
    """讀取 mcpclientprompt.md 的完整內容"""
    try:
        with open('mcpclientprompt.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("警告: 找不到 mcpclientprompt.md 檔案，使用預設內容")
        return "# MCP Client Prompt\n\n用戶輸入："
    except Exception as e:
        print(f"讀取 mcpclientprompt.md 失敗: {e}")
        return "# MCP Client Prompt\n\n用戶輸入："

# 載入 prompt 內容
PROMPT_CONTENT = load_prompt_content()
print(f"✅ 已載入 prompt 內容 ({len(PROMPT_CONTENT)} 字符)")

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/history')
def history():
    """執行歷史頁面"""
    return render_template('history.html', history=execution_history)

@socketio.on('execute_command')
def handle_execute_command(data):
    """處理前端傳來的命令執行請求"""
    user_input = data.get('input', '').strip()
    
    if not user_input:
        emit('error', {'message': '請輸入內容'})
        return
    
    # 記錄開始執行
    execution_id = len(execution_history) + 1
    execution_record = {
        'id': execution_id,
        'user_input': user_input,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'running',
        'output': '',
        'error': ''
    }
    execution_history.append(execution_record)
    
    # 通知前端開始執行
    emit('execution_started', {
        'id': execution_id,
        'user_input': user_input,
        'timestamp': execution_record['timestamp']
    })
    
    # 在背景執行命令
    threading.Thread(
        target=execute_gemini_command,
        args=(user_input, execution_id),
        daemon=True
    ).start()

@socketio.on('stop_execution')
def handle_stop_execution(data):
    """處理停止執行請求"""
    execution_id = data.get('id')
    
    with process_lock:
        if execution_id in current_processes:
            process = current_processes[execution_id]
            try:
                # 嘗試優雅地終止進程
                process.terminate()
                # 等待一段時間後強制殺死
                threading.Timer(5.0, lambda: process.kill() if process.poll() is None else None).start()
                
                # 更新執行記錄
                if execution_id <= len(execution_history):
                    execution_record = execution_history[execution_id - 1]
                    execution_record['status'] = 'stopped'
                    execution_record['error'] = '用戶中斷執行'
                
                # 通知前端
                emit('execution_stopped', {
                    'id': execution_id,
                    'message': '執行已停止'
                })
                
                # 清理進程記錄
                del current_processes[execution_id]
                
            except Exception as e:
                emit('error', {'message': f'停止執行失敗: {str(e)}'})
        else:
            emit('error', {'message': '找不到要停止的執行序列'})

def execute_gemini_command(user_input, execution_id):
    """執行 gemini CLI 命令"""
    try:
        # 構建完整的 prompt，將 mcpclientprompt.md 內容和用戶輸入結合
        full_prompt = PROMPT_CONTENT + f"\n\n用戶輸入：{user_input}"
        
        # 構建命令 - 直接傳遞 prompt 內容
        command = ['gemini', '-y', '-p', full_prompt]
        
        # 通知前端正在執行
        display_command = f'gemini -y -p "{{prompt內容}} user_line={user_input}"'
        socketio.emit('execution_progress', {
            'id': execution_id,
            'message': f'正在執行: {display_command}'
        })
        
        # 執行命令
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            preexec_fn=os.setsid if os.name != 'nt' else None  # 創建進程組以便停止
        )
        
        # 保存進程引用
        with process_lock:
            current_processes[execution_id] = process
        
        # 即時讀取輸出
        stdout_lines = []
        stderr_lines = []
        
        # 讀取標準輸出
        for line in iter(process.stdout.readline, ''):
            if line:
                stdout_lines.append(line.rstrip())
                socketio.emit('execution_output', {
                    'id': execution_id,
                    'line': line.rstrip(),
                    'type': 'stdout'
                })
        
        # 等待程序結束
        process.wait()
        
        # 讀取標準錯誤（如果有）
        stderr_output = process.stderr.read()
        if stderr_output:
            stderr_lines = stderr_output.split('\n')
            for line in stderr_lines:
                if line.strip():
                    socketio.emit('execution_output', {
                        'id': execution_id,
                        'line': line.strip(),
                        'type': 'stderr'
                    })
        
        # 清理進程記錄
        with process_lock:
            if execution_id in current_processes:
                del current_processes[execution_id]
        
        # 更新執行記錄
        execution_record = execution_history[execution_id - 1]
        if execution_record['status'] != 'stopped':  # 如果沒有被手動停止
            execution_record['status'] = 'completed'
            execution_record['output'] = '\n'.join(stdout_lines)
            execution_record['error'] = stderr_output
            execution_record['return_code'] = process.returncode
            
            # 通知前端執行完成
            socketio.emit('execution_completed', {
                'id': execution_id,
                'return_code': process.returncode,
                'success': process.returncode == 0
            })
        
    except Exception as e:
        # 處理執行錯誤
        error_msg = f'執行錯誤: {str(e)}'
        
        # 清理進程記錄
        with process_lock:
            if execution_id in current_processes:
                del current_processes[execution_id]
        
        # 更新執行記錄
        if execution_id <= len(execution_history):
            execution_record = execution_history[execution_id - 1]
            execution_record['status'] = 'error'
            execution_record['error'] = error_msg
        
        # 通知前端錯誤
        socketio.emit('execution_error', {
            'id': execution_id,
            'error': error_msg
        })

@socketio.on('connect')
def handle_connect():
    """客戶端連接"""
    emit('connected', {'message': 'WebSocket 連接成功'})

@socketio.on('disconnect')
def handle_disconnect():
    """客戶端斷開連接"""
    print('客戶端斷開連接')

if __name__ == '__main__':
    print("🚀 Space Live MCP Test Web Interface")
    print("📡 服務器啟動中...")
    print("🌐 訪問 http://localhost:5001")
    print("📝 輸入您的指令，系統將執行 gemini CLI")
    print(f"📋 已載入 prompt 模板 ({len(PROMPT_CONTENT)} 字符)")
    print("=" * 50)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001) 