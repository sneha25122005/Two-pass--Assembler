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

    symtab, littab, pooltab, pass1_table = pass_one(lines)
    pass2_table = pass_two(lines, symtab, littab)

    return jsonify({
        "pass1_table": pass1_table,
        "symtab": symtab,
        "littab": littab,
        "pooltab": pooltab,
        "pass2_table": pass2_table
    })


if __name__ == "__main__":
    app.run(debug=True)