from flask import request, render_template
from flask import redirect, url_for, Flask
from flask import session

from .scripts.gpio_one_logic import IOT

from .scripts.server_utils import isCredentialValid


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=["GET", "POST"])
def index():

    if "username" in session:
        return redirect(url_for("homePage"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        app.logger.info({"username": username, "password": password})

        if isCredentialValid(username, password):
            session["username"] = username
            return redirect(url_for("homePage"))

    return render_template("index.html")


@app.route("/iot/commands")
def homePage():
    if "username" not in session:
        app.logger.info({"username": None})
        return redirect(url_for("index"))

    return render_template("home.html")


@app.route("/iot/devices/switch_on")
def switchOn():
    apiKey = request.headers.get("api_key")
    if apiKey != "":
        return {"status": "ERROR", "message": "Invalid api key"}
    IOT.run()
    return {"status": "OKAY", "message": "action exectuted successfully"}


@app.route("/iot/devices/switch_off")
def switchOff():
    apiKey = request.headers.get("api_key")
    if apiKey != "":
        return {"status": "ERROR", "message": "Invalid api key"}
    IOT.run()
    return {"status": "OKAY", "message": "action exectuted successfully"}


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
