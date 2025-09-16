from flask import Flask, request, jsonify
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
            # Tạo URL dài 200-400 ký tự bằng cách giới hạn số parameter
            params = [
                f"utm_source={utm_data['source']}",
                f"utm_medium={utm_data['medium']}", 
                f"utm_campaign={random.choice(CAMPAIGNS)}"
            ]
            
            # Thêm một số parameter với token ngắn hơn để giữ độ dài 200-400 ký tự
            params.extend([
                f"utm_term={secrets.token_hex(6)}",  # Giảm từ 12 xuống 6
                f"utm_content={secrets.token_hex(8)}",  # Giảm từ 15 xuống 8
                f"utm_id={secrets.token_hex(4)}",  # Giảm từ 8 xuống 4
                f"utm_campaign_id={random.randint(10000, 99999)}",  # Số ngắn hơn
                f"utm_adgroup={secrets.token_hex(5)}",  # Giảm từ 10 xuống 5
                f"gclid={secrets.token_hex(12)}",  # Giảm từ 25 xuống 12
                f"fbclid={secrets.token_hex(10)}",  # Giảm từ 20 xuống 10
                f"ref={secrets.token_hex(4)}",  # Giảm từ 6 xuống 4
                f"promo_code={secrets.token_hex(4)}",  # Giảm từ 8 xuống 4
                f"device_type={random.choice(['mobile', 'desktop', 'tablet'])}",
                f"session_id={secrets.token_hex(8)}",  # Giảm từ 16 xuống 8
            ])
            
            query_string = '&'.join(params)
            url = base_url + '?' + query_string
            
            # Kiểm tra và điều chỉnh độ dài nếu cần
            if len(url) > 400:
                # Nếu vẫn quá dài, loại bỏ một số parameter
                params = params[:10]  # Chỉ giữ 10 parameter đầu
                query_string = '&'.join(params)
                url = base_url + '?' + query_string
            elif len(url) < 200:
                # Nếu quá ngắn, thêm parameter để đạt ít nhất 200 ký tự
                params.append(f"extra_param={secrets.token_hex(10)}")
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
    .info{background:#e3f2fd;padding:10px;border-radius:4px;margin:10px 0;}
    </style>
    </head>
    <body>
        <h1>UTM Data Generator</h1>
        <div class="info">
            <strong>Lưu ý:</strong> Dữ liệu dài sẽ tạo URL có độ dài 200-400 ký tự
        </div>
        <form id="form">
            <div>
                <label>Số lượng:</label>
                <input type="number" id="count" value="1000" min="10" max="1000000">
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
                    Tạo dữ liệu dài (200-400 ký tự)
                </label>
            </div>
            <button type="submit">Generate</button>
        </form>
        <div id="output" class="output" style="display:none">
            <h3>Kết quả:</h3>
            <div id="stats" class="info"></div>
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
            
            const result = await response.json();
            sqlData = result.sql;
            document.getElementById('sql').value = sqlData;
            document.getElementById('stats').innerHTML = 
                `<strong>Thống kê URL:</strong><br/>
                Độ dài trung bình: ${result.avg_length} ký tự<br/>
                Độ dài min: ${result.min_length} ký tự<br/>
                Độ dài max: ${result.max_length} ký tự<br/>
                Số URL dài (>200): ${result.long_urls_count}`;
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
    
    # Tính toán thống kê độ dài URL
    url_lengths = [len(r['url']) for r in records if r['url'] != '-']
    avg_length = sum(url_lengths) / len(url_lengths) if url_lengths else 0
    min_length = min(url_lengths) if url_lengths else 0
    max_length = max(url_lengths) if url_lengths else 0
    long_urls_count = len([l for l in url_lengths if l > 200])
    
    sql = f"-- Generated {count} UTM records (Long data: {'Yes' if long_data else 'No'})\n"
    sql += f"-- URL Length Stats: Avg={avg_length:.0f}, Min={min_length}, Max={max_length}, Long URLs(>200)={long_urls_count}\n"
    sql += f"INSERT INTO `{table}` (id, date_added, referrer_id, url, url_id, parameter_pair_group_id, device, win_width, ipa, user_agent) VALUES\n"
    
    for i, r in enumerate(records):
        sql += f"({r['id']}, '{r['date_added']}', '{r['referrer_id']}', '{r['url']}', '{r['url_id']}', {r['parameter_pair_group_id']}, '{r['device']}', '{r['win_width']}', '{r['ipa']}', '{r['user_agent']}')"
        sql += "," if i < len(records)-1 else ";"
        sql += "\n"
    
    return jsonify({
        'sql': sql,
        'avg_length': round(avg_length, 1),
        'min_length': min_length,
        'max_length': max_length,
        'long_urls_count': long_urls_count
    })

# For Vercel
if __name__ == '__main__':
    app.run(debug=True)