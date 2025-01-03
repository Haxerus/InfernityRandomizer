class Card():
    def __init__(self, index):
        self.index = index
        self.rarity = 0
        self.bonus_rarity = 0
        self.pack = 0
        self.bonus_pack = 0
    
    def set_index(self, index):
        self.index = index
    
    def set_rarity(self, rarity):
        self.rarity = rarity
    
    def set_bonus_rarity(self, bonus_rarity):
        self.bonus_rarity = bonus_rarity
    
    def set_pack(self, pack):
        self.pack = pack
    
    def set_bonus_pack(self, bonus_pack):
        self.bonus_pack = bonus_pack
    
    def get_index(self):
        return self.index
    
    def get_rarity(self):
        return self.rarity
    
    def get_bonus_rarity(self):
        return self.bonus_rarity
    
    def get_pack(self):
        return self.pack
    
    def get_bonus_pack(self):
        return self.bonus_pack