import re
import paramiko
import time
import colorama
from colorama import init, Fore

l = []

mer = ['| ИАФ.2 |', '| ИАФ.3 |', '| ИАФ.4 |', '| УПД.6 |', '| АУД.3 |', '| УПД.4 |', '| ОПС.1 |', '| ЗНИ.7 |']
top = ['link/ether', '45', 'minlen=8lcredit=-1ucredit=-1dcredit=-1ocredit=-1gecoscheckreject_username', 
'per_userdeny=4unlock_time=300', 'restrict192.168.56.0mask255.255.255.0nomodifynotrap', 
'astra-admin:x:1001:rasuadmin', 'enabled', 'floppy:x:25:rasuadmin']

short_pause = 1

print('Сколько машин необходимо проверить?')

n = int(input())

if n == 1:
    #Узнаём адрес
    print('Введите ip адрес машины')
    host0 = input()
    l.append(host0)

i = 0
host = ""
if n > 1:
    while i < n:
        print('Введите ip адрес машины ', i)
        addr = input()
        hostname = host + addr
        l.append(hostname)
        i = i + 1

otchet = open("Otchet.txt", "w+") 

hostnames = l
for i, hostname in enumerate(hostnames):

    results = []

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username="rasuadmin", password="********") 

    ssh = client.invoke_shell()
    ssh.send("ip a | grep 'link/ether'\n")
    ssh.send("cat /etc/login.defs | grep 'PASS_MAX_DAYS'\n")
    ssh.send("cat /etc/pam.d/common-password | grep 'pam_cracklib.so minlen'\n")
    ssh.send("cat /etc/group | grep astra-admin\n")
    ssh.send("cat /etc/pam.d/common-auth | grep 'pam_tally.so per_user'\n")
    ssh.send("systemctl is-enabled networking.service\n")
    ssh.send("cat /etc/group | grep floppy\n")
    ssh.send("cat /etc/ntp.conf | grep 'restrict 192.168.56.0'\n")
    ssh.send("cat /var/log/auth.log | grep 'pam_unix.so(sudo:session)'\n")

    time.sleep(short_pause)
    
    k = ssh.recv(12000).decode("utf-8")

    client.close()

    s = str(k)

    # ИАФ.2
    pattern = r"link/ether"
    result = re.search(pattern, s)
    if result == None:
        result = 'None'
        results.append(result)
    else:
        result0 = result.group(0)
        results.append(result0)

    # ИАФ.3
    pattern = r"45"
    result1 = re.search(pattern, s)
    if result1 == None:
        result1 = 'None'
        results.append(result1)
    else:
        result2 = result1.group(0)
        results.append(result2)

    # Убираем пробелы из вывода
    pattern = r"\s"
    result3 = re.sub(pattern, "", s)

    result7 = re.search(r"per_userdeny=4unlock_time=300", result3)
    result13 = re.search(r"restrict192.168.56.0mask255.255.255.0nomodifynotrap", result3)
    result3 = re.search(r"minlen=8lcredit=-1ucredit=-1dcredit=-1ocredit=-1gecoscheckreject_username", result3)
    # ИАФ.4
    if result3 == None:
        result3 = 'None'
        results.append(result3)
    else:
        result4 = result3.group(0)
        results.append(result4)
    # УПД.6
    if result7 == None:
        result7 = 'None'
        results.append(result7)
    else:
        result8 = result7.group(0)
        results.append(result8)
    # АУД.3
    if result13 == None:
        result13 = 'None'
        results.append(result13)
    else:
        result14 = result13.group(0)
        results.append(result14)
    
    # УПД.4
    pattern = r"astra-admin:x:1001:rasuadmin"
    result5 = re.search(pattern, s)
    if result5 == None:
        result5 = 'None'
        results.append(result5)
    else:
        result6 = result5.group(0) 
        results.append(result6)

    # ОПС.1
    pattern = r"enabled"
    result9 = re.search(pattern, s)
    if result9 == None:
        result9 = 'None'
        results.append(result9)
    else:
        result10 = result9.group(0)
        results.append(result10)

    # ЗНИ.7
    pattern = r"floppy:x:25:rasuadmin"
    result11 = re.search(pattern, s)
    if result11 == None:
        result11 = 'None'
        results.append(result11)
    else:
        result12 = result11.group(0)
        results.append(result12)
    
    init(autoreset=True) 
    ok = Fore.GREEN + 'OK' 
    neok = Fore.RED + 'BAD'
    okresult = Fore.WHITE + ' | Проверка проведена успешно. Полученное значение соотвествует требованиям |'
    badresult = Fore.WHITE + '| Проверка не пройдена, требуется донастройка                              |'

    otchet = open("Otchet.txt", "a+")
    otchet.write('ПК - ')
    otchet.write(str(i)) 
    otchet.write(' - ') 
    otchet.write(hostname)
    otchet.write('\n')

    for j, res in enumerate(results):
        if res == top[j]:
            otchet = open("Otchet.txt", "a+")
            otchet.write(mer[j] + ok + okresult)
            otchet.write('\n')
        if res != top[j]:
            otchet = open("Otchet.txt", "a+")
            otchet.write(mer[j] + neok + badresult)
            otchet.write('\n')

with open("Otchet.txt", "r") as file: 
    content = file.read() 
    print(content)
