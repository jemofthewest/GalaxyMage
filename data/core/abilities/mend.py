VERSION = 1

NAME = "Mend"

DESCRIPTION = "A weak healing spell."

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = FRIENDLY

RANGE = Diamond(0, 5, 16)

AOE = Single()

EFFECTS = [Healing(power=2.0)]


