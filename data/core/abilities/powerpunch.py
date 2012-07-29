VERSION = 1

NAME = "Power Punch"

DESCRIPTION = "This punch packs some extra power."

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Cross(1, 1)

AOE = Single()

EFFECTS = [Damage(power=1.5, damageType=PHYSICAL)]

SOUND = WEAPON_SOUND

REQUIRED_WEAPONS = [Weapon.HAND]
