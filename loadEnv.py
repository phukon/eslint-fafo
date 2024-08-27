from dotenv import load_dotenv
import os

print("running loadenv")
env = os.getenv('SERVER_ENV')
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path)

TEST = os.getenv("TEST")