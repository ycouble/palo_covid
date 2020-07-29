#!/usr/bin/env python3
import logging

import fire

import etl.integration as ei

logger = logging.getLogger("palo_api")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

def update_date_country():
    # Perform per source integration
    logger.warning("Retrieving data from SRK source")
    srk_df = ei.integrate_srk("../data/covid/srk/covid_19_data.csv")  # TODO: online
    logger.info("Concatenating with other sources")
    ei.write_data(srk_df, reset=True)

if __name__ == "__main__":
    fire.Fire(update_date_country)
