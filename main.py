from roblox import *

def main():
    print("[*] SkidPyExternal")
    print("[*] Made by @vynnhere")
    
    try:
        roblox = Roblox()
    except:
        print("[-] Failed to open Roblox!")
        input()
        return
    
    print("[+] Attached to Roblox successfully!")

    base_address = roblox.pm.base_address
    print(f"[+] Found Base at: 0x{base_address:08X}")
    
    datamodel = roblox.get_datamodel()
    print(f"[+] Found DataModel at: 0x{datamodel:08X}")

    renderview = roblox.get_renderview()
    print(f"[+] Found RenderView at: 0x{renderview:08X}")

    workspace = roblox.get_workspace()
    print(f"[+] Found Workspace at: 0x{workspace:08X}")

    humanoid = roblox.get_humanoid()
    print(f"[+] Found Humanoid at: 0x{humanoid:08X}")

    try:
        roblox.set_walkspeed(100.0)
        print("[+] Walkspeed set to 100!")

        roblox.set_jumppower(100.0)
        print("[+] JumpPower set to 100!")
    except:
        print("[-] Failed changing player attributes..")

    input()
    
if __name__ == "__main__":
    main()