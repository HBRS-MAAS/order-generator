# Scenario generator
[![Build Status](https://travis-ci.org/HBRS-MAAS/scenario-generator.svg?branch=master)](https://travis-ci.org/HBRS-MAAS/scenario-generator)

Creates a random scenario based on the parameters from the `scenarios.yaml` config file.

The current names for bakeries, customers and products are read from the corresponding `.yaml` files in the config folder.  
If you want something added, please send a pull request!

## The scripts
To generate a new random scenario, simply run the following command:

```bash
./scenario_generator
```

Note: This will overwrite the random-scenario files in the `scenarios` folder.
