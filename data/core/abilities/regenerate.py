VERSION = 1

NAME = _("Regenerate")

DESCRIPTION = _("Gives your ally regeneration.")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = FRIENDLY

RANGE = Diamond(0, 5, 16)

AOE = Single()

EFFECTS = [Status(Status.REGEN, power=0.2, duration=5)]

