import sys
import os

CONFIG_FILE = os.path.abspath(__file__)

def write_ip(ip):
    with open(CONFIG_FILE, "w") as f:
        f.write(
            'import sys\n'
            f'IP = "{ip}"\n\n'
            'if len(sys.argv) > 1:\n'
            '    new_ip = sys.argv[1]\n'
            '    if new_ip != IP:\n'
            '        IP = new_ip\n'
            '        with open(__file__, "w") as f:\n'
            '            f.write(\n'
            '                \'import sys\\n\'\n'
            '                f\'IP = "{new_ip}"\\n\\n\'\n'
            '                \'if len(sys.argv) > 1:\\n\'\n'
            '                \'    new_ip = sys.argv[1]\\n\'\n'
            '                \'    if new_ip != IP:\\n\'\n'
            '                \'        IP = new_ip\\n\'\n'
            '                \'        with open(__file__, "w") as f:\\n\'\n'
            '                \'            f.write(\\n\'\n'
            '                \'                \\\'import sys\\\\n\\\'\\n\'\n'
            '                \'                f\\\'IP = "{new_ip}"\\\\n\\\\n\\\'\\n\'\n'
            '                \'                ... (continues recursively) ...\\n\'\n'
            '            )\n'
            '        print(f"IP updated to {IP}")\n'
            '    else:\n'
            '        print("IP unchanged.")\n'
            'else:\n'
            '    print(f"Current IP: {IP}")\n'
        )

IP = "192.168.137.217"

if len(sys.argv) > 1:
    new_ip = sys.argv[1]
    if new_ip != IP:
        write_ip(new_ip)
        print(f"IP updated to {new_ip}")
    else:
        print("IP unchanged.")
else:
    print(f"Current IP: {IP}")
