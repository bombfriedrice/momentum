pub contract NBAStats {

    pub resource MomentMetadata {
        pub let momentID: UInt64
        pub var offense: UInt8
        pub var defense: UInt8
        pub var specialAbility: String

        init(momentID: UInt64, offense: UInt8, defense: UInt8, specialAbility: String) {
            self.momentID = momentID
            self.offense = offense
            self.defense = defense
            self.specialAbility = specialAbility
        }
    }

    pub fun createMomentMetadata(momentID: UInt64, offense: UInt8, defense: UInt8, specialAbility: String): @MomentMetadata {
        return <- create MomentMetadata(momentID: momentID, offense: offense, defense: defense, specialAbility: specialAbility)
    }
}