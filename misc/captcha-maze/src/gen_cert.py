"""
SecurinetsENIT CTF 2026 - Misc Challenge: Captcha: Rats in a Maze
Author: MrXFuji

Generates self-signed TLS certificate and private key for the challenge service.
"""

import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_self_signed_cert(cert_path="cert.pem", key_path="key.pem"):
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Subject and Issuer
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "TN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tunis"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "SecurinetsENIT"),
        x509.NameAttribute(NameOID.COMMON_NAME, "captcha.ctf.securinets.tn"),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        )
        .sign(key, hashes.SHA256())
    )

    # Write private key
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # Write certificate
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"[+] TLS certificate saved to {cert_path}")
    print(f"[+] TLS private key saved to {key_path}")

if __name__ == "__main__":
    generate_self_signed_cert()
