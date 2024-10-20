import NBAStats from 0xc354a4406657fcab

pub fun main(momentID: UInt64): {String: AnyStruct} {
    let metadata = getAccount(0xc354a4406657fcab).getCapability(/public/momentMetadata)
                      .borrow<&NBAStats.MomentMetadata>() 
                      ?? panic("No metadata found for the moment")

    return {
        "momentID": metadata.momentID,
        "offense": metadata.offense,
        "defense": metadata.defense,
        "specialAbility": metadata.specialAbility
    }
}