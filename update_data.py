#!/usr/bin/env python3
import logging

import fire

import etl.integration as ei

logger = logging.getLogger("palo_api")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

def update_data():
    logger.info("== Perform per source integration")
    logger.info("  Retrieving data from SRK source")
    srk_df = ei.integrate_srk("../data/covid/srk/covid_19_data.csv")  # TODO: online
    logger.info("  Concatenating with other sources")
    ei.write_data(srk_df, ei.DATAPOINTS_PATH, reset=True)

    logger.info("== Aggregating world totals")
    world_df = ei.aggregate_world()
    ei.write_data(world_df, ei.WORLD_PATH, reset=True)

if __name__ == "__main__":
    fire.Fire(update_data)
