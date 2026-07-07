import whois

def run_whois(domain):
    try:
        info = whois.whois(domain)

        print(info.domain_name)
        print(info.registrar)
        print(info.creation_date)
        print(info.expiration_date)

    except Exception as e:
        print(e)