FROM paraplan:latest

COPY src/ ./src/

ENTRYPOINT [ "uv", "run", "python3", "-m", "src.daemon" ]
