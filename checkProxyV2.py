import os
import requests
import time

filename = "listProxy.txt"
webCheck = 'http://icanhazip.com'
numberOfChecks = range(3)
result_file = "resultCheck.txt"  # New file for exporting results


def checkProxy(result_file):
    # Read the proxy list file
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r') as file:
        lines = file.readlines()

    error_messages = []  # Array to store proxy error messages
    proxies_to_check = []  # List to store proxies for rechecking

    result_lines = []  # List to store result lines for exporting

    result_lines.append("IP              Status         Response Time\n")  # Header line of file

    for line in lines:
        data = line.strip().split(':')
        if len(data) >= 4:
            ip = data[0]
            port = data[1]
            user = data[2]
            password = data[3]
            print("IP:", ip)

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
                    status = "Working"
                    result_line = "{ip:<15} {status:<13} {response_time:<10.4f} seconds\n".format(
                        ip=ip, status=status, response_time=response_time
                    )
                    result_lines.append(result_line)
                else:
                    print("Proxy is not working.")
                    error_messages.append(f"Proxy {ip}:{port} - Error: Non-200 status code")
                    proxies_to_check.append(proxies)

            except requests.exceptions.RequestException as e:
                print("Error occurred during request:", str(e))
                error_messages.append(f"Proxy {ip}:{port} - Error: {str(e)}")
                proxies_to_check.append(proxies)

            print()

    # Export results to file
    result_filepath = os.path.join(os.path.dirname(__file__), result_file)
    with open(result_filepath, 'w') as result_file:
        for line in result_lines:
            result_file.write(line)

    # Prompt for rechecking faulty proxies
    choice = input("Do you want to recheck faulty proxies? (Press Enter to continue): ")
    print()
    if choice.lower() == '':
        print("Rechecking Failed Proxies:")
        print()
        for proxy in proxies_to_check:
            print(f"Check Proxy: {proxy['http']}")
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
                        proxies_to_check.remove(proxy)
                        break
                    else:
                        print(f"({check + 1}) check - Proxy is still not working.")
                except requests.exceptions.RequestException as e:
                    print("Error occurred during request:", str(e))
                print()
    else:
        print("Skipping recheck of faulty proxies.")
    
    with open(result_filepath, "a") as file:
        file.write("                Proxy is not working\n")
        for proxy in proxies_to_check:
            file.write(str(proxy) + "\n")



        

checkProxy(result_file)
