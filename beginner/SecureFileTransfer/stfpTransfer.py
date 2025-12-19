
import paramiko
from hashLib import sha256_checksum

def sftpTransfer(host, port, username, password, action, key_file=None, local_path=None, remote_path=None):
    ''' conect via SSH and perform STFP upload or download with checksum verification verification '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add unknown host

    try: 
        if key_file:
            key = paramiko.RSAKey.from_private_key_file(key_file)
            ssh.connect(hostname=host, port=port, username=username, pkey=key)
        else:
            ssh.connect(hostname=host, port=port, username=username, password=password)
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    sftp = ssh.open_sftp()
    if action == 'upload':
        # compute local file hash
        localHash = sha256_checksum(local_path)
        print(f"Uploading {local_path} to {remote_path}...")
        sftp.put(local_path, remote_path)
        # compute remote file hash by running sha256sum on the server
        stdin, stdout, stderr = ssh.exec_command(f'sha256sum {remote_path}')
        remoteHash= stdout.read().decode().split()[0]
        if localHash == remoteHash:
            print("Upload successful and verified.")
        else:
            print("Upload failed: checksum mismatch. Transfer may be corrupted.")
    
    elif action == 'download':
        print(f"Downloading {remote_path} to {local_path}...")
        sftp.get(remote_path, local_path)
        # compute remote file hash by running sha256sum on the server
        stdin, stdout, stderr = ssh.exec_command(f'sha256sum {remote_path}')
        remoteHash= stdout.read().decode().split()[0]
        # compute local file hash
        localHash = sha256_checksum(local_path)
        if localHash == remoteHash:
            print("Download successful and verified.")
        else:
            print("Download failed: checksum mismatch. Transfer may be corrupted.")

    sftp.close()
    ssh.close()
