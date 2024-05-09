# Overview

This service provides API for the GoF pattern prediction

## How does it work

The server runs on 8000 port, and has only 1 service `/predict`, which allows users to predict GoF patterns inside of a Java class

The server also requires [trained code2vec model](https://github.com/PetrovaAnastasiax), you can configure path to model in `code2vec/config.py`

## How to run

> fastapi main.py
