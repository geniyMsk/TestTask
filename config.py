from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
provider_token = env.str("PROVIDER_TOKEN")

host = env.str("PGHOST")
PG_USER = env.str("PG_USER")
PG_PASS = env.str("PG_PASS")