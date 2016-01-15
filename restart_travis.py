import subprocess

master_status = subprocess.check_output(
    ['travis', 'show', 'master', '-r', 'scikit-beam/scikit-beam']
).decode()

print(master_status)