from django.conf import settings

SUFFIX_GMAIL_TYPE = getattr(settings, 'SUFFIX_GMAIL_TYPE', [])

def clear_email(email):
    """
    Clear email like 'long.s.p.a.m.e.r+account@gmail.com' to
    'longspamer@gmail.com'.
    """
    email_username, email_domain = email.split('@')
    for suffix in SUFFIX_GMAIL_TYPE:
        if email_domain == suffix:
            plus_index = email_username.find('+')
            if plus_index != -1:
                email_username = email_username[:plus_index]
            email_username = email_username.replace('.', '')
            return '%s@%s' % (email_username, email_domain)
    return email

