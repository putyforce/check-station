from ast import pattern
from sys import stderr, stdout
import time
from unittest import result
import paramiko
import re

from colorama import init, Fore 
from colorama import Back 
from colorama import Style 

# Инфа о машине, к которой удалённо подключаюсь

# Имя хоста или его ip адрес.
hostname = '192.168.56.103'
hostname1 = '192.168.56.104'
# Имя пользователя 
username = 'rasuadmin'
# Пароль пользователя
password = '********'
# По умолчанию paramiko выполняет аутентификацию по ключам, для отключения такого типа утентификации поставить значение False.
#look_for_keys = False
# Paramiko может подключаться к локальному SSH - агенту ОС. Это необходимо при работе с ключами. В данном случае утентификация
#происходит по логину и паролю, значит это надо отключить.
#allow_agent = False
short_pause = 1
port = 22

# Создаем клиент ssh. Этот класс представляет соединение с SSH сервером. Он выполняет аутентификацию клиента.
client = paramiko.SSHClient()
# Устанавливает, какую политику использовать, когда выполняется подключение к серверу, ключ которого неизвестен.
# AutoAddPolicy() - политика, которая автоматически добавляет новое имя хоста и ключ в локальный объект HostKeys.
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Метод, который выполняет подключение к SSH - серверу и аутентифицирует подключение.
client.connect(hostname=hostname, port=port, username=username, password=password) 

ssh = client.invoke_shell()

# Выполнить команду и вернуть результат
stdin, stdout, stderr = client.exec_command("cat /etc/pam.d/common-password | grep 'pam_cracklib.so retry'")

ssh.send("cat /etc/pam.d/common-password | grep 'pam_cracklib.so retry'\n")
time.sleep(short_pause)

k = ssh.recv(3000)
#print(k)

#data = stdout.read() + stderr.read()

#print(stdout.readlines)

client.close()

client1 = paramiko.SSHClient()
# Устанавливает, какую политику использовать, когда выполняется подключение к серверу, ключ которого неизвестен.
# AutoAddPolicy() - политика, которая автоматически добавляет новое имя хоста и ключ в локальный объект HostKeys.
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Метод, который выполняет подключение к SSH - серверу и аутентифицирует подключение.
client1.connect(hostname=hostname1, port=port, username=username, password=password) 


ssh = client1.invoke_shell()

# Выполнить команду и вернуть результат
stdin, stdout, stderr = client1.exec_command("cat /etc/pam.d/common-password | grep 'pam_cracklib.so retry'")

ssh.send("cat /etc/pam.d/common-password | grep 'pam_cracklib.so retry'\n")
time.sleep(short_pause)

k1 = ssh.recv(3000)
#print(k)

#data = stdout.read() + stderr.read()

#print(stdout.readlines)

client1.close()

#print(k)
#print(k1)

s = str(k)
s1 = str(k1)

pattern = r"retry=3 minlen=8 difok=3"
result = re.search(pattern, s)
result1 = re.search(pattern, s1)

#result0 = result.group(0)
#print(result)
#print(result1)
#result2 = result1.group(0)

#print(result1)

#print(result1 == "deny=8")
if result == None:
    result = "None"
else:
    result0 = result.group(0)

if result1 == None:
    result1 = "None"
else:
    result2 = result1.group(0)

init(autoreset=True) 

ok = Fore.GREEN + 'OK' 
neok = Fore.RED + 'BAD'
endresult = Fore.WHITE + ' | Проверка проведена успешно. Парольная политика соотвествует заданному значению |'
endresult1 = Fore.WHITE + ' | В процессе проверки выявлены следующие несоотвествия: ожидалось [retry=3 minlen=8 difok=3], получено [retry=3 minlen=8 difok=1] |'

my_file = open("Otchet.txt", "w+")

if result0 == "retry=3 minlen=8 difok=3":
    my_file.write('ПК 1 - ' + hostname)
    my_file.write('\n')
    my_file.write("| ИАФ.4 | " + ok + endresult)
    my_file.write('\n')

my_file = open("Otchet.txt", "a+")
    
if result1 != "retry=3 minlen=8 difok=3":
    my_file.write('ПК 2 - ' + hostname1)
    my_file.write('\n')
    my_file.write("| ИАФ.4 | " + neok + endresult1)
    my_file.write('\n')


my_file.close()

with open("Otchet.txt", "r") as file: 
    content = file.read() 
    print(content)