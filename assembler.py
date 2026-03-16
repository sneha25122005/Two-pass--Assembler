def pass_one(lines):

    symtab = {}
    littab = []
    pooltab = [0]
    pass1_table = []

    lc = 0

    for line in lines:

        parts = line.strip().split()

        if len(parts) == 0:
            continue

        if parts[0] == "START":
            lc = int(parts[1])
            continue

        if parts[0] == "END":
            break

        # SYMBOL DETECTION
        if len(parts) == 3 and parts[1] in ["DC","DS"]:
            label = parts[0]
            symtab[label] = lc

        opcode = ""
        reg = ""
        operand = ""

        if len(parts) == 3:
            opcode = parts[0]
            reg = parts[1]
            operand = parts[2]

        elif len(parts) == 2:
            opcode = parts[0]
            operand = parts[1]

        else:
            opcode = parts[0]

        # literal detection
        if operand.startswith("="):
            if operand not in [l["literal"] for l in littab]:
                littab.append({"literal": operand, "address": None})

        pass1_table.append({
            "LC": lc,
            "INSTRUCTION": line
        })

        lc += 1

    # assign literal addresses
    start = pooltab[-1]

    for i in range(start, len(littab)):
        littab[i]["address"] = lc
        lc += 1

    # convert literal table format
    literal_table = {l["literal"]: l["address"] for l in littab}

    return symtab, literal_table, pooltab, pass1_table


def pass_two(lines, symtab, littab):

    optab = {
        "ADD": "01",
        "SUB": "02",
        "MOVER": "04",
        "MOVEM": "05",
        "STOP": "00"
    }

    registers = {
        "AREG": 1,
        "BREG": 2,
        "CREG": 3,
        "DREG": 4
    }

    lc = 0
    machine = []

    for line in lines:

        parts = line.strip().split()

        if len(parts) == 0:
            continue

        if parts[0] == "START":
            lc = int(parts[1])
            continue

        if parts[0] == "END":
            break

        opcode = parts[0]
        reg = ""
        operand = ""

        if len(parts) >= 2:
            reg = parts[1]

        if len(parts) >= 3:
            operand = parts[2]

        op = optab.get(opcode, "--")
        r = registers.get(reg, 0)

        addr = 0

        if operand in symtab:
            addr = symtab[operand]

        if operand in littab:
            addr = littab[operand]

        machine.append({
            "LC": lc,
            "OPCODE": opcode,
            "REGISTER": r,
            "ADDRESS": addr
        })

        lc += 1

    return machine