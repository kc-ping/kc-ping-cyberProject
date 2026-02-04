BACKUP_ROOT="$HOME/backup" #BASE DIRECTORY FOR BACKUPS

echo "Available backups:"
select BACKUP_DIR in "$BACKUP_ROOT"/*; do
    [[ -d "$BACKUP_DIR"]] || { echo "Invalid selection. Please try again."; continue; } #-d checks if directory exists
    echo "Restoring from $BACKUP_DIR..."
    #Find the encrypted backup file
    ENC_FILE=$(ls "$BACKUP_DIR"*.gpg 2>/dev/null | head -n1)
    if [[ ! -f "$ENC_FILE" ]]; then #-f checks if file exists
        echo "No encrypted backup file found in $BACKUP_DIR"
        exit 1
    fi
    # Decrypt and extract
    echo "Decrypting and extracting...."
    gpg --batch --yes --passphrase-file ~/.backup_passphrase "$ENC_FILE" --output - | tar xzvf - -C / 
    # -C / extracts to root directory, xzvf - reads from stdin, xz is extract, v is verbose, f is file
    #if you just put xz it will extract to current directory but with xzvf it extracts to root directory
    echo "Restoration complete."
    break
done