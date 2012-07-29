from twisted.spread import pb
import engine.Light
import engine.Map
import engine.Unit
import engine.Ability
import engine.Class
import engine.Scenario
import engine.Range
import engine.Effect
import engine.Light
import engine.Equipment
import engine.Battle

pb.setUnjellyableForClass(engine.Light.Light, engine.Light.Light)
pb.setUnjellyableForClass(engine.Map.MapSquare, engine.Map.MapSquare)
pb.setUnjellyableForClass(engine.Map.Map, engine.Map.Map)
pb.setUnjellyableForClass(engine.Unit.Unit, engine.Unit.Unit)
pb.setUnjellyableForClass(engine.Unit.StatusEffects, engine.Unit.StatusEffects)
pb.setUnjellyableForClass(engine.Ability.Ability, engine.Ability.Ability)
pb.setUnjellyableForClass(engine.Class.Class, engine.Class.Class)
pb.setUnjellyableForClass(engine.Scenario.Scenario, engine.Scenario.Scenario)
pb.setUnjellyableForClass(engine.Range.Line, engine.Range.Line)
pb.setUnjellyableForClass(engine.Range.Cross, engine.Range.Cross)
pb.setUnjellyableForClass(engine.Range.Diamond, engine.Range.Diamond)
pb.setUnjellyableForClass(engine.Range.DiamondExtend, engine.Range.DiamondExtend)
pb.setUnjellyableForClass(engine.Range.Single, engine.Range.Single)

pb.setUnjellyableForClass(engine.Effect.Damage, engine.Effect.Damage)
pb.setUnjellyableForClass(engine.Effect.DamageSP, engine.Effect.DamageSP)
pb.setUnjellyableForClass(engine.Effect.DrainLife, engine.Effect.DrainLife)
pb.setUnjellyableForClass(engine.Effect.HealFriendlyDamageHostile, engine.Effect.HealFriendlyDamageHostile)
pb.setUnjellyableForClass(engine.Effect.Healing, engine.Effect.Healing)       
pb.setUnjellyableForClass(engine.Effect.Status, engine.Effect.Status)
pb.setUnjellyableForClass(engine.Light.Light, engine.Light.Light)
pb.setUnjellyableForClass(engine.Light.White, engine.Light.White)
pb.setUnjellyableForClass(engine.Light.Point, engine.Light.Point)
pb.setUnjellyableForClass(engine.Light.Environment, engine.Light.Environment)
pb.setUnjellyableForClass(engine.Equipment.Weapon, engine.Equipment.Weapon)
pb.setUnjellyableForClass(engine.Equipment.Armor, engine.Equipment.Armor)
pb.setUnjellyableForClass(engine.Battle.Battle, engine.Battle.Battle)
pb.setUnjellyableForClass(engine.Battle.DefeatAllEnemies, engine.Battle.DefeatAllEnemies)
pb.setUnjellyableForClass(engine.Battle.PlayerDefeated, engine.Battle.PlayerDefeated)
pb.setUnjellyableForClass(engine.Effect.MissResult, engine.Effect.MissResult)
pb.setUnjellyableForClass(engine.Effect.DamageResult, engine.Effect.DamageResult)
pb.setUnjellyableForClass(engine.Effect.DamageSPResult, engine.Effect.DamageSPResult)
pb.setUnjellyableForClass(engine.Effect.HealResult, engine.Effect.HealResult)
pb.setUnjellyableForClass(engine.Effect.StatusResult, engine.Effect.StatusResult)


