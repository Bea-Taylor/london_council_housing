import pandas as pd
import numpy as np
import re

def res_units_x_query(es, x_res_units, since_year="01/01/2014", to_year="now"):
    """Elastic Search query to filter applications with a minimum number of proposed residential units.

    Args:
        es (obj): Elastic Search object.
        x_res_units (int): Minimum number of proposed residential units.
        since_year (str, optional): Initial date of the search. Defaults to "01/01/2014".

    Returns:
        dataframe: Dataframe with the filtered applications.
    """

    query = {
    "query": {
        "bool": {
        "must": [
            {
            "range": {
                "application_details.residential_details.total_no_proposed_residential_units": {
                "gte": x_res_units
                }
            }
            },
            {
            "range": {
                "valid_date": {
                "gte": since_year,
                "lt": to_year  
                }
            }
            }
        ],
        "must_not": [
            {
            "term": {
                "status.keyword": "Superseded"
            }
            }
        ]
        }
    },
    "_source": [
        "borough",
        "decision_date",
        "valid_date",
        "decision",
        "actual_completion_date",
        "application_details.residential_details.total_no_proposed_residential_units",
        "application_details.residential_details.site_area",
        "application_details.affordable_housing_fast_track",
        "application_details.residential_details.total_no_affordable_units",
        "application_details.residential_details.total_no_proposed_residential_units_discount_market_rent",
        "application_details.residential_details.total_no_proposed_residential_units_discount_market_rent_charged_at_london_rents",
        "application_details.residential_details.total_no_proposed_residential_units_discount_market_sale",
        "application_details.residential_details.total_no_proposed_residential_units_intermediate",
        "application_details.residential_details.total_no_proposed_residential_units_london_affordable_rent",
        "application_details.residential_details.total_no_proposed_residential_units_london_living_rent",
        "application_details.residential_details.total_no_proposed_residential_units_london_shared_ownership",
        "application_details.residential_details.total_no_proposed_residential_units_market_for_rent",
        "application_details.residential_details.total_no_proposed_residential_units_market_for_sale",
        "application_details.residential_details.total_no_proposed_residential_units_self_build_and_custom_build",
        "application_details.residential_details.total_no_proposed_residential_units_shared_equity",
        "application_details.residential_details.total_no_proposed_residential_units_social_rent",
        "application_details.residential_details.total_no_proposed_residential_units_starter_homes",
        "status",
        "id",
        "pp_id",
        "lpa_name",
        "lpa_app_no",
        "site_name",
        "site_number",
        "street_name",
        "uprn",
        "polygon",
        "wgs84_polygon"
    ]
    }


    # Initialise scrolling
    response = es.search(index="applications", body=query, scroll="2m", size=10000)
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    
    all_hits = []
    all_hits.extend(hits)

    # Keep scrolling until no hits are returned
    while len(hits) > 0:
        response = es.scroll(scroll_id=scroll_id, scroll="2m")
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']
        all_hits.extend(hits)

    # Normalize the results into a DataFrame
    df = pd.json_normalize(all_hits)

    return df


def social_units_x_query(es, x_res_units, since_year="01/01/2014", to_year="now"):
    """Elastic Search query to filter applications with a minimum number of proposed social rent units.

    Args:
        es (obj): Elastic Search object.
        x_res_units (int): Minimum number of proposed residential units.
        since_year (str, optional): Initial date of the search. Defaults to "01/01/2014".

    Returns:
        dataframe: Dataframe with the filtered applications.
    """

    query = {
    "query": {
        "bool": {
        "must": [
            {
            "range": {
                "application_details.residential_details.total_no_proposed_residential_units_social_rent": { # this line specifies only applications which add council housing  
                "gte": x_res_units
                }
            }
            },
            {
            "range": {
                "valid_date": {
                "gte": since_year,
                "lt": to_year  
                }
            }
            }
        ],
        "must_not": [
            {
            "term": {
                "status.keyword": "Superseded"
            }
            }
        ]
        }
    },
    "_source": [
        "borough",
        "decision_date",
        "valid_date",
        "decision",
        "actual_completion_date",
        "application_details.residential_details.total_no_proposed_residential_units",
        "application_details.residential_details.site_area",
        "application_details.affordable_housing_fast_track",
        "application_details.residential_details.total_no_affordable_units",
        "application_details.residential_details.total_no_proposed_residential_units_discount_market_rent",
        "application_details.residential_details.total_no_proposed_residential_units_discount_market_rent_charged_at_london_rents",
        "application_details.residential_details.total_no_proposed_residential_units_discount_market_sale",
        "application_details.residential_details.total_no_proposed_residential_units_intermediate",
        "application_details.residential_details.total_no_proposed_residential_units_london_affordable_rent",
        "application_details.residential_details.total_no_proposed_residential_units_london_living_rent",
        "application_details.residential_details.total_no_proposed_residential_units_london_shared_ownership",
        "application_details.residential_details.total_no_proposed_residential_units_market_for_rent",
        "application_details.residential_details.total_no_proposed_residential_units_market_for_sale",
        "application_details.residential_details.total_no_proposed_residential_units_self_build_and_custom_build",
        "application_details.residential_details.total_no_proposed_residential_units_shared_equity",
        "application_details.residential_details.total_no_proposed_residential_units_social_rent",
        "application_details.residential_details.total_no_proposed_residential_units_starter_homes",
        "status",
        "id",
        "pp_id",
        "lpa_name",
        "lpa_app_no",
        "site_name",
        "site_number",
        "street_name",
        "postcode",
        "uprn",
        "polygon",
        "wgs84_polygon",
        "description"
    ]
    }

    # Initialise scrolling
    response = es.search(index="applications", body=query, scroll="2m", size=10000)
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    
    all_hits = []
    all_hits.extend(hits)

    # Keep scrolling until no hits are returned
    while len(hits) > 0:
        response = es.scroll(scroll_id=scroll_id, scroll="2m")
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']
        all_hits.extend(hits)

    # Normalize the results into a DataFrame
    df = pd.json_normalize(all_hits)

    return df