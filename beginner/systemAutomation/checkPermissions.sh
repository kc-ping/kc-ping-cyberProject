#!/bin/bash
# ================================
# Permission Check Script
# Description: Checks important system files for permission issues
# ================================

FILES=( 
    "/etc/passwd"
    "/etc/shadow"
    "/etc/sudoers"
)

for FILE in "${FILES[@]}"; do
    if [ -e "$FILE" ]; then
        PERM=$(stat -c "%a" "$FILE")
        OWNER=$(stat -c "%U" "$FILE")
        
        if [[ "$FILE" == *"passwd"* || "$FILE" == *"shadow"* ]]; then
            if [ "$PERM" -gt 644 ] || [ "$OWNER" != "root" ]; then
                echo "⚠️ Permission issue detected in $FILE: Permissions=$PERM, Owner=$OWNER"
            else
                echo "✅ $FILE permissions are correct."
            fi
        elif [[ "$FILE" == *"sudoers"* ]]; then
            if [ "$PERM" -ne 440 ] || [ "$OWNER" != "root" ]; then
                echo "⚠️ Permission issue detected in $FILE: Permissions=$PERM, Owner=$OWNER"
            else
                echo "✅ $FILE permissions are correct."
            fi
        fi
    else
        echo "❌ $FILE does not exist."
    fi
done