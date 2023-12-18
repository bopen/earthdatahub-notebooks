#!/usr/bin/env python3

############################################################################
#
# MODULE:       Script to generate Jupyter Notebook for EUROSTATS datasets
#
# AUTHOR(S):    Anika Weinmann, Momen Mawad
#
# PURPOSE:      Generation of Jupyter Notebooks for EUROSTATS datasets
#
# COPYRIGHT:	(C) 2023 by mundialis
#
# 		This program is free software under the GNU General Public
# 		License (>=v2). Read the file COPYING that comes with GRASS
# 		for details.
#
#############################################################################

import os

from jinja2 import Template


# parameter for dataset
usecases = [
    {
        "name": "final energy consumption",
        "title": "EUROSTAT Final Consumption of Energy data over Europe",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-final-energy-consumption_sdg_07_11",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/sdg_07_11_esmsip2.htm",
        "dataset_zarr": "sdg_07_11-20000101-20210101.zarr",
        "dataset_var": "L0_TOE_HAB",
        "dataset_var_desc": "on NUTS level 0 (country level) in the unit of ton of oil equivalent per habitant",
    },
    {
        "name": "soil erosion",
        "title": "Europe EUROSTAT soil erosion",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-soil-erosion-aei_pr_soiler",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/aei_pr_soiler_esms.htm",
        "dataset_zarr": "aei_pr_soiler-20000101-20160101.zarr",
        "dataset_var": "L3_TOTAL_CLC2_321_T",
        "dataset_var_desc": "on NUTS level 3 in the unit of tonnes per year for the soil erosion of agriculture areas and natural grassland",
    },
    {
        "name": "population density",
        "title": "Eurostat population density data over Europe",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-population-density-demo_r_d3dens",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/demo_pop_esms.htm",
        "dataset_zarr": "demo_r_d3dens-19900101-20220101.zarr",
        "dataset_var": "L3_PER_KM2",
        "dataset_var_desc": "on NUTS level 3 in the unit of persons per square kilometre",
    },
    {
        "name": "animal populations",
        "title": "Europe EUROSTAT Animal populations by NUTS 2 regions",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-animal-populations-agr_r_animal",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/apro_anip_esms.htm",
        "dataset_zarr": "agr_r_animal-19770101-20230101.zarr",
        "dataset_var": "L2_A2000_THS_HD",
        "dataset_var_desc": "on NUTS level 2 in the unit of thousands of heads",
    },
    {
        "name": "mortality",
        "title": "Eurostat mortality data over Europe",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-mortality-demo_r_mweek3",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/demomwk_esms.htm",
        "dataset_zarr": "demo_r_mweek3-20000103-20231030.zarr",
        "dataset_var": "L3_NR_T_Y65_69",
        "dataset_var_desc": "on NUTS level 3 in the unit of total number of deaths for the age group 65-69",
    },
    {
        "name": "population",
        "title": "Eurostat population data over Europe",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-population-demo_r_pjanaggr3",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/demo_r_gind3_esms.htm",
        "dataset_zarr": "demo_r_pjanaggr3-19900101-20220101.zarr",
        "dataset_var": "L3_NR_T_Y_LT15",
        "dataset_var_desc": "on NUTS level 3 in the unit of total number of population lower than 15 years",
    },
    {
        "name": "government deficit and debt",
        "title": "Europe EUROSTAT Government deficit and debt",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-government-deficit-surplus-gov_10dd_edpt1",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/gov_10dd_esms.htm",
        "dataset_zarr": "gov_10dd_edpt1-19950101-20220101.zarr",
        "dataset_var": "L0_MIO_EUR_S13_B9",
        "dataset_var_desc": "on NUTS level 0 (country level) in the unit of net borrowing or net lending of the consolidated general government sector millions of euro",
    },
    {
        "name": "labour market employment rates",
        "title": "Eurostat Regional Labour Market Employment Rates",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-employment-rates_lfst_r_erednu",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/reg_lmk_esms.htm",
        "dataset_zarr": "lfst_r_erednu-19950101-20220101.zarr",
        "dataset_var": "L0_TOTAL_TOTAL_TOTAL_Y15_64_T_PC",
        "dataset_var_desc": "on NUTS level 0 (country level) in the unit of number of persons (thousands) in age group of 15-64 years",
    },
    {
        "name": "gross domestic product",
        "title": "Europe Gross domestic product (GDP)",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-regional-economic-accounts_nama_10r_3gdp",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/reg_eco10_esms.htm",
        "dataset_zarr": "nama_10r_3gdp-20000101-20210101.zarr",
        "dataset_var": "L3_MIO_EUR",
        "dataset_var_desc": "on NUTS level 3 in the unit of millions of Euros",
    },
    {
        "name": "gerd",
        "title": "Europe EUROSTAT GERD",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-gross-domestic-expenditure-R-D-rd_e_gerdreg",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/rd_esms.htm",
        "dataset_zarr": "rd_e_gerdreg-19800101-20220101.zarr",
        "dataset_var": "L2_GOV_EUR_HAB",
        "dataset_var_desc": "on NUTS level 2 in the unit of Euro per inhabitant for the institutional sector government",
    },
    {
        "name": "CDD and HDD data",
        "title": "Eurostat CDD & HDD data over Europe",
        "metadata_link": "https://earthdatahub.com/collections/eurostat/datasets/geoprocessed-eurostat-cooling-heating-degree-days-nrg_chddr2_a",
        "eurostat_link": "https://ec.europa.eu/eurostat/cache/metadata/en/nrg_chdd_esms.htm",
        "dataset_zarr": "nrg_chddr2_a-19790101-20220101.zarr",
        "dataset_var": ["L3_NR_CDD", "L3_NR_HDD"],
        "dataset_var_desc": "heating degree day (HDD) and cooling degree day (CDD) on NUTS level 3 in the unit of Kelvin",
    },
]


for usecase in usecases:
    dataset_name = usecase["name"]
    # notebook file
    notebook_file = os.path.join(
        "..",
        "use-cases",
        f"eurostats_{dataset_name.replace(' ', '-')}.ipynb",
    )

    # read template and create notbook file
    if isinstance(usecase["dataset_var"], str):
        with open("templates/eurostats_template.ipynb") as tpl_file:
            template = Template(tpl_file.read())
        rendered_plt = template.render(
            title=usecase["title"],
            dataset_name=usecase["name"],
            metadata_link=usecase["metadata_link"],
            eurostat_link=usecase["eurostat_link"],
            dataset_zarr=usecase["dataset_zarr"],
            dataset_var=usecase["dataset_var"],
            dataset_var_desc=usecase["dataset_var_desc"],
        )
    else:
        with open(
            "templates/eurostats_several_vars_template.ipynb"
        ) as tpl_file:
            template = Template(tpl_file.read())
        rendered_plt = template.render(
            title=usecase["title"],
            dataset_name=usecase["name"],
            metadata_link=usecase["metadata_link"],
            eurostat_link=usecase["eurostat_link"],
            dataset_zarr=usecase["dataset_zarr"],
            dataset_var=usecase["dataset_var"],
            dataset_var_desc=usecase["dataset_var_desc"],
        )
    with open(notebook_file, "w") as notebook:
        notebook.write(rendered_plt)
