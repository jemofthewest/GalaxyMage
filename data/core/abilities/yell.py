VERSION = 1

NAME = _("Yell")

DESCRIPTION = _("Yell, dazing enemies and damaging them slightly.")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Single()

AOE = Diamond(0,3)

EFFECTS = [Damage(power=0.5, damageType=MAGICAL),
           Status(Status.PARALYZE, hit=.7, duration=1)]
