#!/usr/bin/env python3
import fire

import etl.integration as ei

def update_date_country():
    # Perform per source integration
    srk_df = ei.integrate_srk("../data/covid/srk/covid_19_data.csv")  # TODO: online
    ei.write_data(srk_df, reset=True)
    # to remove
    ei.write_data(ei.tag_source(srk_df, "srk2"))

if __name__ == "__main__":
    fire.Fire(update_date_country)
