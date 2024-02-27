from typing import Union

from rsa import newkeys, encrypt, decrypt
from rsa import PublicKey, PrivateKey

from os import path, makedirs

from ego.safe.Encryption import Encryption

from ego.exception.type.NullPointException import NullPointException


class RSAEncryption(Encryption):

    def generate_key(
            self,
            nbits=1024,
            key_type="key_obj",
            save_path=None,
            pub_file_name="public_key",
            pri_file_name="private_key",
            file_fmt="PEM",
            encoding="utf-8"
    ):
        """
        创建密钥对
        Args:
            nbits: 指定密钥对长度
            key_type: 返回密钥的类型
                key_obj: PublicKey, PrivateKey
                str: 密钥对字符串
                file: 文件形式书保存，需要与save_path参数合并使用
            save_path: 密钥对保存路径
            pub_file_name: 公钥文件名,
            pri_file_name: 私钥文件名,
            file_fmt: 密钥文件格式，可选（PEM、DER），默认 PEM
            encoding: 生成密钥内容的编码，默认 UTF-8
        Returns:

        """
        public_key, private_key = newkeys(nbits)

        if key_type == "str":
            return [
                public_key.save_pkcs1(file_fmt).decode(encoding),
                private_key.save_pkcs1(file_fmt).decode(encoding)
            ]
        elif key_type == "file":
            if not path.exists(save_path):
                makedirs(save_path)

            with open(f"{save_path}/{pub_file_name}.{file_fmt.lower()}", mode="wb+") as pub_file:
                pub_file.write(public_key.save_pkcs1(file_fmt))
            with open(f"{save_path}/{pri_file_name}.{file_fmt.lower()}", mode="wb+") as pri_file:
                pri_file.write(private_key.save_pkcs1(file_fmt))
            return None
        else:
            return [public_key, private_key]

    def exec_encrypt(
            self,
            message: Union[str, bytes],
            public_key: Union[PublicKey, None] = None,
            pk_file_path: Union[str, None] = None,
            encoding="utf-8"
    ):
        if type(message) != bytes:
            msg = message.encode(encoding=encoding)
        else:
            msg = message

        if not public_key and not pk_file_path:
            raise NullPointException("Public key cannot be empty!")

        if public_key:
            pk = public_key
        else:
            with open(pk_file_path, mode="rb") as pk_file:
                pk = PublicKey.load_pkcs1(pk_file.read())
        ciphertext = encrypt(msg, pk)

        return ciphertext

    def exec_decrypt(
            self,
            ciphertext: Union[str, bytes],
            private_key: Union[PrivateKey, None] = None,
            pk_file_path: Union[str, None] = None,
            encoding="utf-8"
    ):
        if type(ciphertext) != bytes:
            cipher_msg = ciphertext.encode(encoding=encoding)
        else:
            cipher_msg = ciphertext

        if not private_key and not pk_file_path:
            raise NullPointException("Private key cannot be empty!")
        if private_key:
            pk = private_key
        else:
            with open(pk_file_path, mode="rb") as pk_file:
                pk = PrivateKey.load_pkcs1(pk_file.read())
        plaintext = decrypt(cipher_msg, pk)

        return plaintext


if __name__ == "__main__":
    password = "Fearon@1993"
    rsaEncryption = RSAEncryption()
    # pub_key, pri_key = rsaEncryption.generate_key(1024)
    # print(pub_key)
    # print(pub_key.save_pkcs1().decode())
    # print(pri_key)
    # print(pri_key.save_pkcs1().decode())
    # keys = rsaEncryption.generate_key(1024)
    # print(f"pub_key --> {keys[0]}")
    # print(f"pri_key --> {keys[1]}")

    cert_path = "E:\\projects\\python\python-yw-ops\\cmdb_service\\cert"
    # rsaEncryption.generate_key(
    #     nbits=1024,
    #     key_type="file",
    #     save_path=cert_path
    # )

    # cipher_bytes = rsaEncryption.exec_encrypt(password, pub_key)
    # print(cipher_bytes)
    # plain_bytes = rsaEncryption.exec_decrypt(cipher_bytes, pri_key)
    # print(plain_bytes)
    # print(plain_bytes.decode(encoding="utf-8"))

    cipher_bytes = rsaEncryption.exec_encrypt(password, pk_file_path=f"{cert_path}/public_key.pem")
    print(cipher_bytes)
    print(cipher_bytes.hex())
    plain_bytes = rsaEncryption.exec_decrypt(cipher_bytes, pk_file_path=f"{cert_path}/private_key.pem")
    print(plain_bytes)
    print(plain_bytes.decode(encoding="utf-8"))
