VERSION = 1

NAME = _("Haste")

DESCRIPTION = _("Increases the speed of a unit.")

ABILITY_TYPE = ACTION

COST = 10

TARGET_TYPE = FRIENDLY

RANGE = Diamond(0, 5, 16)

AOE = Single()

EFFECTS = [Status(Status.HASTE, power=0.5, duration=5)]
