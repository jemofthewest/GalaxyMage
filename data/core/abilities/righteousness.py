VERSION = 1

NAME = _("Righteousness")

DESCRIPTION = _("Call forth a righteous flame.")

ABILITY_TYPE = ACTION

#COST = 75
COST = 25

TARGET_TYPE = FRIENDLY_AND_HOSTILE

RANGE = Diamond(0, 4, 16)

AOE = Diamond(0, 2)

EFFECTS = [HealFriendlyDamageHostile(power=1.0, damageType=FIRE),
           HealFriendlyDamageHostile(power=1.0, damageType=HOLY)]

SOUND = 'fire'

