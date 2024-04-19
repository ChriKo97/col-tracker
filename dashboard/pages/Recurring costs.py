import os

import helper
import recurring_costs.main as main


from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv("POSTGRES_USER", "admin")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("DB_NAME", "col")
db_host = os.getenv("DB_HOST", "col-database")
db_port = os.getenv("DB_PORT", 5432)

engine = helper.connect_to_database(
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    name=db_name)

main.add_recurring_cost(engine)

