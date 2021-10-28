from typing import Dict, List, Union


class BaseUser:
    VALID_USER_ATTRIBUTES: Dict[str, Union[bool, str, None]] = {
        "id": None,
        "username": None,
        "discriminator": None,
        "bot": False,
        "system": False,
        "mfa_enabled": False,
        "banner": None,
        "banner_color": None,
        "accent_color": None,
        "locale": None,
        "verified": False,
        "email": None,
        "flags": 0,
        "premium_types": 0,
        "public_flags": 0,
        "bio": "",
        "avatar": None
    }
    MANDATORY_USER_ATTRIBUTES: List[str] = [
        "id",
        "username",
        "discriminator"
    ]

    def __init__(self, **kwargs):
        for mandatory_attr in self.MANDATORY_USER_ATTRIBUTES:
            assert mandatory_attr in kwargs, f"Missing mandatory attribute '{mandatory_attr}'"
        for attr in kwargs:
            assert attr in self.VALID_USER_ATTRIBUTES, f"Invalid user attribute '{attr}'"

        self.__attributes = {attr_name: kwargs.get(attr_name, self.VALID_USER_ATTRIBUTES[attr_name])
                             for attr_name in self.VALID_USER_ATTRIBUTES}

    def __getattr__(self, item) -> Union[bool, str, None]:
        if item in self.__attributes:
            return self.__attributes[item]
        raise AttributeError(f"Unexpected attribute '{item}'")


class BotClientUser(BaseUser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class User(BaseUser):
    pass
