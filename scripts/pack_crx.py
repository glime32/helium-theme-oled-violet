#!/usr/bin/env python3
"""Pack an extension directory into a signed CRX3 file (same format Chromium produces).

usage: pack_crx.py SRC_DIR KEY.pem OUT.crx   -> prints the extension ID
"""
import hashlib, io, os, struct, sys, zipfile
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def field(num, payload):  # protobuf length-delimited field
    return varint((num << 3) | 2) + varint(len(payload)) + payload


def zip_dir(src):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            dirs.sort()
            for f in sorted(files):
                path = os.path.join(root, f)
                info = zipfile.ZipInfo(os.path.relpath(path, src), date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, open(path, "rb").read())
    return buf.getvalue()


def extension_id(pub_der):
    return "".join("abcdefghijklmnop"[int(c, 16)] for c in hashlib.sha256(pub_der).hexdigest()[:32])


def pack(src, key_path, out):
    key = serialization.load_pem_private_key(open(key_path, "rb").read(), password=None)
    pub = key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    crx_id = hashlib.sha256(pub).digest()[:16]
    signed_header_data = field(1, crx_id)                      # SignedData { crx_id }
    archive = zip_dir(src)
    to_sign = b"CRX3 SignedData\x00" + struct.pack("<I", len(signed_header_data)) + signed_header_data + archive
    sig = key.sign(to_sign, padding.PKCS1v15(), hashes.SHA256())
    header = field(2, field(1, pub) + field(2, sig))           # sha256_with_rsa { public_key, signature }
    header += field(10000, signed_header_data)                 # signed_header_data
    with open(out, "wb") as f:
        f.write(b"Cr24" + struct.pack("<I", 3) + struct.pack("<I", len(header)) + header + archive)
    return extension_id(pub)


if __name__ == "__main__":
    print(pack(*sys.argv[1:4]))
