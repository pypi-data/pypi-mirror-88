# Bakplane Client for Python
Bakplane is the orchestration backbone for Dominus, FinFlo, and Fabrik.

This SDK can be used to control ingestion sessions, mastering executions, plugin installation, etc. 

As an example, we use this package to with Airflow to control ingestion orchestration. 

## Installation
Installing the bakplane python client takes just a few seconds:
```bash
pip install bakplane-python-sdk
```

## Bindings
If you're a contributor and would like to generate the bindings from proto then run:

```bash
scripts/proto.sh
```

## Examples
If you want to explore the notebooks then install `jupyter`:
```shell script
pip install jupyter
cd bakplane/examples
jupyter notebook
```

## Packages
If you want to build a new bakplane binary then run:

```shell script
git tag -a v1.1.1 -m "Bakplane SDK Release"
git push origin v1.1.1
```

Then you may find the packages available here: https://github.com/openaristos/bakplane-python-sdk/releases

## Spark
Start spark in Docker:
```shell script
docker run -it --rm -p 8888:8888 --name pyspark jupyter/pyspark-notebook
```

Copy the latest python package, and the notebooks, onto the cluster:
```shell script
scripts/package.sh
docker cp dist/bakplane-python-sdk-1.1.1.tar.gz pyspark:/tmp/
docker cp bakplane/examples/notebooks/spark.ipynb pyspark:/home/jovyan/work/
```

Note: use `host.docker.internal` instead of `localhost` when testing.

Then start the jupyter notebook by clicking on the link provided by the Docker container.

## Documentation
If you're interested in learning more then read the documentation: https://oa.docs.openaristos.io/

<h1 align="center">
    <img src="https://gist.githubusercontent.com/daefresh/32418b316dda99eb537fcef08b4c88af/raw/f4ed8e6fb4fd343eb61541c76871233d1105d2ec/bakplane_logo.svg" alt="Bakplane"/>
</h1>

Copyright (C) 2020 Aristos Data, LLC