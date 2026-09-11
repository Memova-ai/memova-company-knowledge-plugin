---
name: company-knowledge-capture
description: Check for a durable company-knowledge candidate when the current Codex task has genuinely completed a substantial outcome, or when reviewing a locally queued ended task. Use for completed decisions, verified delivery, resolved incidents, finalized documents or meetings, and reusable methods; skip ordinary questions, brainstorming, intermediate work, failures still under investigation, and duplicate or sensitive material.
---

# Company Knowledge Completion Capture

Run a semantic knowledge checkpoint after the employee's primary task is genuinely complete. This
is a P1 complement to central SharePoint source synchronization: it captures new conclusions
created inside Codex, never crawls SharePoint and never uploads a conversation transcript.

Before acting, read
`../company-knowledge-submit/references/submission-workflow-contract.json`,
`../company-knowledge-submit/references/trigger-routing-v1.json`, and
`../company-knowledge-submit/references/receipt-candidate-v1.schema.json`. For current-task
`business_status` or `general_knowledge`, also read the corresponding current-task selection
schema. The dedicated Company MCP remains authoritative for identity, capabilities, validation,
idempotency, policy, publication, audit, provenance and index visibility.

## Semantic trigger

Assess at most once when the task has produced one or more of these durable outcomes:

- an approved product, architecture, policy or business decision;
- a code change whose exact revision and focused validation are complete;
- a production or staging deployment with immutable version and health evidence;
- a resolved incident with confirmed cause, repair and verification;
- a finalized document, meeting conclusion, operating procedure or reusable method;
- a materially changed, evidence-backed project or business status.

Do not activate merely because a turn stopped, a session exists, a commit was created, a tool ran,
or the assistant used words such as “done” or “completed”. Skip ordinary company questions,
summaries without a new fact, brainstorming, unapproved proposals, unfinished work, failed or
inconclusive investigations, routine edits, duplicates, personal notes and content outside the
company-public-internal distribution scope.

## Quiet assessment and duplicate check

1. Finish and verify the employee's primary task before doing this checkpoint. Never delay an
   unfinished task to capture knowledge.
2. Use only the smallest stable conclusion and bounded supporting evidence from the current task.
   Never select the whole transcript, repository, diff, directory, raw log, private message,
   credentials, tokens, cookies, MFA data, secrets or unrelated workspace context.
3. Prefer one highest-value candidate. Use more than one only when distinct receipt types are
   essential, and process them sequentially.
4. Search the Company MCP for the same business object, outcome and evidence revision. A matching
   current record with no substantive change is `NO_SUBMIT`. A conflicting or superseded record
   must use the correction workflow; never overwrite or conceal it.
5. Apply the trigger catalog, receipt routing, evidence and sensitivity gates from the submission
   Skill. If evidence is incomplete, restricted or unsafe to summarize, do not prepare a preview.
6. If the result is `NO_SUBMIT`, finish the original task without adding a knowledge-capture prompt
   or status paragraph. The checkpoint should normally be invisible.

## Automatic preview, one employee confirmation

This Plugin distribution has organization-level opt-in to automatically prepare an ephemeral
preview after a qualifying task outcome. That opt-in authorizes only one prepare call for the exact
candidate selected by this checkpoint. It never authorizes durable publication.

- For current-task `business_status` or `general_knowledge`, use the bounded server-owned route and
  never invent a source URL, revision, evidence hash or owner.
- For other receipt types, prepare only when the current task contains every contract-required,
  immutable evidence field. Otherwise stop at `NEED_MORE_EVIDENCE` without asking the employee to
  manufacture evidence.
- Call `prepare_knowledge_submission` once. Do not retry automatically or replace the candidate if
  validation, authentication, policy or dependency checks fail.
- Display the complete server preview, exclusions, limitations, receipt type, owner, snapshot,
  preview ID, hash and expiry. State clearly that nothing has been published yet.
- Ask for one concise final confirmation to publish that exact preview. Silence, a later unrelated
  message, a different preview or organization-level capture opt-in is not confirmation.
- Only after that confirmation call `submit_knowledge_candidate` exactly once with the fields
  allowed by the frozen submission contract. Verify the bounded publication status and report
  Published Knowledge, SubmissionReceipt, citation and search visibility.

If the employee declines or does not answer, allow the preview to expire. Never publish in a Hook,
on `SessionEnd`, in a scheduled catch-up, or merely because a task was successful.

## Ended-session fallback

The Plugin's `SessionEnd` Hook records only a private local pointer to an ended main task. It does
not send transcript content or credentials anywhere and cannot call the Company MCP. If a later
task explicitly reviews that local queue, inspect at most one ended task at a time, apply the same
semantic and evidence gates, and default to `NO_SUBMIT`. Never batch-upload transcripts or infer
that every ended session contains company knowledge.
