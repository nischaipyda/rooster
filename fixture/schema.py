POST_NEW_VERSUS = """
mutation PostNewTeam($input: fixture_teams_insert_input!) {
  insert_fixture_teams_one(object: $input) {
    id
    team_a_id
    team_b_id
  }
}
"""

POST_NEW_TOSS = """
mutation postNewToss($input: TossInput){
  tossCreate(input: $input){
    errors{
      field
      message
      code
    }
    toss{
      id
      decision
      uncontested
      winner{
        id
      }
    }
  }
}
"""

POST_NEW_OUTCOME = """
mutation postNewOutcome($input: OutcomeInput){
  outcomeCreate(input: $input){
    errors{
      field
      message
    }
    outcome{
	  id
    }
  }
}
"""

POST_NEW_FIXTURE = """
mutation PostNewFixture($input: fixture_insert_input!) {
  insert_fixture_one(object: $input) {
    id
    innings {
      id
    }
    innings_aggregate {
      aggregate {
        count
      }
    }
    outcome {
      id
    }
    toss {
      id
    }
    tournament {
      id
    }
    versus {
      id
    }
  }
}

"""

POST_NEW_INNINGS = """
mutation postNewInnings($input: InningsInput){
  inningsCreate(input: $input){
    errors{
      field
      message
    }
  	innings{
	  id
      inningsNumber
    }
  }
}
"""

POST_NEW_FIXTURE_OFFICIAL = """
mutation postNewFixtureOfficial($input: FixtureOfficialsInput){
  fixtureOfficialCreate(input: $input){
    errors{
      field
      message
      code
    }
    fixtureOfficials{
      id
      official{
        id
        displayName
      }
    }
  }
}
"""
POST_NEW_PLAYING_XI_FIXTURE = """
mutation postNewPlayingXIFixture($input: PlayingXIFixturesInput){
  playingXiFixtureCreate(input: $input){
    errors{
      field
      message
      code
    }
    playingXIFixtures{
      id
      player{
        id
        name
      }
      team{
        name
      }
    }
  }
}
"""
GET_STAGE_BY_NAME = """
query GetStageByName($name: String!) {
  stage(where: {name: {_eq: $name}}) {
    id
  }
}
"""
GET_FIXTURE_BY_ID = """
query GetFixtureById($id: Int!) {
  fixture_by_pk(id: $id) {
    id
    innings {
      id
    }
    outcome {
      id
    }
    versus {
      id
    }
    toss {
      id
    }
  }
}
"""
