VERSION = 1

NAME = _("Slow")

DESCRIPTION = _("Decreases the speed of a unit.")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Diamond(1, 5, 16)

AOE = Single()

EFFECTS = [Status(Status.SLOW, power=1.0, hit=0.5, duration=5)]

