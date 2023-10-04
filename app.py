import subprocess
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
        logging.info(f'Command executed successfully: {command}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Command failed: {command}, Error: {str(e)}')

def setup_packages():
    command = (
        "apt-get update && "
        "apt-get install -y openssh-client git curl tmux vim zsh wget locales && "
        "apt-get clean && "
        "rm -rf /var/lib/apt/lists/*"
    )
    run_command(command)

def setup_locale():
    commands = [
        'echo "en_US.UTF-8 UTF-8" > /etc/locale.gen',
        'locale-gen en_US.UTF-8',
        'update-locale LANG=en_US.UTF-8'
    ]
    for command in commands:
        run_command(command)

def setup_environment():
    commands = [
        'echo "ENV LANG=en_US.UTF-8" >> $HOME/.bashrc',
        'echo "ENV GIT_SSH_COMMAND=\\"ssh -o StrictHostKeyChecking=no\\"" >> $HOME/.bashrc',
        'export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"'
    ]
    for command in commands:
        run_command(command)


def repair_key_format(decoded_key: bytes) -> bytes:
    # Убедитесь, что ключ начинается и заканчивается правильными маркерами
    header = b"-----BEGIN OPENSSH PRIVATE KEY-----"
    footer = b"-----END OPENSSH PRIVATE KEY-----"
    
    # Удалить все возможные маркеры и пробелы
    key_body = decoded_key.replace(header, b"").replace(footer, b"").strip()
    
    # Объединить маркеры и ключ, добавив переносы строк
    repaired_key = header + b"\n" + key_body + b"\n" + footer + b"\n"
    
    return repaired_key




def setup_ssh():
    ssh_dir = '/root/.ssh'
    os.makedirs(ssh_dir, exist_ok=True)
    
    # Замените следующую строку вашим ключом в формате bytes
    raw_key = b"""
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACC9COV4NTs7H+Vs3++oGCTQizHfKH0GBTBFqddXdxlMQQAAAJjPXDqwz1w6
sAAAAAtzc2gtZWQyNTUxOQAAACC9COV4NTs7H+Vs3++oGCTQizHfKH0GBTBFqddXdxlMQQ
AAAEB/mrkSCcTIGVKx27jGS4PbhLJOsZdsOdwptQwOTc25eb0I5Xg1Ozsf5Wzf76gYJNCL
Md8ofQYFMEWp11d3GUxBAAAAEWFydWRAdmVsZXNic2QuY29tAQIDBA==
-----END OPENSSH PRIVATE KEY-----
"""
    
    # Используйте функцию repair_key_format для исправления формата ключа
    repaired_key = repair_key_format(raw_key)
    
    # Запись исправленного ключа в файл
    with open(f'{ssh_dir}/dev_key', 'wb') as file:
        file.write(repaired_key)
    
    run_command(f'echo github.com,140.82.121.3 ssh-ed25519 SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU >> {ssh_dir}/known_hosts')


def clone_repo():
    run_command('git clone -b dev1 git@github.com:velesbsdllc/ssh-vair.git')

def main():
    setup_packages()
    setup_locale()
    setup_environment()
    setup_ssh()
    setup_zsh()
   # clone_repo()

if __name__ == "__main__":
    main()
