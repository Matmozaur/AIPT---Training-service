import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp

from api.endpoints_training import router_trainings
from services.graphql_service import schema

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s:%(lineno)d:  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(router_trainings, prefix="/v1/training")

app.add_route("/graphql", GraphQLApp(schema=schema))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
