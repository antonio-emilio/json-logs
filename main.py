import subprocess
import json
import csv
import os
from datetime import datetime
import ping3

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()

while True:
    # Execute o comando ping para obter a latência
    latency = ping3.ping('18.231.164.139')

    # Execute o comando iperf3
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_filename = f"log_{timestamp}.json"
    iperf_command = f'echo "Hello, world!" | iperf3 -c 18.231.164.139 -u -b 10M -i 1 -t 5 -J --logfile {log_filename}'
    process = subprocess.Popen(iperf_command, shell=True)
    process.wait()  # Aguardar o término do comando iperf3

    # Verificar o código de retorno do comando iperf3
    if process.returncode != 0:
        print("Erro ao executar o comando iperf3.")
        continue  # Reiniciar o loop se houver um erro

    # Ler o conteúdo do arquivo JSON gerado pelo iperf3
    with open(log_filename, 'r') as json_file:
        iperf_data = json.load(json_file)

    # Adicionar informação de ping ao JSON
    iperf_data['ping_latency_s'] = latency

    # Salvar o arquivo JSON atualizado
    with open(log_filename, 'w') as json_file:
        json.dump(iperf_data, json_file)

    # Mover o arquivo JSON resultante para a pasta json-logs
    if not os.path.exists('json-logs'):
        os.makedirs('json-logs')

    os.rename(log_filename, os.path.join('json-logs', log_filename))

    # Navegar para a pasta json-logs
    os.chdir('json-logs')

    # Executar os comandos git add . e git commit -m "feat"
    git_add_command = 'git add .'
    run_command(git_add_command)

    git_commit_command = 'git commit -m "feat"'
    run_command(git_commit_command)

    # Executar o comando git push
    git_push_command = 'git push origin main'  # Altere 'main' para o nome da sua branch principal
    run_command(git_push_command)

    print(f"Arquivo JSON movido para json-logs, commit realizado localmente e push efetuado para o GitHub às {datetime.now()}.")

    # Aguardar um intervalo antes de iniciar o próximo loop (por exemplo, a cada 5 minutos)
    import time
    time.sleep(300)  # Esperar 300 segundos (5 minutos) antes de iniciar o próximo loop
