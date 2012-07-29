VERSION = 1

NAME = _("Hold")

DESCRIPTION = _("Holds an enemy in place.")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Diamond(1, 5, 16)

AOE = Single()

EFFECTS = [Status(Status.PARALYZE_LEGS, hit=0.5, duration=5)]
