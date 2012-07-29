VERSION = 1

NAME = _("Protect")

DESCRIPTION = _("Protect a friend for one turn.")

ABILITY_TYPE = ACTION

COST = 20

TARGET_TYPE = FRIENDLY

RANGE = Diamond(0, 4, 16)

AOE = Single()

EFFECTS = [Status(Status.INVULNERABLE, duration=1)]

