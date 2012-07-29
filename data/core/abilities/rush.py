VERSION = 1

NAME = "Rush"

DESCRIPTION = "A slightly more powerful attack."

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Cross(1, 1)

AOE = Line(2)

EFFECTS = [Damage(power=1.25, damageType=PHYSICAL)]

SOUND = WEAPON_SOUND
