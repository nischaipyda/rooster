GET_TEAM_BY_NAME = """
query GetTeamByName($name: String) {
  team(where: {name: {_ilike: $name}}) {
    id
    name
  }
}
"""

POST_NEW_TEAM = """
mutation PostNewTeam($input: [team_insert_input!]!) {
  insert_team(
    objects: $input, 
    on_conflict: {
      constraint: team_team_name_short_name_pool_id_gender_id_a75fbbe5_uniq,
       update_columns: [name,city_id,country_id,gender,pool,primary_color,secondary_color,short_name]
    }
  ) {
    affected_rows
    returning {
      id
      name
    }
  }
}

"""