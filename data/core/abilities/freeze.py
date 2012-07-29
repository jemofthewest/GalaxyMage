VERSION = 1

NAME = _("Freeze")

DESCRIPTION = _("Weak ice spell. (Sometimes freezes.)")

ABILITY_TYPE = ACTION

COST = 5

TARGET_TYPE = HOSTILE

RANGE = Diamond(1, 5, 16)

AOE = Single()

EFFECTS = [Damage(power=1.0, damageType=ICE),
           Status(Status.FREEZE, hit=0.1, duration=3)]
