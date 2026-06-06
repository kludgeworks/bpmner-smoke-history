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

# Fail closed against human manual runs: only the automation app (a [bot] actor) may dispatch.
# TODO: once the GitHub App exists, tighten this to the exact '<app-slug>[bot]'.
case "$actor" in
*'[bot]') ;;
*)
  echo "ingest may only be dispatched by the automation app, not '$actor'"
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
