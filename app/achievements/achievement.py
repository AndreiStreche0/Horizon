from enum import Enum

class AchievementTier(Enum):
    BRONZE = 0
    SILVER = 1
    GOLD = 2

class Achievement:
    def __init__(self, name, description, tiers):
        self.name = name
        self.description = description
        self.tiers = tiers  # [bronze, silver, gold]
        self.unlockedTier = None  # None, BRONZE, SILVER, or GOLD
        
    def get_tier_name(self, tier):
        tier_names = {
            AchievementTier.BRONZE: "Bronze",
            AchievementTier.SILVER: "Silver",
            AchievementTier.GOLD: "Gold"
        }
        return tier_names.get(tier, "Unknown")
    
    def get_description_for_tier(self, tier):
        if tier == AchievementTier.BRONZE:
            return self.description % self.tiers[0]
        elif tier == AchievementTier.SILVER:
            return self.description % self.tiers[1]
        elif tier == AchievementTier.GOLD:
            return self.description % self.tiers[2]
        return self.description
    
    def get_current_description(self):
        if self.unlockedTier:
            return self.get_description_for_tier(self.unlockedTier)
        return self.description % self.tiers[0]
    
    def unlock(self, tier):
        if self.unlockedTier is None or tier.value > self.unlockedTier.value:
            self.unlockedTier = tier
            return True
        return False
    
    def is_unlocked(self):
        return self.unlockedTier is not None
    
    def get_tier_value(self, tier):
        return self.tiers[tier.value]