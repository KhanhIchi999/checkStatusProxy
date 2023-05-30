import os
import requests
import time

filename = "listProxy.txt"
webCheck = 'http://icanhazip.com'
numberOfChecks = range(3)


def checkProxy():
    # read file proxyList
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r') as file:
        lines = file.readlines()

    error_messages = []  # Array to store proxy error messages
    proxies_to_check = []  # List to store proxies for rechecking
   
    for line in lines:
            data = line.strip().split(':')
            if len(data) >= 4:
                ip = data[0]
                port = data[1]
                user = data[2]
                password = data[3]
                print("IP:", ip)
                # print("Port:", port)
                # print("User:", user)
                # print("Password:", password)
                # print()

            proxies = {
                'http': f'http://{user}:{password}@{ip}:{port}',
                'https': f'https://{user}:{password}@{ip}:{port}'
            }

            try:
                start_time = time.time()
                response = requests.get(webCheck, proxies=proxies, timeout=5)
                end_time = time.time()
                if response.status_code == 200:
                    print("Proxy is working.")
                    response_time = end_time - start_time
                    print("Response Time:", response_time, "seconds")
                else:
                    print("Proxy is not working.")
                    error_messages.append(f"Proxy {ip}:{port} - Error: Non-200 status code")
                    proxies_to_check.append(proxies)

            except requests.exceptions.RequestException as e:
                print("Error occurred during request:", str(e))
                error_messages.append(f"Proxy {ip}:{port} - Error: {str(e)}")
                proxies_to_check.append(proxies)
            print()

    # Prompt for rechecking faulty proxies
    choice = input("Do you want to recheck faulty proxies? (Press Enter to continue): ")
    print()
    if choice.lower() == '':
        print("Rechecking Failed Proxies:")
        print()
        for proxy in proxies_to_check:
            print(f"Check Proxy : {proxy['http']}")
            print()
            for check in numberOfChecks:
                try:
                    start_time = time.time()
                    response = requests.get(webCheck, proxies=proxy, timeout=5)
                    end_time = time.time()

                    if response.status_code == 200:
                        print("Proxy is working.")
                        response_time = end_time - start_time
                        print("Response Time:", response_time, "seconds")
                        break
                    else:
                        print(f"({check + 1}) check - Proxy is still not working.")
                except requests.exceptions.RequestException as e:
                    print("Error occurred during request:", str(e))
                print()
    else:
        print("Skipping recheck of faulty proxies.")
checkProxy()