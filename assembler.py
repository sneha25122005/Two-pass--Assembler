def pass_one(lines):

    symtab = {}
    littab = {}
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

        # label detection
        if len(parts) == 3:
            label = parts[0]
            symtab[label] = lc

        operand = parts[-1]

        # literal detection
        if operand.startswith("="):
            if operand not in littab:
                littab[operand] = None

        lc += 1

    # assign literal addresses
    for lit in littab:
        littab[lit] = lc
        lc += 1

    return symtab, littab
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

        # remove label if exists
        if len(parts) == 3:
            opcode = parts[0]
            reg = parts[1]
            operand = parts[2]
        else:
            opcode = parts[0]
            reg = parts[1]
            operand = parts[2]

        op = optab.get(opcode, "??")
        r = registers.get(reg, 0)

        addr = 0

        if operand in symtab:
            addr = symtab[operand]

        if operand in littab:
            addr = littab[operand]

        machine.append({
            "LC": lc,
            "OPCODE": opcode,
            "MACHINE_CODE": op,
            "REGISTER": r,
            "ADDRESS": addr
        })

        lc += 1

    return machine