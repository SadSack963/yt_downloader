
# https://github.com/YunzheZJU/youtube-po-token-generator
# Install NodeJS >= 18.0 and issue the folling command to install this tool
#   npm install -g youtube-po-token-generator
#
# Execute the following command somewhere in your program or directly in a shell
#   youtube-po-token-generator
# => {"visitorData":"...","poToken":"..."}
# A string of JSON format would be printed to stdout, parse and use it as you like

# https://github.com/coreybutler/nvm-windows/releases
# Install nvm / NodeJS


def generate_po_token():
    import subprocess
    import json

    generate_process = subprocess.run(["powershell", "youtube-po-token-generator"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    # print(f"{generate_process}")
    # Convert to a dictionary
    po_token = json.loads(generate_process.stdout.decode())
    # print(po_token)
    return po_token
