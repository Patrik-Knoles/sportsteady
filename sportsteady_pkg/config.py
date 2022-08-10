class BaseConfig:
    SECRET_KEY="59ja$aP1"
    ADMIN_EMAIL="nwadubafrancisxavier@gmail.com"

class TestConfig(BaseConfig):
    ADMIN_EMAIL="tinnievisuals@gmail.com"

class LiveConfig(BaseConfig):
    ADMIN_EMAIL="live@yahoo.com"