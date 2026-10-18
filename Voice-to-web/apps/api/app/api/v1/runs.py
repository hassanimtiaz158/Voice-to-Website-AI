from fastapi import APIRouter

router = APIRouter(prefix="/runs", tags=["runs"])

# TODO: implement. Keep this layer thin: validate input, call a service, return a schema.
