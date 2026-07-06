import argparse
import markdown
import os
from xhtml2pdf import pisa
import base64

def generate_pdf(md_path, pdf_path, radar_path):
    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert MD to HTML
    html_content = markdown.markdown(md_text, extensions=['tables'])

    # Prepare Radar Image (base64) so xhtml2pdf renders it properly
    img_tag = ""
    if radar_path and os.path.exists(radar_path):
        with open(radar_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            img_tag = f'<div style="text-align: center;"><img src="data:image/png;base64,{encoded_string}" width="600" /></div>'
            
        # Replace the markdown image tag placeholder (if any) or just append it where it says "![Advanced Metrics Radar]"
        # To be safe, we can inject it right after the <h2> header for the radar chart
        html_content = html_content.replace('<h2>📊 核心数据碰撞与雷达图</h2>', f'<h2>📊 核心数据碰撞与雷达图</h2>{img_tag}')

    # HTML wrapper with SimHei font for Chinese characters
    html_template = f"""
    <html>
    <head>
    <style>
        @font-face {{
            font-family: 'SimHei';
            src: url('C:/Windows/Fonts/simhei.ttf');
        }}
        body {{
            font-family: 'SimHei', sans-serif;
            font-size: 14px;
            line-height: 1.6;
        }}
        h1 {{
            font-size: 24px;
            color: #333;
            text-align: center;
        }}
        h2 {{
            font-size: 18px;
            color: #0056b3;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #f4f4f4;
        }}
        ul {{
            margin-left: 20px;
        }}
    </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Save to PDF
    with open(pdf_path, "wb") as result_file:
        pisa_status = pisa.CreatePDF(html_template, dest=result_file)

    if pisa_status.err:
        print(f"Error occurred during PDF generation: {pisa_status.err}")
    else:
        print(f"PDF successfully generated at {pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--md", required=True, help="Input markdown file")
    parser.add_argument("--out", required=True, help="Output PDF file")
    parser.add_argument("--radar", required=False, help="Radar chart image to embed")
    args = parser.parse_args()
    
    generate_pdf(args.md, args.out, args.radar)
