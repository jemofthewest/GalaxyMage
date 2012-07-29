VERSION = 1

NAME = _("Bite of The Vampire")

DESCRIPTION = _("Bite into your enemy and drink her blood!")

ABILITY_TYPE = ACTION

COST = 0

TARGET_TYPE = HOSTILE

RANGE = Cross(1, 1)

AOE = Single()

EFFECTS = [DrainLife(power=0.50, percentDamageHealed=2.0, damageType=MAGICAL)]
