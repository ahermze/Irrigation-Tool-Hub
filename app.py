from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world"

if __name__ == "__main__":
    app.run(host="localhost", port=5000)