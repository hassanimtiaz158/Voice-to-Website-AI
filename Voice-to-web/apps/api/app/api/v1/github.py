from fastapi import APIRouter

router = APIRouter(prefix="/github", tags=["github"])

# TODO: implement. Keep this layer thin: validate input, call a service, return a schema.
