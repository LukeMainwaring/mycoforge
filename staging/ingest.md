# Ingest queue

Sources captured in `raw/` that have not been ingested yet, in recommended
order. One source per session: run Ingest, tick the row once the `ingest |` log
entry exists. The "watch out" line is the question most likely to pull the session off
course, usually where the source argues with this KB's own conventions. It is a
prompt to evaluate, not a conclusion; per the Ingest workflow, if the answer
implies a schema change, note it in the log and do it on a branch. Plain markdown links only, so lint
leaves this file alone.
