VERSION = 1

NAME = _("Crawl")

DESCRIPTION = _("Decreases the movement rate of a unit.")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Diamond(1, 5, 16)

AOE = Single()

EFFECTS = [Status(Status.MINUS_MOVE, power=2.0, hit=0.5, duration=5)]

