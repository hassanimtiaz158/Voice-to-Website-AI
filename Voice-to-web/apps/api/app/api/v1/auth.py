from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# TODO: implement. Keep this layer thin: validate input, call a service, return a schema.
