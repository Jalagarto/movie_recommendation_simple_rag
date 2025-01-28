### How to Run it

run it using docker:
1. build the docker image: `docker build . -t movie-recommendation-app`
2. run it: `docker run movie-recommendation-app`

or run it locally:
1. Install all dependencies: 
   1. `pip install poetry` if you do not have it installed in your env
   2. `poetry install --with dev` to install production and dev dependencies
2. `poetry run streamlit run src/app/serve.py`  or `streamlit run src/app/serve.py`

to execute tets I use: 
`poetry run pytest tests/`
to see the code coverage report:
`poetry run pytest tests/ --cov=src --cov-report=term-missing --cov-report=xml`

Note that main.py is there to be used locally, but not in production


#### Basic Project structure:

├── src
│   ├── agents
│   ├── app
│   ├── data
│   └── utils
└── tests
