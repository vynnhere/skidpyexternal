import pymem
import offsets

class Roblox:
    def __init__(self):
        self.pm = pymem.Pymem("RobloxPlayerBeta.exe")
    
    def readstring(self, address, max_length=1000):
        try:
            name = self.pm.read_bytes(address, max_length)
            null = name.find(b'\x00')
            if null != -1:
                return name[:null].decode('utf-8', errors='ignore')
            return name.decode('utf-8', errors='ignore')
        except:
            return
    
    def getname(self, address):
        try:
            nameptr = self.pm.read_ulonglong(address + offsets.NAME)
            length_field = self.pm.read_int(nameptr + 0x10)
            
            if length_field >= 16:
                string_ptr = self.pm.read_ulonglong(nameptr)
                return self.readstring(string_ptr)
            else:
                return self.readstring(nameptr)
        except:
            return
    
    def getchildren(self, address):
        children = []
        try:
            start_address = self.pm.read_ulonglong(address + offsets.CHILDREN)
            end_address = self.pm.read_ulonglong(start_address + offsets.CHILREN_END)
            
            current = self.pm.read_ulonglong(start_address)
            
            while current < end_address:
                child_address = self.pm.read_ulonglong(current)
                if child_address:
                    children.append(child_address)
                current += 0x10

        except:
            pass
    
        return children
    
    def findfirstchild(self, address, name):
        for child in self.getchildren(address):
            if self.getname(child) == name:
                return child
        return
    
    def get_datamodel(self):
        base = self.pm.base_address
        fake_datamodel = self.pm.read_ulonglong(base + offsets.FAKE_DATAMODEL_POINTER)
        datamodel = self.pm.read_ulonglong(fake_datamodel + offsets.FAKE_DATAMODEL_TO_DATAMODEL)
        
        return datamodel

    def get_renderview(self):
        datamodel = self.get_datamodel()
        renderview1 = self.pm.read_ulonglong(datamodel + offsets.DATAMODEL_TO_RENDERVIEW_1)
        renderview2 = self.pm.read_ulonglong(renderview1 + offsets.DATAMODEL_TO_RENDERVIEW_2)
        renderview = self.pm.read_ulonglong(renderview2 + offsets.DATAMODEL_TO_RENDERVIEW_3)

        return renderview

    def get_workspace(self):
        datamodel = self.get_datamodel()
        workspace = self.findfirstchild(datamodel, 'Workspace')

        return workspace

    def get_playerlist(self):
        datamodel = self.get_datamodel()
        players = self.findfirstchild(datamodel, 'Players')
        playerlist = self.getchildren(players)

        return playerlist

    def get_humanoid(self):
        datamodel = self.get_datamodel()
        players = self.findfirstchild(datamodel, 'Players')
        localplayer = self.pm.read_ulonglong(players + offsets.LOCALPLAYER)
        character = self.pm.read_ulonglong(localplayer + offsets.MODEL_INSTANCE)
        humanoid = self.findfirstchild(character, 'Humanoid')

        return humanoid

    def set_walkspeed(self, speed: float):
        humanoid = self.get_humanoid()

        self.pm.write_float(humanoid + offsets.WALKSPEED, speed)
        self.pm.write_float(humanoid + offsets.WALKSPEED_CHECK, speed)
    
    def set_jumppower(self, power: float):
        humanoid = self.get_humanoid()

        self.pm.write_float(humanoid + offsets.JUMP_POWER, power)