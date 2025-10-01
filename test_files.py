import os
import webbrowser

file_path = os.path.abspath('data-dashboard.html')
print('HTML文件路径:', file_path)
print('文件存在:', os.path.exists(file_path))
print('JSON文件存在:', os.path.exists('data_results.json'))

# 检查文件大小
if os.path.exists('data-dashboard.html'):
    size = os.path.getsize('data-dashboard.html')
    print(f'HTML文件大小: {size} bytes')

if os.path.exists('data_results.json'):
    size = os.path.getsize('data_results.json')
    print(f'JSON文件大小: {size} bytes')