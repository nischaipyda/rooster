BULK_POST_NEW_PERSON = """
mutation PostNewPeople($input: [person_insert_input!]!) {
  insert_person(
    objects: $input, 
    on_conflict: {
      constraint: person_pkey, 
      update_columns: [name,display_name,key_bigbash,key_cricbuzz,key_crichq,key_cricinfo,key_cricinfo_2,key_cricingif,
                        key_cricketarchive,key_cricketarchive_2,key_opta,key_opta_2,key_pulse,key_pulse_2]
    }
  ) {
    affected_rows
    returning {
      id
      display_name
    }
  }
}
"""

