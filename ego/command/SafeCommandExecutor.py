from typing import Union

from argparse import ArgumentParser, Namespace

from ego.safe.oaep.RSAEncryption import RSAEncryption

from ego.utils.file.File import path_format, get_path


class SafeCommandExecutor:
    def __init__(self, root_parser):
        self.root_parser: ArgumentParser = root_parser
        self.subparser: Union[ArgumentParser, None] = None
        self.rsaEncryption = RSAEncryption()

    def create_parser(self, subparser: ArgumentParser):
        self.subparser = subparser
        subparser.add_argument(
            "-g",
            "--generate",
            default=False,
            action="store_true",
            help="Generate key pairs. "
        )
        subparser.add_argument(
            "-t",
            "--generate_path",
            metavar="generate_path",
            nargs="?",
            help="Generate key pairs with file path(default save in the root path of the [python-yw-ops] project). "
        )
        subparser.add_argument(
            "--nbits",
            nargs="?",
            type=int,
            help="number of bits(default: 1024). "
        )
        subparser.add_argument(
            "--pf_name",
            metavar="public_key_file_name",
            nargs="?",
            help="public_key file name(default: public_key). "
        )
        subparser.add_argument(
            "--if_name",
            metavar="private_key_file_name",
            nargs="?",
            help="private_key file name(default: private_key). "
        )
        subparser.add_argument(
            "--file_fmt",
            nargs="?",
            help="pk_file format[PEM | DER](default: PEM). "
        )
        subparser.add_argument(
            "-e",
            "--encrypt",
            metavar="plaintext",
            nargs="?",
            help="Convert target content to ciphertext. "
        )
        subparser.add_argument(
            "-d",
            "--decrypt",
            metavar="ciphertext",
            nargs="?",
            help="Convert target content to plaintext. "
        )
        subparser.add_argument(
            "-p",
            "--public_key",
            metavar="public_key_file_path",
            nargs="?",
            help="choose a public_key file path(need absolute path). "
        )
        subparser.add_argument(
            "-i",
            "--private_key",
            metavar="private_key_file_path",
            nargs="?",
            help="choose a private_key file path(need absolute path). "
        )
        subparser.add_argument(
            "--encoding",
            nargs="?",
            help="pk_file encoding(default: UTF-8). "
        )

        subparser.set_defaults(generate_path=path_format(f"{get_path()}"))
        subparser.set_defaults(nbits=1024)
        subparser.set_defaults(pf_name="public_key")
        subparser.set_defaults(if_name="private_key")
        subparser.set_defaults(file_fmt="PEM")
        subparser.set_defaults(encoding="UTF-8")
        subparser.set_defaults(func=self.executor)

    def executor(self, args: Namespace):
        if args.generate:
            self.generate(args)
            return

        if args.encrypt:
            self.encrypt(args)
            return

        if args.decrypt:
            self.decrypt(args)
            return

        print("operation error!")
        self.subparser.print_help()

    def generate(self, args: Namespace):
        self.rsaEncryption.generate_key(
            nbits=args.nbits,
            key_type="file",
            save_path=args.generate_path,
            pub_file_name=args.pf_name,
            pri_file_name=args.if_name,
            file_fmt=args.file_fmt,
            encoding=args.encoding
        )

    def encrypt(self, args: Namespace):
        if not args.public_key:
            print("Please specify a public key!")
            self.subparser.print_help()

        cipher_bytes = self.rsaEncryption.exec_encrypt(
            message=args.encrypt,
            pk_file_path=args.public_key,
            encoding=args.encoding
        )
        print(cipher_bytes.hex())

    def decrypt(self, args: Namespace):
        if not args.private_key:
            print("Please specify a private key!")
            self.subparser.print_help()

        plain_bytes = self.rsaEncryption.exec_decrypt(
            ciphertext=bytes.fromhex(args.decrypt),
            pk_file_path=args.private_key,
            encoding=args.encoding
        )
        print(plain_bytes.decode(encoding=args.encoding))
