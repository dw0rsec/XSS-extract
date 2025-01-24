# XSS-extract

>⚠️ **CREDITS**: This script is an altered version of this original https://github.com/TeneBrae93/offensivesecurity/blob/main/xss-extract.py 

This project is a simple HTTP server that serves a JavaScript file designed for exfiltrating data from a target file on a web server using Cross-Site Scripting (XSS) techniques. The server generates a script that, when included in a web page, will read the contents of a specified file and send it to a specified attacker's IP address.

## Disclaimer:

**This tool is intended for educational purposes only. Use it responsibly and only on systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal and unethical.**

## Features:

- Generates a malicious JavaScript file that can be used for exfiltrating data.
- Serves the generated JavaScript file over HTTP.
- Displays the XSS payload for easy inclusion in a target web page.
- Cleans up afterwards

## Requirements:

- Python 3.x
- Basic understanding of XSS and web security concepts.

## Usage:

Run the script with the required arguments:

```shell
python3 xss-extract.py -f [TARGET FILE] -i [ATTACKER IP]
```

## License:

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/dw0rsec/XSS-extract/blob/main/LICENSE) file for details.