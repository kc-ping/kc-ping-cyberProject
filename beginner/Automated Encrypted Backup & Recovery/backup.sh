BACKUP_ROOT= "$HOME/backup" #BASE DIRECTORY FOR BACKUPS
SOURCE_DIRS= ('/etc','/home','/var/log') #DIRECTORIES TO BACKUP
DATE="$(date + %F-%H%M%S)" #TIMESTAMP FOR BACKUP FILES

DEST_DIR ="$BACKUP_ROOT/$DATE" #DESTINATION DIRECTORY FOR BACKUPS
LOGFILE="$BACKUP_ROOT/backup.log" #LOG FILE LOCATION

mkdir -p "$DEST_DIR" #CREATE DESTINATION DIRECTORY

#Create tarball of source and ecrypt with GPG (symmetric) encryption
TARBALL ="$DEST_DIR/backup-$DATE.tar.gz"
echo "[$(date)] Starting backup to $DEST_DIR" >> "$LOGFILE"
tar czf - "${SOURCE_DIRS[@]}" > "$TARBALL"
if [ $? -ne 0 ]; then #CHECK IF TARBALL CREATION WAS SUCCESSFUL $? -ne 0 means last command failed, ne is not equal
    echo "[$(date)] Error creating tarball" >> "$LOGFILE"
    exit 1
fi
echo "[$(date)] Tarball created at $TARBALL" >> "$LOGFILE"

#Encrypt the tarball with GPG(AES-256) output to .gpg file
gpg --chipher-algo AES256  --batch  --yes --passphrase-file ~/.backup_passphrase -c "$TARBALL" #ENCRYPT THE TARBALL with GPG and passphrase from file
if [ $? -ne 0 ]; then
    echo "[$(date)] Error encrypting tarball" >> "$LOGFILE"
    exit 1
fi
rm -f "$TARBALL" #REMOVE UNENCRYPTED TARBALL
echo "[$(date)] Encrypted backup created at $TARBALL.gpg" >> "$LOGFILE"