import whois

domain = "google.com"

info = whois.whois(domain)

print("Domain:", info.domain_name)
print("Registrar:", info.registrar)
print("Creation:", info.creation_date)
print("Expiry:", info.expiration_date)
print("Updated:", info.updated_date)
print("Name Servers:", info.name_servers)