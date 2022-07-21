BULK_POST_NEW_COUNTRY = """
mutation PostNewCountry($input: [country_insert_input!]!) {
  insert_country(
    objects: $input,
    on_conflict: {
      constraint: country_pkey,
      update_columns: [name,capital,currency,currency_name,currency_symbol,emoji,iso2,iso3,latitude,longitude,
                        numeric_code,phone_code,region,subregion,tld ]
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

BULK_POST_NEW_STATE = """
mutation PostNewState($input: [state_insert_input!]!) {
  insert_state(
    objects: $input,
    on_conflict: {
      constraint: state_pkey,
      update_columns: [name, country_id, latitude, longitude, state_code, type]
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

BULK_POST_NEW_CITY = """
mutation PostNewCity($input: [city_insert_input!]!) {
  insert_city(
    objects: $input, 
    on_conflict: {
      constraint: city_pkey, 
      update_columns: [name, country_id, latitude, longitude, state_id]
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

GET_COUNTRIES = """
    query getCountries($filter: CountryFilterInput){
      countries(filter:$filter){
            id
            name
        }
    }
"""

GET_STATES = """
    query getStateS($filter: StateFilterInput){
      states(filter:$filter){
            id
            name
        }
    }
"""

GET_CITIES = """
    query getCities($filter: CityFilterInput){
      cities(filter:$filter){
            id
            name
        }
    }
"""

POST_NEW_VENUE = """
mutation postNewVenue($input: VenueInput){
  venueCreate(input: $input){
    errors{
      field
      message
      code
    }
    venue{
      id
      name
    }
  }
}
"""

GET_VENUE_BY_NAME = """
query GetVenueByName($name: String!) {
  venue(where: {name: {_eq: $name}}) {
    id
    name
  }
}
"""

GET_CITY_BY_NAME = """
query getCityByName($filter: CityFilterInput){
  cities(filter: $filter){
    edges{
      node{
        id
        name
        state{
          id
        }
        country{
          id
        }
      }
    }
  }
}
"""
