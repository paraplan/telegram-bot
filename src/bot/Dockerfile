FROM paraplan:latest

COPY templates/ ./templates/
COPY src/ ./src/

COPY alembic.ini ./
COPY migrations/ ./migrations/

RUN chmod +x /app/src/bot/docker-entrypoint.sh

ENTRYPOINT [ "/app/src/bot/docker-entrypoint.sh" ]
