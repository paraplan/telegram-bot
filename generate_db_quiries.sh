#!/bin/bash
uv run edgedb-py --dir src/database/queries --target async --file src/database/generated.py
