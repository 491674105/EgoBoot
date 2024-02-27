from typing import Union

from gitlab import Gitlab


class Auth:
    def __init__(self, url, token, **kwargs):
        self.url = url
        self.token = token
        self.api_version = "4"

        self.self_hosted = False
        self.ssl_verify = False
        self.timeout = 3
        self.gl_inst: Union[Gitlab, None] = None

    def update(self, configs):
        for key in configs:
            setattr(self, key, configs[key])

    def auth(self):
        if self.self_hosted:
            self.__auth_gitlab_self_hosted()
            return

        self.__auth_gitlab()

    def __auth_gitlab(self):
        """
            gitlab云服务认证
        """
        self.gl_inst = Gitlab(
            self.url,
            oauth_token=self.token,
            api_version=self.api_version,
            ssl_verify=self.ssl_verify,
            timeout=self.timeout
        )

    def __auth_gitlab_self_hosted(self):
        """
            自建gitlab服务认证
        """
        self.gl_inst = Gitlab(
            url=self.url,
            private_token=self.token,
            api_version=self.api_version,
            ssl_verify=self.ssl_verify,
            timeout=self.timeout
        )
