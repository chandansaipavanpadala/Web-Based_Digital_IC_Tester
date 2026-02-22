import machine
import time
from ic_database import IC_DATABASE

# Define I2C
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
CHIPS = [0x20, 0x21, 0x22]

# Memory mapping: Default all pins to 1 (High/Input)
chip_states = {
    0x20: bytearray([0xFF, 0xFF]),
    0x21: bytearray([0xFF, 0xFF]),
    0x22: bytearray([0xFF, 0xFF])
}

def write_pin(pin_idx, value):
    """ Writes state to memory and blasts it to the chip in one fast transaction """
    chip_idx = pin_idx // 16
    addr = CHIPS[chip_idx]
    port = 0 if (pin_idx % 16) < 8 else 1
    bit = pin_idx % 8
    
    if value == 1:
        chip_states[addr][port] |= (1 << bit)
    else:
        chip_states[addr][port] &= ~(1 << bit)
    
    i2c.writeto(addr, chip_states[addr])

def read_pin(pin_idx):
    """ Reads the direct raw state of the pins """
    chip_idx = pin_idx // 16
    addr = CHIPS[chip_idx]
    port = 0 if (pin_idx % 16) < 8 else 1
    bit = pin_idx % 8
    
    data = i2c.readfrom(addr, 2)
    return (data[port] >> bit) & 1

def test_logic(ic_name, ic_data, verbose=True):
    """ Handles the actual truth table testing. If verbose=False, runs silently. """
    overall_pass = True

    # --- POWER UP ---
    if "power" in ic_data:
        write_pin(ic_data["power"]["vcc"], 1)
        write_pin(ic_data["power"]["gnd"], 0)
        time.sleep(0.1)

    for gate_idx, gate in enumerate(ic_data["gates"]):
        if verbose:
            print(f"\n  [ Checking Gate {gate_idx + 1} ]")
            print("  -----------------------------------")
        
        write_pin(gate["output"], 1) # Set to Input
        
        for row in gate["table"]:
            inputs, expected = row[:-1], row[-1]
            
            for i, pin_val in enumerate(inputs):
                write_pin(gate["inputs"][i], pin_val)
            
            time.sleep(0.05)
            actual = read_pin(gate["output"])
            
            if actual == expected:
                if verbose: print(f"    In: {inputs}  |  Exp: {expected}  |  Got: {actual}  ✅")
            else:
                if verbose: print(f"    In: {inputs}  |  Exp: {expected}  |  Got: {actual}  ❌")
                overall_pass = False
                if not verbose: break # Fast fail for auto-identify
                
        if verbose: print("  -----------------------------------")
        if not overall_pass and not verbose: break # Fast fail for auto-identify

    # --- POWER DOWN ---
    if "power" in ic_data:
        write_pin(ic_data["power"]["vcc"], 1)
        write_pin(ic_data["power"]["gnd"], 1)

    return overall_pass

def auto_identify():
    print("\n=====================================")
    print("      AUTO-IDENTIFYING IC...         ")
    print("=====================================")
    
    for ic_name, ic_data in IC_DATABASE.items():
        print(f"[*] Scanning signatures for {ic_name}...")
        
        # Run the test silently
        if test_logic(ic_name, ic_data, verbose=False):
            print(f"\n>>> MATCH FOUND! The inserted IC is: {ic_name} ({ic_data['name']}) ✅ <<<")
            return
            
    print("\n>>> NO MATCH FOUND ❌ <<<")
    print("The IC is either broken, inserted incorrectly, or not in the database.")

def manual_test():
    print("\nAvailable ICs:", ", ".join(IC_DATABASE.keys()))
    choice = input("Enter IC Name to test: ").upper().strip()
    
    if choice in IC_DATABASE:
        ic_data = IC_DATABASE[choice]
        print(f"\n=====================================")
        print(f"Testing: {ic_data['name']}")
        print(f"=====================================")
        
        if test_logic(choice, ic_data, verbose=True):
            print(f"\n>>> FINAL RESULT: {choice} PASSED ✅ <<<")
        else:
            print(f"\n>>> FINAL RESULT: {choice} FAILED ❌ <<<")
    else:
        print("Error: IC not found in database.")

# --- INIT & MAIN LOOP ---
print("Scanning I2C...")
devices = i2c.scan()
if devices: 
    print(f"Devices found: {[hex(d) for d in devices]}")

while True:
    print("\n" + "="*35)
    print("        MOBILE IC CHECKER")
    print("="*35)
    print("1. Auto-Identify IC")
    print("2. Manual IC Test")
    print("="*35)
    
    mode = input("Select an option (1 or 2): ").strip()
    
    if mode == '1':
        auto_identify()
    elif mode == '2':
        manual_test()
    else:
        print("Invalid choice. Please enter 1 or 2.")