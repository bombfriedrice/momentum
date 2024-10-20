import NBAStats from 0xc354a4406657fcab

transaction(momentID: UInt64, offense: UInt8, defense: UInt8, specialAbility: String) {
    prepare(signer: AuthAccount) {
        let metadata <- NBAStats.createMomentMetadata(momentID: momentID, offense: offense, defense: defense, specialAbility: specialAbility)
        signer.save(<-metadata, to: /storage/momentMetadata)
    }

    execute {
        log("Metadata added to Top Shot moment.")
    }
}