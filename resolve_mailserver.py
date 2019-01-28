import os
import sys
import dns.resolver    


DATA_PATH = "/Users/user/Desktop/"

def resolve_dns_record(domain, _type):
    try:
        return dns.resolver.query(domain, _type)        
    except:
        return False


def main():
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)

    domain_name = ""

    if len(sys.argv) == 2:
        domain_name = sys.argv[1]
    else:
        print("Enter domain_name:")
        domain_name = sys.stdin.readline().strip()
    
    name, ext = os.path.splitext(domain_name)
    save_path = DATA_PATH + name
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    else:
        print(save_path + " : Already exist.")
        sys.exit()
    mailserver_path = save_path + "/mailserver/"
    os.mkdir(mailserver_path)
    ip_path = save_path + "/ip/"
    os.mkdir(ip_path)
    mailserver_list = save_path + "/mailserver-List.txt"
    ip_list = save_path + "/ip-List.txt"

    domains = []
    with open(DATA_PATH + domain_name, "r") as f:
        domains = f.readlines()
    
    for index, domain in enumerate(domains):
        domain = domain.strip()
        print(str(index + 1) + ": " + domain)

        mailservers = resolve_dns_record(domain, "MX")
        if mailservers == False:
            continue
        for mailserver in mailservers:
            mailserver = mailserver.to_text().split(' ')
            mailserver = mailserver[1][:-1]

            with open(mailserver_path + domain + ".txt", "a") as f:
                f.write(mailserver + "\n")
            with open(mailserver_list, "a") as f:
                f.write(mailserver + "\n")

            ips = resolve_dns_record(mailserver, "A")
            if ips == False:
                continue
            for ip in ips:
                ip = ip.to_text()

                with open(ip_path + mailserver + ".txt", "a") as f:
                    f.write(ip + "\n")
                with open(ip_list, "a") as f:
                    f.write(ip + "\n")

    ip_list_uniq = save_path + "/ip-List-uniq.txt"
    command = "awk '!a[$0]++' " + ip_list + " > " + ip_list_uniq
    os.system(command)

if __name__ == "__main__":
    main()
