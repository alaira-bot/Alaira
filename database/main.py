from flask import Flask
import time

app = Flask("alaira-database")

@app.route("/kill")
def kill_route():
    print("Killing database")
    time.sleep(5)  # TODO
    print("Database killed")
    return "", 204

def run():  # started from the main file - not invoked manually
    app.run()
