import argparse
import markdown
import os
import base64

def generate_html(md_path, html_path, radar_path):
    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert MD to HTML
    html_content = markdown.markdown(md_text, extensions=['tables'])

    # Prepare Radar Image (base64)
    img_tag = ""
    if radar_path and os.path.exists(radar_path):
        with open(radar_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            img_tag = f"""
            <div class="radar-container">
                <img src="data:image/png;base64,{encoded_string}" alt="Radar Chart" />
            </div>
            """
            
        # Inject radar chart right after the core data header
        html_content = html_content.replace('<h2>📊 核心数据碰撞与雷达图</h2>', f'<h2>📊 核心数据碰撞与雷达图</h2>{img_tag}')

    # Premium HTML wrapper with Rich Aesthetics
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Football Prediction Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-primary: #1f2937;
            --text-secondary: #4b5563;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --border: #e5e7eb;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.7;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
        }}

        .report-container {{
            max-width: 900px;
            margin: 40px auto;
            background: var(--card-bg);
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            padding: 50px 60px;
            overflow: hidden;
            position: relative;
        }}
        
        .report-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 6px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        }}

        h1 {{
            font-size: 2.2rem;
            font-weight: 700;
            color: #111827;
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--border);
        }}

        h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--accent);
            margin-top: 40px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }}

        p {{
            color: var(--text-secondary);
            margin-bottom: 16px;
        }}

        ul {{
            margin-bottom: 20px;
            padding-left: 24px;
            color: var(--text-secondary);
        }}

        li {{
            margin-bottom: 8px;
        }}

        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 30px 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}

        th {{
            background-color: #f8fafc;
            font-weight: 600;
            color: #334155;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        .radar-container {{
            text-align: center;
            margin: 40px 0;
            padding: 20px;
            background: #f8fafc;
            border-radius: 12px;
            border: 1px solid var(--border);
            transition: transform 0.3s ease;
        }}
        
        .radar-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }}

        .radar-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}

        .fab-print {{
            position: fixed;
            bottom: 40px;
            right: 40px;
            background: linear-gradient(135deg, #2563eb, #4f46e5);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 16px 28px;
            font-size: 16px;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.39);
            transition: all 0.2s ease-in-out;
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 1000;
        }}

        .fab-print:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
        }}
        
        .fab-print:active {{
            transform: translateY(1px);
        }}

        /* Print Specific Styles */
        @media print {{
            body {{
                background-color: white;
            }}
            .report-container {{
                box-shadow: none;
                margin: 0;
                padding: 0;
                max-width: 100%;
            }}
            .report-container::before {{
                display: none;
            }}
            .fab-print {{
                display: none !important;
            }}
            .radar-container {{
                border: none;
                background: transparent;
                padding: 0;
            }}
        }}
    </style>
</head>
<body>

    <div class="report-container">
        {html_content}
    </div>

    <!-- Floating Action Button for PDF Export -->
    <button class="fab-print no-print" onclick="window.print()">
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
        </svg>
        Export PDF
    </button>

</body>
</html>
"""

    # Save to HTML
    with open(html_path, "w", encoding="utf-8") as result_file:
        result_file.write(html_template)

    print(f"Beautiful HTML report successfully generated at {html_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--md", required=True, help="Input markdown file")
    parser.add_argument("--out", required=True, help="Output HTML file")
    parser.add_argument("--radar", required=False, help="Radar chart image to embed")
    args = parser.parse_args()
    
    generate_html(args.md, args.out, args.radar)
