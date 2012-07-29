VERSION = 1

NAME = _("Defend")

DESCRIPTION = _("Increase your defense temporarily.")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = FRIENDLY

RANGE = Single()

AOE = Single()

EFFECTS = [Status(Status.PLUS_WDEF, power=0.5, duration=3)]
