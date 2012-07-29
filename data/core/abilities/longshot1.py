# "Extend" action ability.

VERSION = 1

NAME = "Long Shot 1"

DESCRIPTION = "Shoot a long-distance arrow."

COST = 5

ABILITY_TYPE = ACTION

TARGET_TYPE = HOSTILE

RANGE = DiamondExtend(1)

AOE = Single()

EFFECTS = [Damage(power=1.0, damageType=PHYSICAL)]

SOUND = WEAPON_SOUND

REQUIRED_WEAPONS = [Weapon.BOW]
