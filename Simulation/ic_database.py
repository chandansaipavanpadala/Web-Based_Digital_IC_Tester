# ic_database.py

IC_DATABASE = {
    "74LS00": {
        "name": "Quad 2-Input NAND Gate",
        "power": {"vcc": 38, "gnd": 47}, 
        "gates": [
            # Gate 1 (Pins 1, 2 -> 3)
            {"inputs": [41, 42], "output": 43, "table": [(0,0,1), (0,1,1), (1,0,1), (1,1,0)]},
            # Gate 2 (Pins 4, 5 -> 6)
            {"inputs": [44, 45], "output": 46, "table": [(0,0,1), (0,1,1), (1,0,1), (1,1,0)]},
            # Gate 3 (Pins 9, 10 -> 8)
            {"inputs": [33, 34], "output": 32, "table": [(0,0,1), (0,1,1), (1,0,1), (1,1,0)]},
            # Gate 4 (Pins 12, 13 -> 11)
            {"inputs": [36, 37], "output": 35, "table": [(0,0,1), (0,1,1), (1,0,1), (1,1,0)]}
        ]
    },
    "74LS08": {
        "name": "Quad 2-Input AND Gate",
        "power": {"vcc": 38, "gnd": 47}, 
        "gates": [
            # The physical pins are exactly the same, only the expected output changes
            {"inputs": [41, 42], "output": 43, "table": [(0,0,0), (0,1,0), (1,0,0), (1,1,1)]},
            {"inputs": [44, 45], "output": 46, "table": [(0,0,0), (0,1,0), (1,0,0), (1,1,1)]},
            {"inputs": [33, 34], "output": 32, "table": [(0,0,0), (0,1,0), (1,0,0), (1,1,1)]},
            {"inputs": [36, 37], "output": 35, "table": [(0,0,0), (0,1,0), (1,0,0), (1,1,1)]}
        ]
    }
}