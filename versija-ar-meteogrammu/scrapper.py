from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime

def get_weather_data(page):
    try:
        # Switch to Kopsavilkums tab
        try:
            page.click('text=Kopsavilkums', timeout=10000)
            time.sleep(2)  # Wait for tab switch
        except:
            print("Kopsavilkums tab already active or not found")
            pass
        
        # Get weather summary data
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
        print(f"Weather data error: {str(e)}")
        return None

def get_meteogramma_screenshot(page):
    try:
        # Switch to Meteogramma tab
        tab_selectors = [
            'text=Meteogramma',
            'div.tab-link:has-text("Meteogramma")',
            'button:has-text("Meteogramma")',
            '//*[contains(text(), "Meteogramma")]'
        ]
        
        tab_found = False
        for selector in tab_selectors:
            try:
                page.click(selector, timeout=15000)
                print(f"Clicked Meteogramma tab using selector: {selector}")
                tab_found = True
                time.sleep(3)  # Wait for tab switch
                break
            except Exception as e:
                print(f"Failed to click with selector {selector}: {str(e)}")
                continue
        
        if not tab_found:
            print("Could not find Meteogramma tab")
            return None
        
        # Wait for Meteogramma content to load
        time.sleep(5)  # Important - give time for graph to render
        
        # Try to find the Meteogramma content
        content_selectors = [
            'div.meteogramma-container',
            'div.meteogram-container',
            'div.chart-container',
            'div.tab-content.active',
            'canvas',  # Directly target the canvas element
            'div.plot-container'
        ]
        
        for selector in content_selectors:
            try:
                content = page.locator(selector)
                content.wait_for(state="visible", timeout=20000)
                
                # Get bounding box with padding
                box = content.bounding_box()
                if not box:
                    continue
                
                # Add padding to the screenshot area
                padding = 20
                clip_area = {
                    'x': max(0, box['x'] - padding),
                    'y': max(0, box['y'] - padding),
                    'width': box['width'] + (2 * padding),
                    'height': box['height'] + (2 * padding)
                }
                
                # Create output directory
                os.makedirs('output', exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"output/meteogramma_{timestamp}.png"
                
                # Take screenshot
                page.screenshot(
                    path=screenshot_path,
                    clip=clip_area,
                    timeout=30000
                )
                
                print(f"Saved Meteogramma screenshot to: {screenshot_path}")
                return screenshot_path
                
            except Exception as e:
                print(f"Error with selector {selector}: {str(e)}")
                continue
        
        return None
        
    except Exception as e:
        print(f"Meteogramma error: {str(e)}")
        return None

def generate_html_report(weather_data):
    # Determine weather icon based on conditions
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
        .meteogram-link {{
            margin-top: 20px;
            text-align: center;
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
            <div class="weather-item">
                <strong>Apstākļi:</strong> <span>{weather_data.get('conditions', 'N/A')}</span>
            </div>
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
        
        <div class="meteogram-link">
            <p>Meteogramma pieejama zemāk:</p>
            <img src="{weather_data.get('meteogram_path', '')}" alt="Meteogramma" style="max-width: 100%;">
        </div>
        
        <div class="footer">
            Atjaunināts: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Dati: LVGMC
        </div>
    </div>
</body>
</html>
    """
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save HTML file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"output/laika_zinas_{timestamp}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def main():
    url = "https://videscentrs.lvgmc.lv/karte/Saldus/Saldus%2C%20Saldus%20nov./P125/22.493326/56.664915"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = context.new_page()
        page.set_default_timeout(60000)
        
        try:
            # Navigate to page
            print("Loading page...")
            page.goto(url, wait_until="networkidle")
            time.sleep(3)  # Wait for initial load
            
            # Get weather data from Kopsavilkums
            print("\n=== Getting weather summary ===")
            weather_data = None
            for attempt in range(3):
                weather_data = get_weather_data(page)
                if weather_data:
                    break
                time.sleep(5)
            
            if not weather_data:
                print("Failed to get weather data")
                return
            
            # Print weather summary to console
            print("\n=== LAIKA APTĀKĻU KOPSAVILKUMS ===")
            print(f"Periods: {weather_data.get('period', 'N/A')}")
            print(f"Temperatūra: {weather_data.get('temperature', 'N/A')}")
            print(f"Apstākļi: {weather_data.get('conditions', 'N/A')}")
            print(f"Nokrišņi: {weather_data.get('precipitation', 'N/A')}mm")
            print(f"Vējš: {weather_data.get('wind_speed', 'N/A')}m/s {weather_data.get('wind_direction', '')}")
            print(f"Vēja brāzmas: {weather_data.get('wind_gusts', 'N/A')}m/s")
            print(f"Mitrums: {weather_data.get('humidity', 'N/A')}%")
            print(f"UV indekss: {weather_data.get('uv_index', 'N/A')}")
            
            # Get Meteogramma screenshot
            print("\n=== Getting Meteogramma ===")
            meteogram_path = None
            for attempt in range(3):
                meteogram_path = get_meteogramma_screenshot(page)
                if meteogram_path:
                    weather_data['meteogram_path'] = os.path.basename(meteogram_path)
                    break
                time.sleep(5)
            
            # Generate HTML report
            html_file = generate_html_report(weather_data)
            print(f"\nHTML report saved to: {html_file}")
            
            if meteogram_path:
                print(f"Meteogramma screenshot saved to: {meteogram_path}")
            else:
                print("Failed to capture Meteogramma")
            
        except Exception as e:
            print(f"Critical error: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
