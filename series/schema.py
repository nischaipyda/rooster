GET_ALL_SERIES_BY_NAME = """
query GetAllSeriesByName($name: String!, $gender: String!, $pool: String!, $season: String!) {
  series(where: {name: {_eq: $name}, gender: {_eq: $gender}, pool: {_eq: $pool}, season: {_eq: $season}}) {
    id
    name
    start_date
    end_date
    season
  }
}


"""
POST_NEW_SERIES = """
mutation PostNewTeam($input: series_insert_input!) {
  insert_series_one(object: $input) {
    id
    name
  }
}
"""

POST_NEW_SERIES_TEAMS = """
mutation PostNewSeriesTeams($input: [series_teams_insert_input!]!) {
  insert_series_teams(
    objects: $input, 
    on_conflict: {
      constraint: series_teams_team_id_series_id_ea1d8564_uniq, 
      update_columns: []
    }
  ) {
    affected_rows
    returning {
      series {
        id
        name
      }
      team {
        id
        name
      }
    }
  }
}
"""

UPDATE_SERIES_START_DATE = """
mutation UpdateSeriesStateDate($series: bigint!, $start_date: date!) {
  update_series(where: {id: {_eq: $series}, start_date: {_gt: $start_date}}, _set: {start_date: $start_date}) {
    affected_rows
    returning {
      id
      start_date
    }
  }
}
"""

UPDATE_SERIES_END_DATE = """
mutation UpdateSeriesEndDate($series: bigint!, $end_date: date!) {
  update_series(where: {id: {_eq: $series}, end_date: {_lt: $end_date}}, _set: {end_date: $end_date}) {
    affected_rows
    returning {
      id
      end_date
    }
  }
}
"""

