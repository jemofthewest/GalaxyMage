VERSION = 1

NAME = _("Fire")

DESCRIPTION = _("Weak fire spell.")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Diamond(0, 4, 16)

AOE = Diamond(0, 1)

EFFECTS = [Damage(power=1.0, damageType=FIRE)]

SOUND = 'fire'

