from flask import Flask, render_template, request, jsonify
from assembler import pass_one, pass_two

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assemble", methods=["POST"])
def assemble():

    code = request.json["code"]
    lines = code.split("\n")

    symtab, littab = pass_one(lines)
    machine = pass_two(lines, symtab, littab)

    return jsonify({
    "symbol_table": symtab,
    "literal_table": littab,
    "machine_code": machine
})


if __name__ == "__main__":
    app.run(debug=True)