# Image the Tester runs generated code in. No network, non-root, resource-limited at run time.
FROM python:3.12-slim
RUN useradd -m runner
USER runner
WORKDIR /workspace
