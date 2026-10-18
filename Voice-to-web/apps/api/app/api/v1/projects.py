from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["projects"])

# TODO: implement. Keep this layer thin: validate input, call a service, return a schema.
