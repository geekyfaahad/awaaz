from cryptography.fernet import Fernet

def load_key():
    """Loads the symmetric encryption key from a file."""
    with open("encryption_key.key", "rb") as key_file:
        return key_file.read()

def decrypt_url(encrypted_url, key):
    """Decrypts the URL using the provided key."""
    cipher = Fernet(key)
    decrypted_url = cipher.decrypt(encrypted_url).decode()
    return decrypted_url

if __name__ == "__main__":
    key = load_key()
    encrypted_url = b"gAAAAABnUiY7dXeOo3kEn8vE799th4up_op1WETMRump6p3LvA4PVJxOrhDMqd0jF7bwmZiIHX_XYY2ZqUt5AlvfYr7VHrfykiW1JpjYfNiGG8EneZJRqvvvDqJTMdNgbxD_3bTR-Ax2h3JAHlauoLyBtsvh_g5i9uwrxTgZWpUNjEKWPApMbeZhOvpJrg37L-bmBfbvlosyfOEDX3JrFs3PzG_eRHIWt_X9N9o0OgPkYyNq5a5dyZU1pD0OyaiYQAdo7IHZJRaHGUuy0oBjdvR-2hifOtI2QHgWAhvhkf2xXTGmv_Q9wF8rAcke5joJFGHmB5g-JyHVknE17e8juRITfTribariOBn7uGZ4zpzAmKk_jB3xaL5jgxJHuVghxpmQ4-dVDSaeCXrDNvjNj2grUXLq1mCew5SH2ARCxg_xt938277OrxDjZ2ox4f3XDMW6Umpp5Bzfk50D_ixQR33tBXegj2NWsvb-f17Nv3q1_XbvPzNqM_Luu9U57ITM1IrfzIxi1SFbrjMSUZqFiOAtYWyqX-4X3QUnQxZ_CcDD-yT4PASGc14SBj-GGhU1Zz3p3XIjnoDvQYOI6gVq1t5LPDvsUEEurbvdrBE7aETZaRNCzQwKdeqBtmrfDlKIoGCkBBaVAYlNo5CGcu1nU-HxM2UtK1HF_g=="
    decrypted_url = decrypt_url(encrypted_url, key)
    print(f"Decrypted URL: {decrypted_url}")
