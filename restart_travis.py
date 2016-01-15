import subprocess

master_status = subprocess.check_output(
    ['travis', 'show', 'master', '-r', 'scikit-beam/scikit-beam']
).decode()

# build_number is the travis number that corresponds to the python 3.5
# build on travis; something like 1493.3
build_number = -1
for line in master_status.split('\n'):
    # I am looking for the line in the travis status that looks like this:
    # #1493.3 passed:  3 min          python: 3.5, os: linux
    # so that I can grab the number at the front, 1493.3 and restart it
    if 'python: 3.5' in line:
        build_number = line.split()[0][1:]
        print(build_number)
        break
else:
    print(master_status)
    raise ValueError("No python 3.5 builds found")

restart_message = subprocess.check_output(
    ['travis', 'restart', build_number, ' -r', 'scikit-beam/scikit-beam']
).decode()

print(restart_message)


