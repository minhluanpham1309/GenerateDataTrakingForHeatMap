#!/usr/bin/env python3
"""
Script fix lỗi 404 Vercel - Chuyển Flask app sang cấu trúc đúng
"""

import os
import shutil
import json

def create_api_folder():
    """Tạo thư mục api/"""
    if not os.path.exists('api'):
        os.makedirs('api')
        print("✅ Đã tạo thư mục api/")
    else:
        print("📁 Thư mục api/ đã tồn tại")

def create_api_index():
    """Tạo api/index.py với Flask app"""
    content = '''from flask import Flask, request, jsonify
import random, secrets, json
from datetime import datetime, timedelta

app = Flask(__name__)

# Minimal UTM generator
UTM_SOURCES = [
    {'source': 'google', 'weight': 20, 'medium': 'organic'},
    {'source': 'facebook', 'weight': 15, 'medium': 'social'},
    {'source': 'instagram', 'weight': 10, 'medium': 'social'},
    {'source': '-', 'weight': 5, 'medium': 'direct'}
]

CAMPAIGNS = ['spring_sale', 'product_launch', 'brand_awareness']

def generate_record(record_id, url_id, long_data=False):
    utm_data = random.choices(UTM_SOURCES, weights=[s['weight'] for s in UTM_SOURCES])[0]
    
    if utm_data['source'] == '-':
        url = '-'
    else:
        base_url = f"https://{utm_data['source']}.com/"
        
        if long_data:
            params = [
                f"utm_source={utm_data['source']}",
                f"utm_medium={utm_data['medium']}", 
                f"utm_campaign={random.choice(CAMPAIGNS)}"
            ]
            
            params.extend([
                f"utm_term={secrets.token_hex(12)}",
                f"utm_content={secrets.token_hex(15)}",
                f"utm_id={secrets.token_hex(8)}",
                f"utm_source_platform={utm_data['source']}_platform",
                f"utm_campaign_id={random.randint(100000, 999999)}",
                f"utm_adgroup={secrets.token_hex(10)}",
                f"utm_keyword={secrets.token_hex(8)}",
                f"gclid={secrets.token_hex(25)}",
                f"fbclid={secrets.token_hex(20)}",
                f"msclkid={secrets.token_hex(18)}",
                f"ttclid={secrets.token_hex(15)}",
                f"li_fat_id={secrets.token_hex(12)}",
                f"twclid={secrets.token_hex(14)}",
                f"ref={secrets.token_hex(6)}",
                f"affiliate_id={random.randint(10000, 99999)}",
                f"promo_code={secrets.token_hex(8)}",
                f"landing_page_variant=v{random.randint(1,10)}",
                f"audience_segment={secrets.token_hex(6)}",
                f"creative_id={secrets.token_hex(8)}",
                f"placement_id={secrets.token_hex(6)}",
                f"ad_position={random.choice(['top', 'sidebar', 'bottom', 'popup'])}",
                f"device_type={random.choice(['mobile', 'desktop', 'tablet'])}",
                f"session_id={secrets.token_hex(16)}",
            ])
            
            query_string = '&'.join(params)
            url = base_url + '?' + query_string
        else:
            url = f"{base_url}?utm_source={utm_data['source']}&utm_medium={utm_data['medium']}&utm_campaign={random.choice(CAMPAIGNS)}"
    
    return {
        'id': record_id,
        'date_added': '2025-08-22 ' + f"{random.randint(10,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
        'referrer_id': secrets.token_hex(16),
        'url': url,
        'url_id': url_id,
        'parameter_pair_group_id': 'null',
        'device': random.choice(['d', 'm', 't']),
        'win_width': random.choice([1920, 1366, 375, 768]),
        'ipa': '0:0:0:0:0:0:0:1',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

@app.route('/')
def home():
    return """
    <h1>UTM Generator</h1>
    <p>Tool tạo dữ liệu UTM tracking</p>
    <a href="/api/" style="color: #007bff; text-decoration: none; font-size: 18px;">
        → Vào UTM Generator
    </a>
    """

@app.route('/api/')
def referrer_page():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>UTM Generator</title>
    <style>body{font-family:Arial;max-width:800px;margin:0 auto;padding:20px}
    input,button{padding:10px;margin:5px;border:1px solid #ddd;border-radius:4px}
    button{background:#007bff;color:white;cursor:pointer}
    .output{margin-top:20px;padding:15px;background:#f8f9fa;border-radius:4px}
    </style>
    </head>
    <body>
        <h1>UTM Data Generator</h1>
        <form id="form">
            <div>
                <label>Số lượng:</label>
                <input type="number" id="count" value="1000" min="10" max="10000">
            </div>
            <div>
                <label>ID bắt đầu:</label>
                <input type="number" id="startId" value="1" min="1">
            </div>
            <div>
                <label>Tên bảng:</label>
                <input type="text" id="table" value="680671148.202508_referrer">
            </div>
            <div>
                <label>URL ID:</label>
                <input type="text" id="urlId" value="172502477">
            </div>
            <div>
                <label>
                    <input type="checkbox" id="longData"> 
                    Tạo dữ liệu dài (>200 ký tự)
                </label>
            </div>
            <button type="submit">Generate</button>
        </form>
        <div id="output" class="output" style="display:none">
            <h3>Kết quả:</h3>
            <button onclick="download()">Download SQL</button>
            <button onclick="copy()">Copy SQL</button>
            <textarea id="sql" style="width:100%;height:300px" readonly></textarea>
        </div>
        
        <script>
        let sqlData = '';
        document.getElementById('form').onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                record_count: document.getElementById('count').value,
                start_id: document.getElementById('startId').value,
                table_name: document.getElementById('table').value,
                url_id: document.getElementById('urlId').value,
                long_data: document.getElementById('longData').checked
            };
            
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            sqlData = await response.text();
            document.getElementById('sql').value = sqlData;
            document.getElementById('output').style.display = 'block';
        };
        
        function download() {
            const blob = new Blob([sqlData], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'utm_data.sql';
            a.click();
        }
        
        function copy() {
            document.getElementById('sql').select();
            document.execCommand('copy');
            alert('Đã copy!');
        }
        </script>
    </body>
    </html>"""

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    count = int(data.get('record_count', 1000))
    start_id = int(data.get('start_id', 1))
    table = data.get('table_name', 'test_table')
    url_id = data.get('url_id', '123')
    long_data = data.get('long_data', False)
    
    records = [generate_record(start_id + i, url_id, long_data) for i in range(count)]
    
    sql = f"-- Generated {count} UTM records (Long data: {'Yes' if long_data else 'No'})\\n"
    sql += f"INSERT INTO `{table}` (id, date_added, referrer_id, url, url_id, parameter_pair_group_id, device, win_width, ipa, user_agent) VALUES\\n"
    
    for i, r in enumerate(records):
        sql += f"({r['id']}, '{r['date_added']}', '{r['referrer_id']}', '{r['url']}', '{r['url_id']}', {r['parameter_pair_group_id']}, '{r['device']}', '{r['win_width']}', '{r['ipa']}', '{r['user_agent']}')"
        sql += "," if i < len(records)-1 else ";"
        sql += "\\n"
    
    return sql

# For Vercel
if __name__ == '__main__':
    app.run(debug=True)
'''
    
    with open('api/index.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print(" Đã tạo api/index.py")

def update_vercel_json():
    """Cập nhật vercel.json cho cấu trúc mới"""
    config = {
        "version": 2,
        "builds": [
            {
                "src": "api/index.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "api/index.py"
            }
        ]
    }
    
    with open('vercel.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print(" Đã cập nhật vercel.json")

def update_requirements():
    """Cập nhật requirements.txt"""
    content = """Flask==2.3.3
Werkzeug==2.3.6"""
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print(" Đã cập nhật requirements.txt")

def backup_old_app():
    """Backup app.py cũ"""
    if os.path.exists('app.py'):
        shutil.copy('app.py', 'app.py.backup')
        print(" Đã backup app.py -> app.py.backup")

def main():
    print(" Fix lỗi 404 Vercel - Chuyển sang cấu trúc đúng...")
    print()
    
    # Backup và tạo structure mới
    backup_old_app()
    create_api_folder()
    create_api_index()
    update_vercel_json()
    update_requirements()
    
    print()
    print(" Fix hoàn tất! Cấu trúc mới:")
    print("├── api/")
    print("│   └── index.py ")
    print("├── vercel.json  (updated)")
    print("├── requirements.txt  (updated)")
    print("└── app.py.backup (backup)")
    print()
    print(" Bước tiếp theo:")
    print("1. git add .")
    print("2. git commit -m 'Fix Vercel 404 - Update structure'")
    print("3. git push")
    print()
    print(" URL sau khi deploy:")
    print("• Home: https://your-app.vercel.app/")
    print("• UTM Generator: https://your-app.vercel.app/api/")
    print()
    print(" Vercel sẽ tự động redeploy!")

if __name__ == "__main__":
    main()