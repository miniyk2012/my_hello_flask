SECRET_KEY = "123456"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,  # 悲观ping
    "pool_recycle": 300,  # 每300s对连接池做个回收, 再重连, mysql默认是8小时, Flask-SQLALchemy默认是2小时
}