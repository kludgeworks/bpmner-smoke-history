#!/usr/bin/env bash
#
# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
#
#MISE description="Validate an ingest dispatch (untrusted inputs) before any work."
#USAGE flag "--ref <ref>" env="REF" help="git ref the dispatch ran on (must be main)"
#USAGE flag "--actor <actor>" env="ACTOR" help="dispatching actor (must be a [bot])"
#USAGE flag "--run-id <run_id>" env="RID" help="bpmner Actions run id (numeric)"
set -euo pipefail

ref="${usage_ref:?}"
actor="${usage_actor:?}"
run_id="${usage_run_id:?}"

[ "$ref" = "main" ] || {
  echo "ingest must run on main, got '$ref'"
  exit 1
}

# Fail closed: only the bpmner-smoke-history-bot App may dispatch (humans + other bots rejected).
case "$actor" in
'bpmner-smoke-history-bot[bot]') ;;
*)
  echo "ingest may only be dispatched by bpmner-smoke-history-bot, not '$actor'"
  exit 1
  ;;
esac

case "$run_id" in
'' | *[!0-9]*)
  echo "run_id must be numeric, got '$run_id'"
  exit 1
  ;;
esac

echo "dispatch by $actor for bpmner run $run_id — ok"
