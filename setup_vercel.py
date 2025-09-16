#!/usr/bin/env python3
"""
Script tự động tạo các files cần thiết để deploy UTM Generator lên Vercel
"""

import os
import json

def create_requirements():
    content = "Flask==2.3.3"
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Đã tạo requirements.txt")

def create_vercel_json():
    config = {
        "version": 2,
        "builds": [
            {
                "src": "./app.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/"
            }
        ]
    }
    
    with open('vercel.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print("✅ Đã tạo vercel.json")

def create_vercelignore():
    content = """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
node_modules/"""
    
    with open('.vercelignore', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Đã tạo .vercelignore")

def create_runtime_txt():
    content = "python-3.9.18"
    with open('runtime.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Đã tạo runtime.txt")

def create_readme():
    content = """# UTM Generator

Tool tao du lieu UTM tracking cho database testing

## Features
- Tao UTM parameters realistic
- Query strings dai >200 ky tu  
- Export SQL INSERT statements
- Download va copy de dang
- Deploy tren Vercel

## Live Demo
Deployed on Vercel: [Your URL here]

## Local Development
```bash
pip install -r requirements.txt
python app.py
```
Truy cap: http://localhost:5000/referrer_page

## Deploy len Vercel
1. Push code len GitHub
2. Import project tu https://vercel.com  
3. Deploy tu dong!

## Usage
1. Truy cap `/referrer_page`
2. Nhap so luong records
3. Tich "Tao du lieu dai" cho query strings >200 chars
4. Generate & download SQL

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** Vanilla HTML/CSS/JS
- **Deploy:** Vercel Serverless
- **Database:** MySQL/PostgreSQL compatible SQL

## Sample Output
```sql
INSERT INTO `680671148.202508_referrer` 
(id, date_added, referrer_id, url, url_id, parameter_pair_group_id, device, win_width, ipa, user_agent) 
VALUES
(1, '2025-08-22 14:30:45', 'abc123def456', 'https://google.com/?utm_source=google&utm_medium=organic&utm_campaign=spring_sale&gclid=...', '172502477', null, 'd', 1920, '0:0:0:0:0:0:0:1', 'Mozilla/5.0...');
```
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Đã tạo README.md")

def create_gitignore():
    content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
Thumbs.db

# Logs
*.log

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Vercel
.vercel"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Đã tạo .gitignore")

def main():
    print("Setup UTM Generator for Vercel deployment...")
    print()
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ Không tìm thấy app.py!")
        print("Hãy đảm bảo bạn chạy script này trong thư mục chứa app.py")
        return
    
    # Create all necessary files
    create_requirements()
    create_vercel_json()
    create_vercelignore()
    create_runtime_txt()
    create_readme()
    create_gitignore()
    
    print()
    print("Setup hoàn tất! Files đã tạo:")
    print("├── app.py (đã có)")
    print("├── requirements.txt ✅")
    print("├── vercel.json ✅")
    print("├── .vercelignore ✅")
    print("├── runtime.txt ✅")
    print("├── README.md ✅")
    print("└── .gitignore ✅")
    print()
    print("Bước tiếp theo:")
    print()
    print("1. Init Git & push lên GitHub:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'UTM Generator for Vercel'")
    print("   git remote add origin https://github.com/USERNAME/utm-generator.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("2. Deploy trên Vercel:")
    print("   • Vào https://vercel.com")
    print("   • Continue with GitHub")
    print("   • New Project → Import utm-generator")
    print("   • Deploy!")
    print()
    print("3. Test app:")
    print("   • URL sẽ có dạng: https://utm-generator-abc123.vercel.app")
    print("   • Truy cập: /referrer_page")
    print()
    print("Chúc bạn deploy thành công!")

if __name__ == "__main__":
    main()