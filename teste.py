def remove_domain_from_email(email):
    if '@' in email:
        return email.split('@')[0]
    return email

email = "williamjohny05@gmail.com"
username = remove_domain_from_email(email)
print(username) 