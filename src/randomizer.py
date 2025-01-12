import random
import json

from pathlib import Path

from card import Card
from ndstool_wrapper import NdsToolWrapper
from pac_wrapper import PacWrapper

class Randomizer():
    def __init__(self, rom_path):
        self.__load_card_pool()
        self.nds_tool = NdsToolWrapper(rom_path)
    
    def randomize_rom(self, settings, output_path):
        self.__import_rom()

        if settings["seed"] == "":
            random.seed()
        else:
            random.seed(settings["seed"])

        # Do randomization
        if settings["packs"]:
            self.__randomize_packs()
        
        if settings["starter_deck"]:
            self.__randomize_starting_deck()
        
        if settings["structure_deck"]:
            self.__randomize_structure_decks()
        
        if settings["cpu_shuffle"]:
            self.__shuffle_cpu_decks()

        self.__export_rom(output_path)

    def __randomize_packs(self):
        # Constants
        card_offset = 0x7A8
        num_packs = 56

        pack_bytes = self.bin2_pac.get_file_bytes("card_pack.bin")
        new_packs = bytearray(pack_bytes)
        cards = []
        packs = [[] for _ in range(num_packs)]

        for i in range(card_offset, len(pack_bytes), 8):
            cards.append(Card(i))

        random.shuffle(cards)

        for i in range(len(cards)):
            pack_index = i % num_packs
            cards[i].set_pack(pack_index+1)
            if pack_index >= 31:
                cards[i].set_bonus_pack(pack_index+1)
            packs[pack_index].append(cards[i])
        
        for pack in packs:
            for card in pack[:6]:
                card.set_rarity(2)
                card.set_bonus_rarity(2)
            
            for card in pack[6:15]:
                card.set_rarity(3)
                card.set_bonus_rarity(3)
            
            for card in pack[15:30]:
                card.set_rarity(4)
                card.set_bonus_rarity(4)

            for card in pack:
                i = card.get_index()
                new_packs[i] = card.get_rarity()
                new_packs[i+1] = card.get_bonus_rarity()
                new_packs[i+3] = card.get_pack()
                new_packs[i+4] = card.get_bonus_pack()

        self.bin2_pac.override_file_data("card_pack.bin", new_packs)

    def __randomize_starting_deck(self):
        # Constants
        header_offset = 8

        main_deck_size = 40
        main_deck_offset = header_offset + 2

        extra_deck_size = 4
        extra_deck_offset = header_offset + (main_deck_size * 2) + 4

        side_deck_size = 15
        side_deck_offset = header_offset + (main_deck_size * 2) + (extra_deck_size * 2) + 6

        deck_bytes = self.deck_pac.get_file_bytes("rpg001_0_syoki.ydc")
        new_deck = bytearray(deck_bytes)

        self.__randomize_deck(self.main_pool, new_deck, main_deck_size, main_deck_offset)
        self.__randomize_deck(self.main_pool, new_deck, side_deck_size, side_deck_offset)
        self.__randomize_deck(self.extra_pool, new_deck, extra_deck_size, extra_deck_offset)

        self.deck_pac.override_file_data("rpg001_0_syoki.ydc", new_deck)

        # Wipe speed duel deck
        speed_deck = self.deck_pac.get_file_bytes("rpg002_0_rd.ydc")
        new_speed_deck = bytearray(14)
        new_speed_deck[:header_offset] = speed_deck[:header_offset]

        self.deck_pac.override_file_data("rpg002_0_rd.ydc", new_speed_deck)

    def __randomize_structure_decks(self):
        header_offset = 8
        main_deck_size = 40
        main_deck_offset = header_offset + 2

        deck_file_names = self.deck_pac.get_file_names()
        sd_file_names = [file_name for file_name in deck_file_names if file_name.startswith("sd")]

        for deck_file in sd_file_names:
            # print(deck_file)
            deck = self.deck_pac.get_file_bytes(deck_file)

            # extra_deck_size = 3 if deck_file == "sd_starter10.ydc" else 0
            extra_deck_size = random.randint(4, 8)
            extra_deck_offset = header_offset + (main_deck_size * 2) + 4
            deck_size_bytes = extra_deck_offset + (extra_deck_size * 2) + 2

            new_deck = bytearray(deck_size_bytes)
            new_deck[:header_offset] = deck[:header_offset]

            new_deck[header_offset] = main_deck_size
            new_deck[extra_deck_offset - 2] = extra_deck_size

            self.__randomize_deck(self.main_pool, new_deck, main_deck_size, main_deck_offset)
            if extra_deck_size > 0:
                self.__randomize_deck(self.extra_pool, new_deck, extra_deck_size, extra_deck_offset)

            self.deck_pac.override_file_data(deck_file, new_deck)

    def __randomize_deck(self, pool, new_deck, deck_size, offset):
        deck = []
        for _ in range(deck_size):
            next_card = random.choice(pool)
            while deck.count(next_card) >= 3:
                next_card = random.choice(pool)
            
            deck.append(next_card)
        
        for i, next_card in enumerate(deck):
            address = offset + (i * 2)
            new_deck[address:address + 2] = next_card.to_bytes(2, byteorder='little', signed=False)
    
    def __shuffle_cpu_decks(self):
        deck_file_names = self.deck_pac.get_file_names()
        cpu_deck_names = []

        for name in deck_file_names:
            if any(keyword in name for keyword in ("rpg", "wcs")) and "_rd" not in name:
                cpu_deck_names.append(name)
        
        cpu_deck_names.remove("rpg001_0_syoki.ydc")
        
        decks = []
        for name in cpu_deck_names:
            decks.append(self.deck_pac.get_file_bytes(name))
        
        random.shuffle(decks)

        for i, name in enumerate(cpu_deck_names):
            header = 8
            # size = len(self.deck_pac.get_file_bytes(name))
            # new_deck = bytearray(size)
            new_deck = bytearray(len(decks[i]))
            new_deck[:header] = self.deck_pac.get_file_bytes(name)[:header]
            new_deck[header:len(decks[i])] = decks[i][header:]
            self.deck_pac.override_file_data(name, new_deck)
        

    def __load_card_pool(self):
        self.main_pool = []
        self.extra_pool = []

        with open("res/card_ids.json", "r") as file:
            cards = json.loads(file.read())

            self.main_pool.extend(cards["normal"])
            self.main_pool.extend(cards["effect"])
            self.main_pool.extend(cards["spell"])
            self.main_pool.extend(cards["trap"])
            self.main_pool.extend(cards["ritual"])
            
            self.extra_pool.extend(cards["fusion"])
            self.extra_pool.extend(cards["synchro"])
    
    def __import_rom(self):
        self.nds_tool.extract()

        bin2_path = Path("ndstool/temp/data/Data_arc_pac/bin2.pac")
        if bin2_path.is_file():
            self.bin2_pac = PacWrapper(str(bin2_path))
        else:
            raise RuntimeError("bin2.pac is missing")
        
        deck_path = Path("ndstool/temp/data/Data_arc_pac/deck.pac")
        if deck_path.is_file():
            self.deck_pac = PacWrapper(str(deck_path))
        else:
            raise RuntimeError("deck.pac is missing")
    
    def __export_rom(self, output_path):
        self.bin2_pac.repack()
        self.deck_pac.repack()
        self.nds_tool.build(output_path)