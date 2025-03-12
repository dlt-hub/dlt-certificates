def generate_markdown_certificate(user_data: dict) -> str:
    markdown_template = f"""
# Certificate of Achievement: {user_data['certificate_name']}

## Awarded to **{user_data['user_name']}**

![Course Image]({user_data['course']['image_url']})

### Certificate Details
- **Certificate ID**: `{user_data['certificate_id']}`
- **Certificate Holder ID**: `{user_data['certificate_holder_id']}`

### Course Information
- **Course**: [{user_data['course']['name']}]({user_data['course']['url']})

### Issued by
[**{user_data['issuer']['name']}**]({user_data['issuer']['url']}) 

### Certification Period
- **Issued**: {user_data['certified_at']}
- **Valid Until**: {user_data['valid_until']}

---

## Contact Information
- **GitHub**: {user_data['github']}
- **Contact**: {user_data['contact']}

## Comments
{user_data['user_name']} has successfully completed the {user_data['course']['name']}. We commend their dedication and expertise in the field.

---

For more information, please visit [{user_data['issuer']['name']}]({user_data['issuer']['url']}).
    """
    return markdown_template
