### How to Run it

Run it using docker:
1. build the docker image: `docker build . -t movie-recommendation-app`
2. run it: `docker run -p 8501:8501 movie-recommendation-app`

or run it locally:
1. Install all dependencies: 
   1. `pip install poetry` if you do not have it installed in your env
   2. `poetry install --with dev` to install production and dev dependencies
2. `poetry run streamlit run src/app/serve.py`  or `streamlit run src/app/serve.py`

To execute tets use: 
`poetry run pytest tests/`

To also see the code coverage report:
`poetry run pytest tests/ --cov=src --cov-report=term-missing --cov-report=xml`

Note that main.py is there to be used locally, but not in production


#### Basic Project structure:
```
├── src
│   ├── agents
│   ├── app
│   ├── data
│   └── utils
└── tests
```

To access the Documentation and a Report of the works done see the [wiki](https://github.com/Jalagarto/movie_recommendation_simple_rag/wiki/Movie-Recommendation-Chatbot-with-RAG)
