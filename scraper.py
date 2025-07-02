# scraper.py
from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime

def get_weather_data():
    url = "https://videscentrs.lvgmc.lv/karte/Saldus/Saldus%2C%20Saldus%20nov./P125/22.493326/56.664915"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = context.new_page()
        page.set_default_timeout(45000)
        
        try:
            page.goto(url, wait_until="networkidle")
            
            try:
                page.click('text=Kopsavilkums', timeout=10000)
            except:
                pass
            
            selectors = [
                'div.tab-pane.active >> text=No plkst.',
                'div.weather-summary >> text=No plkst.',
                'div:has-text("No plkst.")',
                'text=No plkst.'
            ]
            
            summary_element = None
            for selector in selectors:
                try:
                    summary_element = page.locator(selector).first
                    summary_element.wait_for(state="visible", timeout=15000)
                    break
                except:
                    continue
            
            if not summary_element:
                return None
                
            summary_text = summary_element.inner_text()
            
            weather_data = {}
            lines = [line.strip() for line in summary_text.split('\n') if line.strip()]
            
            for i, line in enumerate(lines):
                if line == 'No plkst.':
                    weather_data['period'] = f"{lines[i]} {lines[i+1]} līdz {lines[i+3]} {lines[i+4]}"
                elif line == 'Saldus':
                    weather_data['temperature'] = lines[i+1]
                elif line == 'Nokrišņi':
                    weather_data['precipitation'] = lines[i+1]
                elif line == 'Vējš':
                    weather_data['wind_speed'] = lines[i+1]
                elif line == 'Vēja virziens':
                    weather_data['wind_direction'] = lines[i+1]
                elif line == 'Vējš brāzmās':
                    weather_data['wind_gusts'] = lines[i+1]
                elif line == 'Mitrums':
                    weather_data['humidity'] = lines[i+1]
                elif line == 'UV indekss':
                    weather_data['uv_index'] = lines[i+1]
                elif 'Skaidrs laiks.' in line:
                    weather_data['conditions'] = line
            
            return weather_data
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
        finally:
            browser.close()

def generate_html_report(weather_data):
    conditions = weather_data.get('conditions', '').lower()
    if 'lietus' in conditions:
        icon = '🌧️'
    elif 'mākoņains' in conditions:
        icon = '⛅'
    elif 'sniegs' in conditions:
        icon = '❄️'
    elif 'saulains' in conditions or 'skaidrs' in conditions:
        icon = '☀️'
    else:
        icon = '🌤️'
    
    html_content = f"""
<!DOCTYPE html>
<html lang="lv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laika ziņas - Saldus</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f9ff;
            color: #333;
        }}
        .weather-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }}
        .weather-icon {{
            font-size: 3rem;
            margin-right: 20px;
        }}
        .weather-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}
        .weather-item {{
            display: flex;
            align-items: center;
        }}
        .weather-item span {{
            margin-left: 10px;
        }}
        h1 {{
            color: #2c5282;
            margin: 0;
        }}
        .period {{
            color: #4a5568;
            font-size: 1.1rem;
            margin-top: 5px;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            font-size: 0.8rem;
            color: #718096;
        }}
    </style>
</head>
<body>
    <div class="weather-container">
        <div class="header">
            <div class="weather-icon">{icon}</div>
            <div>
                <h1>Laika ziņas - Saldus</h1>
                <div class="period">{weather_data.get('period', '')}</div>
            </div>
        </div>
        
        <div class="weather-info">
            <div class="weather-item">
                <strong>Temperatūra:</strong> <span>{weather_data.get('temperature', 'N/A')}</span>
            </div>
<!--            <div class="weather-item">
                <strong>Apstākļi:</strong> <span>{weather_data.get('conditions', 'N/A')}</span>
            </div> -->
            <div class="weather-item">
                <strong>Nokrišņi:</strong> <span>{weather_data.get('precipitation', 'N/A')}mm</span>
            </div>
            <div class="weather-item">
                <strong>Vējš:</strong> <span>{weather_data.get('wind_speed', 'N/A')}m/s {weather_data.get('wind_direction', '')}</span>
            </div>
            <div class="weather-item">
                <strong>Vēja brāzmas:</strong> <span>{weather_data.get('wind_gusts', 'N/A')}m/s</span>
            </div>
            <div class="weather-item">
                <strong>Mitrums:</strong> <span>{weather_data.get('humidity', 'N/A')}%</span>
            </div>
            <div class="weather-item">
                <strong>UV indekss:</strong> <span>{weather_data.get('uv_index', 'N/A')}</span>
            </div>
        </div>
        
        <div class="footer">
            Atjaunināts: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Dati: LVGMC
        </div>
    </div>
</body>
</html>
    """
    
    os.makedirs('output', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"output/laika_zinas_{timestamp}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

if __name__ == "__main__":
    max_attempts = 3
    weather = None
    
    for attempt in range(max_attempts):
        weather = get_weather_data()
        if weather:
            break
        time.sleep(5)
    
    if weather:
        print("\n=== LAIKA APSTĀKĻU KOPSAVILKUMS ===")
        print(f"Periods: {weather.get('period', 'N/A')}")
        print(f"Temperatūra: {weather.get('temperature', 'N/A')}")
#        print(f"Apstākļi: {weather.get('conditions', 'N/A')}")
        print(f"Nokrišņi: {weather.get('precipitation', 'N/A')}mm")
        print(f"Vējš: {weather.get('wind_speed', 'N/A')}m/s {weather.get('wind_direction', '')}")
        print(f"Vēja brāzmas: {weather.get('wind_gusts', 'N/A')}m/s")
        print(f"Mitrums: {weather.get('humidity', 'N/A')}%")
        print(f"UV indekss: {weather.get('uv_index', 'N/A')}")
        
        html_file = generate_html_report(weather)
        print(f"\nHTML report saved to: {html_file}")
    else:
        print("Failed to retrieve weather data")
