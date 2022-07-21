BULK_POST_NEW_DELIVERY = """
mutation PostNewGroupTeams($input: [delivery_insert_input!]!) {
  insert_delivery(
    objects: $input, 
    on_conflict: {
      constraint: delivery_delivery_pkey, 
      update_columns: [ball,batter_id,bowler_id,byes,innings_id,is_non_boundary,leg_byes,no_balls,non_striker_id,over,
                        penalty,review_id,runs_from_extras,runs_total,wides]
    }
  ) {
    affected_rows
    returning {
      ball
      unique_delivery_number
    }
  }
}
"""
