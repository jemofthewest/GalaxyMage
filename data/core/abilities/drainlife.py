VERSION = 1

NAME = _("Drain Life")

DESCRIPTION = _("Regenerate yourself at the expense of your enemy.")

ABILITY_TYPE = ACTION

COST = 10

TARGET_TYPE = HOSTILE

RANGE = Diamond(0, 4, 16)

AOE = Single()

EFFECTS = [DrainLife(power=1.0, percentDamageHealed=1.0, damageType=MAGICAL)]

SOUND = 'fire'

