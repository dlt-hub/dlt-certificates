from markdown2 import markdown
from weasyprint import HTML

def generate_markdown_certificate(user_data: dict) -> str:
    markdown_template = f"""
# Certificate of Achievement: {user_data['certificate_name']}

## Awarded to 

![Course Image]({user_data['course']['image_url']})

### Certificate Details
- **Certificate ID**: 

### Course Information
- **Course**: [{user_data['course']['name']}]({user_data['course']['url']})

### Issued by
[**{user_data['issuer']['name']}**]({user_data['issuer']['url']}) 

### Certification Period
- **Issued**: 
- **Valid Until**: {user_data['valid_until']}

---

## Comments
The student has successfully completed the course. We commend their dedication and expertise in the field.

---

For more information, please visit [{user_data['issuer']['name']}]({user_data['issuer']['url']}).
    """
    return markdown_template


data_sample =  {
        "course": {
            "name": "Course ELT with dlt: dlt Fundamentals",
            "url": "https://dlthub.learnworlds.com/course/dlt-fundamentals",
            "image_url": "../certificates/badges/dlt_ELT_specialist.png"
        },
        "issuer": {
            "name": "dltHub",
            "url": "https://dlthub.com/"
        },
        "certificate_name": "dlt ELT Specialist",
        "valid_until": "No expiration",
    }


# Convert markdown to HTML
content_html = markdown(generate_markdown_certificate(data_sample))

full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {{
            margin: 20mm;
        }}
        body {{
            font-family: 'Helvetica Neue', sans-serif;
            margin: 20px;
            line-height: 1.4;
            color: #333;
            font-size: 13px;
        }}
        h1 {{
            text-align: left;
            font-size: 26px;
            margin: 12px 0 6px 0;
        }}
        h2 {{
            text-align: left;
            font-size: 20px;
            margin: 6px 0 4px 0;
        }}
        h3 {{
            font-size: 16px;
            margin-top: 24px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 4px;
        }}
        img {{
            display: block;
            margin: 16px auto;
            max-width: 180px;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
            margin: 0;
        }}
        li {{
            margin-bottom: 6px;
        }}
        p {{
            margin: 6px 0;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ccc;
            margin: 24px 0;
        }}
    </style>
</head>
<body>
{content_html}
</body>
</html>
"""

# Use a proper base URL if images are relative
HTML(string=full_html, base_url='.').write_pdf('certificate_pretty.pdf')
