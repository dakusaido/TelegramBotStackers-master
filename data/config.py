from environs import Env

env = Env()

env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')

ADMINS_ID = [1150292418]  # 1822173282, 925463724, 1486628263, 1822173282, 1150292418
