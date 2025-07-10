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
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'space-live-mcp-test'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# 記錄執行歷史
execution_history = []

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

def execute_gemini_command(user_input, execution_id):
    """執行 gemini CLI 命令"""
    try:
        # 構建命令
        command = [
            'gemini', '-y', '-p', 
            f'"@mcpclientprompt.md user_line={user_input}"'
        ]
        
        # 通知前端正在執行
        # 正確顯示包含引號的命令
        display_command = f'gemini -y -p "@mcpclientprompt.md user_line={user_input}"'
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
            universal_newlines=True
        )
        
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
        
        # 更新執行記錄
        execution_record = execution_history[execution_id - 1]
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
    print("=" * 50)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5001) 