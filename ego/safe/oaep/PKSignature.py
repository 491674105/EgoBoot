from json import dumps

from rsa import newkeys, sign, verify
from rsa import PublicKey, PrivateKey

from ego.safe.Signature import Signature, Algorithm

# from ego.utils.Time import get_time_of_second
# from ego.utils.JSONUtil import sort_json


class PKSignature(Signature):
    __default_length = 1024

    def __init__(self, message=None, length=-1, stdout=False, target_path=None):
        super().__init__()
        if message:
            self.msg = message
        if type(self.msg) == dict:
            self.msg_str = dumps(self.msg)
        else:
            self.msg_str = self.msg
        if length > 0:
            self.length = length
        else:
            self.length = self.__default_length
        self.stdout = stdout
        self.target_path = target_path
        self.public_key = None
        self.public_key_str = ""
        self.private_key = None
        self.private_key_str = ""

    def generate(self, length=-1):
        if length > 0:
            self.length = length

        (public_key, private_key) = newkeys(self.length)
        self.public_key = public_key
        self.public_key_str = self.public_key.save_pkcs1().decode()
        self.private_key = private_key
        self.private_key_str = self.private_key.save_pkcs1().decode()
        if self.stdout:
            print("public_key:\n" + self.public_key_str)
            print("private_key:\n" + self.private_key_str)

        if self.target_path:
            self.save_keys()

    def save_keys(self, target_path=None):
        if target_path:
            self.target_path = target_path

        with open(f"{self.target_path}/public.pem", "w+") as file:
            file.write(self.public_key_str)

        with open(f"{self.target_path}/private.pem", "w+") as file:
            file.write(self.private_key_str)

    def load_pub_key(self, pub_key):
        self.public_key = PublicKey.load_pkcs1(pub_key)
        self.public_key_str = self.public_key.save_pkcs1().decode()

    def load_pri_key(self, pri_key):
        self.private_key = PrivateKey.load_pkcs1(pri_key)
        self.private_key_str = self.private_key.save_pkcs1().decode()

    def signing(self, algo=Algorithm.SHA1):
        return sign(self.msg_str.encode(), self.private_key, str(algo.value))

    def verifying(self, cip):
        return verify(self.msg_str.encode(), cip, self.public_key)


# if __name__ == "__main__":
    # from ego.utils.File import get_path

    # 生成密钥对
    # sign = Signature(stdout=True)
    # sign.generate(1024)
    # sign.save_keys(get_path())

    # msg = {
    #     "APP_NAME": "example",
    #     "GIT_TAG": "origin/dev",
    #     "APP_ENV": "dev",
    #     "APP_METHOD": "update",
    #     "APP_TYPE": "jar",
    #     "APP_ZONE": "default-normal",
    #     "INSTANCE_ID": 1,
    #     "USER_ID": 1,
    #     # "INSTANCE_IP": "",
    #     # "NEW_IP": "",
    #     # "APP_ROLL_TAG_LIST": "",
    #     "TIMESTAMP": get_time_of_second()
    # }
    # msg = {
    #     "env": "dev",
    #     "git_tag": "origin/dev",
    #     "git_url": "git@example:example/example.git",
    #     "publish_result": "SUCCESS",
    #     "service_name": "example",
    #     "user_id": "86",
    #     "xxf_zone": "default-normal",
    #     "req_time": get_time_of_second()
    # }
    # new_msg = sort_json(msg)
    # msg_context = dumps(new_msg)
    # print(msg_context)
    #
    # signature = PKSignature(message=msg_context, stdout=True, target_path=get_path("cert"))
    # signature.load_pub_key(open(f"{signature.target_path}\\public.pem", "r").read().encode())
    # signature.load_pri_key(open(f"{signature.target_path}\\private.pem", "r").read().encode())
    # # 签名
    # cipher = signature.signing(Algorithm.SHA1).hex()
    # print(cipher)
    # # 验签
    # try:
    #     result = signature.verifying(bytes.fromhex(cipher))
    #     algorithm = Algorithm(result)
    #     print("Application passed!")
    # except Exception as e:
    #     print(e)
    #     print("Access denied!")
