from stfpTransfer import sftpTransfer
import argparse
import os
import getpass

def main():
    parser = argparse.ArgumentParser(description="Secure File Transfer via SFTP with Checksum Verification")
    parser.add_argument('action', choices=['upload', 'download'], help="Action to perform: upload or download")
    parser.add_argument('local_path', help="Local file path")
    parser.add_argument('remote_path', help="Remote file path")
    parser.add_argument('--host', required=True, help="SSH server hostname or IP address")
    parser.add_argument('--port', type=int, default=22, help="SSH server port (default: 22)")
    parser.add_argument('--username', required=True, help="SSH username")
    parser.add_argument('--password', help="SSH password (if not using key-based authentication)")
    parser.add_argument('--key', help="Path to private key file for key-based authentication")
    args = parser.parse_args()

    #prompt for password if no key file is provided
    if not args.key and args.password is None:
        args.password = getpass.getpass(prompt="Enter SSH password: ")

    sftpTransfer(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        action=args.action,
        key_file=args.key,
        local_path=args.local_path,
        remote_path=args.remote_path
    )

if __name__ == "__main__":
    main()
    # This is the command i Used to test the upload function
    # #--host 192.168.56.102 --user tuser upload SecureFileTransfer/testFile.txt  /home/tuser/Documents/testFile.text

    # This is the command i Used to test the download function
    # └─$ /home/kali/cyberlab/kc-ping-cyberProject/beginner/.venv/bin/python /home/kali/cyberlab/kc-ping-cyberProject/beginner/SecureFileTransfer/main.py   
    # --host 192.168.56.102 --user tuser download SecureFileTransfer/File.txt  /home/tuser/Documents/File.text