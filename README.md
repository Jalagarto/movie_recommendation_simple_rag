run it using docker:
1. build the docker image: `docker build . -t movie-recommendation-app`
2. run it: `docker run movie-recommendation-app`

or run it locally:
1. Install all dependencies: 
   1. `pip install poetry` if you do not have it installed in your env
   2. `poetry install --with dev` to install production and dev dependencies
2. `streamlit run src/app/serve.py`

to execute tets I use: 
`poetry run pytest tests/`