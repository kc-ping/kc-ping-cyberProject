import paramiko

# Initialize the SSH client and automatically add unknown host keys (for simplicity)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
# what are host keys? 
# Host keys are cryptographic keys used to identify a server in SSH connections.

# Using a key file for authentication 
# (with optionally a passphrase because the key might be encrypted)
key = paramiko.RSAKey.from_private_key_file('~/.ssh/id_ed25519')
ssh.connect(hostname='192.168.56.102', port=22, username='tuser', pkey=key)

if key:
    ssh.connect(hostname='192.168.56.102', port=22, username='tuser', pkey=key)
else:
    ssh.connect(hostname='192.168.56.102', port=22, username='tuser', password='target')

# File transfer using SFTP
sftp = ssh.open_sftp()
sftp.put('/home/kali/cyberlab/kc-ping-cyberProject/beginner/Secure File Transfer/testFile.txt', '/home/tuser/testfile.txt') # Upload file
sftp.get('/home/tuser/testfile.txt', '/home/kali/Downloads/testfile_downloaded.txt') # Download file
sftp.close()
ssh.close()