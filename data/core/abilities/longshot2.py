# "Extend" action ability.

VERSION = 1

NAME = "Long Shot 2"

DESCRIPTION = "Shoot a long-distance arrow."

COST = 10

ABILITY_TYPE = ACTION

TARGET_TYPE = HOSTILE

RANGE = DiamondExtend(2)

AOE = Single()

EFFECTS = [Damage(power=1.0, damageType=PHYSICAL)]

SOUND = WEAPON_SOUND

REQUIRED_WEAPONS = [Weapon.BOW]
