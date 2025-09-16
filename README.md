# UTM Generator

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
