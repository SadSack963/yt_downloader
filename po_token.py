# https://github.com/YunzheZJU/youtube-po-token-generator
# Install Node.js >= 18.0 and issue the following command to install this tool
#   npm install -g youtube-po-token-generator
#
# Execute the following command somewhere in your program or directly in a shell
#   youtube-po-token-generator
# => {"visitorData":"...","poToken":"..."}
# A string of JSON format would be printed to stdout, parse and use it as you like

# https://github.com/coreybutler/nvm-windows/releases
# Install nvm / NodeJS


def get_new_po_token(token_file: str) -> None:
    """
    Get Proof of Origin Token from YouTube. Save in JSON file.

    :param token_file: filename
    :type token_file: string
    :return:
    :rtype:
    """

    import subprocess
    import json
    from json import JSONDecodeError

    logging.info(f"Start - get PoToken")
    generate_process = subprocess.run(["powershell", "youtube-po-token-generator"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    logging.debug(f"End - get PoToken: {generate_process = }")
    if generate_process.returncode == 0:
        # Convert bytestring to dictionary
        po_token = json.loads(generate_process.stdout.decode())
        logging.info(f"PoToken = {po_token}")

        default_tokens = {
                "access_token": None,
                "refresh_token": None,
                "expires": None,
                "visitorData": None,
                "po_token": None
            }

        try:
            # Read token file
            logging.debug(f"Read tokens: {token_file}")
            with open(token_file, mode="r") as fp:
                tokens = json.load(fp)
        except FileNotFoundError as e:
            logging.error(f"Token file not found: [{e.args}] {e.filename}")
            tokens = default_tokens
        except JSONDecodeError as e:
            logging.error(f"JSON Decode Error: [{e.args}] {e.msg}")
            tokens = default_tokens

        # Insert new values
        tokens["visitorData"] = po_token["visitorData"]
        tokens["po_token"] = po_token["poToken"]
        # Save token file
        logging.debug(f"Save tokens: {token_file}")
        with open(token_file, mode="w") as fp:
            json.dump(tokens, fp)
    else:
        logging.error(f"Could not get PO Token from YouTube. Return Code: {generate_process.returncode} {generate_process = }")


if __name__ == "__main__":
    import logging
    from logger import start_logging

    logger = logging.getLogger(__name__)
    start_logging()

    get_new_po_token("tokens.json")
