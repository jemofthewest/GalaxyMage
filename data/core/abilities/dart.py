# "Dart" action ability.

VERSION = 1

NAME = "Dart"

DESCRIPTION = "Throw a dart."

COST = 5

ABILITY_TYPE = ACTION

TARGET_TYPE = HOSTILE

RANGE = Diamond(1, 5, 16)

AOE = Single()

EFFECTS = [Damage(power=1.0, damageType=PHYSICAL)]

SOUND = 'sword-hit-large'

