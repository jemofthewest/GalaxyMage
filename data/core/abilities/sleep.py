VERSION = 1

NAME = _("Sleep")

DESCRIPTION = _("Put a opponent to sleep.")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Diamond(1, 5, 16)

AOE = Single()

EFFECTS = [Status(Status.SLEEP, power=0.1, duration=5)]
