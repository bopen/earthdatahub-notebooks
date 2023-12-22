# Scripts

## Script to automated create EUROSTATS notebook

The script to generate automated a Jupyter notebook for a EUROSTATS dataset
is `create_eurostat_data_notebook.py`.

In the script the `usecases` has to be adjusted so that for each usecase a notebook can be created. The usecase are looking for example link this:

```
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
    ...
]
```

The script uses the jinja2 templates in the `templates` folder. So if the notebooks has to be adjusted these templates has to be changed.

After executing the scripts the notebooks will be created in the `use-cases` folder. They should be tested and maybe the `time` has to be adjusted depending on the dataset.

Additinally, the notebooks has to be registered inside the `index.json`.
