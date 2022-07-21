GET_ALL_TOURNAMENTS_BY_SERIES_AND_FORMAT = """
query GetTournament($series: bigint!, $format: String!) {
  tournament(where: {series_id: {_eq: $series}, format: {_eq: $format}}) {
    id
    format
    series {
      id
    }
  }
}

"""

GET_ALL_GROUPS_BY_TOURNAMENT = """
query GetAllGroupsByTournament($tournament: bigint, $name: String) {
  group(where: {tournament_id: {_eq: $tournament}, name: {_eq: $name}}) {
    id
    name
    tournament_id
  }
}
"""

GET_GROUPS_TEAMS_COUNT_BY_TOURNAMENT = """
query GetGroupCountByTournament($tournament: bigint) {
  group_aggregate(where: {tournament_id: {_eq: $tournament}}) {
    aggregate {
      count(distinct: false)
    }
  }
  group_teams_aggregate(where: {group: {tournament_id: {_eq: $tournament}}}) {
    aggregate {
      count
    }
  }
}
"""

POST_NEW_TOURNAMENT = """
mutation PostNewTournament($input: tournament_insert_input!) {
  insert_tournament_one(object: $input) {
    id
  }
}
"""

POST_NEW_GROUP = """
mutation PostNewGroup($input: group_insert_input!) {
  insert_group_one(object: $input) {
    name
    id
    tournament_id
  }
}

"""

POST_NEW_GROUP_TEAMS = """
mutation PostNewGroupTeams($input: [group_teams_insert_input!]!) {
  insert_group_teams(
    objects: $input, 
    on_conflict: {
      constraint: group_teams_team_id_group_id_d7fe059b_uniq, 
      update_columns: []
    }
  ) {
    affected_rows
    returning {
      team_id
      group_id
    }
  }
}
"""

UPDATE_TOURNAMENT_START_DATE = """
mutation UpdateTournamentStateDate($tournament: bigint!, $start_date: date!) {
  update_tournament(where: {id: {_eq: $tournament}, start_date: {_gt: $start_date}}, _set: {start_date: $start_date}) {
    affected_rows
    returning {
      id
      start_date
    }
  }
}
"""

UPDATE_TOURNAMENT_END_DATE = """
mutation UpdateTournamentEndDate($tournament: bigint!, $end_date: date!) {
  update_tournament(where: {id: {_eq: $tournament}, end_date: {_lt: $end_date}}, _set: {end_date: $end_date}) {
    affected_rows
    returning {
      id
      end_date
    }
  }
}
"""

UPDATE_TOURNAMENT_GROUPS_AND_TEAMS_COUNT = """
mutation PostNewGroupTeams($tournament: bigint!, $groups_count: Int!, $teams_count: Int!) {
  update_tournament_by_pk(
    pk_columns: {id: $tournament}, 
    _set: {groups_count: $groups_count, teams_count: $teams_count}
  ) {
    id
    teams_count
    groups_count
  }
}
"""
