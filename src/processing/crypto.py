from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

#Key generation
#TO CONTINUE
def rsaKeypair():
    privateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    publicKey = privateKey.public_key()

    #Serialise keys
    private_pem = privateKey.private_bytes(
        encoding = serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem