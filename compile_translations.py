import os
import struct

def compile_po_to_mo(po_path, mo_path):
    """Simple .po to .mo compiler without needing gettext"""
    translations = {}
    
    with open(po_path, 'r', encoding='utf-8') as f:
        msgid = None
        msgstr = None
        in_msgid = False
        in_msgstr = False
        
        for line in f:
            line = line.rstrip('\n')
            
            if line.startswith('msgid '):
                msgid = line[6:].strip('"')
                in_msgid = True
                in_msgstr = False
            elif line.startswith('msgstr '):
                msgstr = line[7:].strip('"')
                in_msgstr = True
                in_msgid = False
            elif line.startswith('"') and (in_msgid or in_msgstr):
                # Continuation line
                content = line.strip('"')
                if in_msgid:
                    msgid += content
                elif in_msgstr:
                    msgstr += content
            elif line.strip() == '':
                # Empty line - save translation
                if msgid is not None and msgstr is not None:
                    if msgid:  # Skip empty msgid (header)
                        translations[msgid] = msgstr
                msgid = None
                msgstr = None
                in_msgid = False
                in_msgstr = False
        
        # Save last entry
        if msgid is not None and msgstr is not None and msgid:
            translations[msgid] = msgstr
    
    # Write .mo file
    keys = sorted([k for k in translations.keys() if k])
    
    # Build the message catalog
    offsets = []
    ids = b''
    strs = b''
    
    for key in keys:
        ids += key.encode('utf-8') + b'\x00'
        strs += translations[key].encode('utf-8') + b'\x00'
    
    # Calculate offsets
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    koffsets = []
    voffsets = []
    
    offset = 0
    for key in keys:
        length = len(key.encode('utf-8'))
        koffsets.append((length, keystart + offset))
        offset += length + 1
    
    offset = 0
    for key in keys:
        length = len(translations[key].encode('utf-8'))
        voffsets.append((length, valuestart + offset))
        offset += length + 1
    
    # Add header entry
    header = b''
    header_trans = b'Content-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n'
    
    with open(mo_path, 'wb') as f:
        # Magic number (little endian)
        f.write(struct.pack('<I', 0x950412de))
        # File format revision
        f.write(struct.pack('<I', 0))
        # Number of strings
        f.write(struct.pack('<I', len(keys) + 1))
        # Offset of table with original strings
        f.write(struct.pack('<I', 7 * 4))
        # Offset of table with translation strings  
        f.write(struct.pack('<I', 7 * 4 + (len(keys) + 1) * 8))
        # Size of hashing table (0 = no hashing)
        f.write(struct.pack('<I', 0))
        # Offset of hashing table
        f.write(struct.pack('<I', 0))
        
        # Write header entry in key table
        f.write(struct.pack('<II', 0, keystart + len(ids)))
        
        # Write key offsets
        for length, offset in koffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Write header entry in value table
        f.write(struct.pack('<II', len(header_trans), valuestart + len(strs)))
        
        # Write value offsets
        for length, offset in voffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Write keys
        f.write(ids)
        # Write header key (empty)
        f.write(b'\x00')
        
        # Write values
        f.write(strs)
        # Write header translation
        f.write(header_trans)

# Compile both locale files
base_path = r'c:\Users\gulno\OneDrive\Документы\projects\6\mariyam-new-year\locale'

compile_po_to_mo(
    os.path.join(base_path, 'uz', 'LC_MESSAGES', 'django.po'),
    os.path.join(base_path, 'uz', 'LC_MESSAGES', 'django.mo')
)

compile_po_to_mo(
    os.path.join(base_path, 'kaa', 'LC_MESSAGES', 'django.po'),
    os.path.join(base_path, 'kaa', 'LC_MESSAGES', 'django.mo')
)

print("Translation files compiled successfully!")
