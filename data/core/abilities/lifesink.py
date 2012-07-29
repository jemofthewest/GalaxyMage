VERSION = 1

NAME = _("Life Sink")

DESCRIPTION = _("A relatively strong, life draining attack.")

ABILITY_TYPE = ACTION

COST = 20

TARGET_TYPE = HOSTILE

RANGE = Diamond(0, 4, 16)

AOE = Diamond(0,1)

EFFECTS = [DrainLife(power=2.0, percentDamageHealed=0.5, damageType=MAGICAL)]

SOUND = 'fire'

