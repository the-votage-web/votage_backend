import os
import re
import markdown
from xhtml2pdf import pisa

def convert_md_to_pdf(md_file_path, pdf_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Pre-process Mermaid code blocks to render cleanly in PDF
    def replace_mermaid(match):
        content = match.group(1).strip()
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Parse entities and relationships
        entities = []
        relations = []
        current_entity = None
        
        for line in lines:
            if line.startswith('erDiagram'):
                continue
            if '{' in line:
                current_entity = line.split('{')[0].strip()
                entities.append((current_entity, []))
            elif '}' in line:
                current_entity = None
            elif current_entity and len(entities) > 0:
                parts = line.split()
                if len(parts) >= 2:
                    entities[-1][1].append((parts[0], parts[1]))
            elif '||' in line or '}|' in line or '|{' in line:
                relations.append(line)

        html_out = ['<div class="erd-container">']
        html_out.append('<h3>Entity Relationship Diagram Summary</h3>')
        
        if relations:
            html_out.append('<h4>Entity Connections</h4><table class="erd-table"><thead><tr><th>Source Entity</th><th>Cardinality / Relation</th><th>Target Entity</th><th>Field</th></tr></thead><tbody>')
            for rel in relations:
                # e.g. Member ||--o{ FirstTimers : "member"
                match_rel = re.match(r'(\w+)\s+([\|\}\{o\-]+)\s+(\w+)\s*:\s*"(.*?)"', rel)
                if match_rel:
                    src, card, tgt, field = match_rel.groups()
                    card_desc = "One-to-Many" if "||--o{" in card else ("One-to-One" if "||--||" in card else ("Many-to-Many" if "}|--|{" in card else card))
                    html_out.append(f'<tr><td><strong>{src}</strong></td><td>{card_desc}</td><td><strong>{tgt}</strong></td><td><code>{field}</code></td></tr>')
                else:
                    html_out.append(f'<tr><td colspan="4"><code>{rel}</code></td></tr>')
            html_out.append('</tbody></table>')

        html_out.append('</div>')
        return '\n'.join(html_out)

    md_text = re.sub(r'```mermaid\n(.*?)```', replace_mermaid, md_text, flags=re.DOTALL)

    # Convert Markdown to HTML with extensions
    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'toc'])

    css_style = """
    @page {
        size: a4 portrait;
        margin: 1.5cm;
    }

    body {
        font-family: Helvetica, Arial, sans-serif;
        font-size: 10pt;
        line-height: 1.5;
        color: #1e293b;
        background-color: #ffffff;
    }

    h1 {
        font-size: 20pt;
        color: #0f172a;
        border-bottom: 2px solid #4f46e5;
        padding-bottom: 6px;
        margin-top: 0;
        margin-bottom: 12px;
    }

    h2 {
        font-size: 15pt;
        color: #1e1b4b;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 4px;
        margin-top: 18px;
        margin-bottom: 10px;
    }

    h3 {
        font-size: 13pt;
        color: #4338ca;
        margin-top: 14px;
        margin-bottom: 8px;
    }

    h4 {
        font-size: 11pt;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 6px;
    }

    p {
        margin-bottom: 8px;
        color: #334155;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 8px;
        margin-bottom: 14px;
        font-size: 8.5pt;
    }

    th {
        background-color: #4f46e5;
        color: #ffffff;
        font-weight: bold;
        text-align: left;
        padding: 6px 8px;
        border: 1px solid #4338ca;
    }

    td {
        padding: 5px 8px;
        border: 1px solid #e2e8f0;
        vertical-align: top;
    }

    tr:nth-child(even) td {
        background-color: #f8fafc;
    }

    code {
        font-family: Courier, monospace;
        font-size: 8.5pt;
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 1px 3px;
    }

    .erd-container {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 10px;
        margin-bottom: 16px;
    }

    .erd-table th {
        background-color: #0284c7;
        border-color: #0369a1;
    }
    """

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Django Data Models & Schema</title>
    <style>
    {css_style}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

    with open(pdf_file_path, "wb") as output_pdf:
        pisa_status = pisa.CreatePDF(full_html, dest=output_pdf)

    if pisa_status.err:
        print(f"Error creating PDF: {pisa_status.err}")
    else:
        print(f"PDF successfully created at: {pdf_file_path}")

if __name__ == "__main__":
    convert_md_to_pdf('/root/programs/votage_pg/church/DATA_MODELS.md', '/root/programs/votage_pg/church/DATA_MODELS.pdf')
