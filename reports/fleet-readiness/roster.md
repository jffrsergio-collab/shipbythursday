# Ship-by-Thursday — fleet readiness evidence

Snapshot captured: 2026-09-17T03:42:42.906062+00:00. Filesystem inspection only; not runtime certification.

## Gates

1. Configuration parsed → 2. Authentication verified → 3. Tools verified → 4. Role-specific pilot passed → 5. Explicit unattended approval.

The inventory establishes only configuration parsing and file presence. Gates 2–5 are NOT CHECKED here. Earlier runtime tests may exist; this audit neither erases them nor certifies them after an update. Shared/root authentication was not inspected. Missing profile auth.json does not imply missing usable credentials.

| Profile | Provider | Model | Effort pin | Stored jobs | Explicitly enabled | Local auth file | Evidence stage |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| engineer-bot-repl | nous | upstage/solar-pro4:free | medium | 1 | 1 | absent | configuration parsed; runtime not checked |
| ship-creative-director | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-data-dan | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-drop | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-eggbot | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-email-ethan | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-grokbot | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-hashbrown | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-host-finder | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-kb-manager | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-manager | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-marky | nous | upstage/solar-pro4:free | medium | 0 | 0 | present | configuration parsed; runtime not checked |
| ship-operator-research | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-ops-bot | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-pixel | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-prioritizer | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-prospecting-bot | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-slide-sonia | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |
| ship-steve | nous | upstage/solar-pro4:free | medium | 0 | 0 | absent | configuration parsed; runtime not checked |

## Interpretation and remaining checks

- One stored job with enabled=true is observed in engineer-bot-repl. This is not proof of a healthy scheduler, successful execution, or delivered output. Its fleet-watcher.yaml is listed separately; that YAML is not registration evidence and has not been deleted.
- All 19 profiles have SOUL.md and memories.md. File presence is not proof those instructions are loaded.
- Host Finder retains Nous / upstage/solar-pro4:free / medium and Tavily for search and extraction. Its last attempted Solar pilot was blocked by startup/authentication; not a model-quality verdict.
- Ride: 200 guests are within 400 published banquet seats; event-specific layout, pricing and availability remain unconfirmed. Pearl: disputed rates remain UNVERIFIED without applicable evidence.
- No model, credential, approval policy or schedule was changed by this inventory. No new routine is registered for the inventory itself.
- Inventory omits secrets, raw job prompts and auth contents. It is not a transcript-review agent or an automatic fleet repair system. Review report metadata before public sharing.

## Historical role sources — carried forward, not reverified

| Profile | Prior roster source |
| --- | --- |
| engineer-bot-repl | tape [02:25:28] + marketplace engineer-bot |
| ship-creative-director | tape [02:37:13] |
| ship-data-dan | tape [00:30:25-01:12:19] |
| ship-drop | tape [07:15:05] |
| ship-eggbot | tape [01:59:05] + marketplace dr-eggbot |
| ship-email-ethan | tape [00:30:25-01:12:19] |
| ship-grokbot | Not recorded in prior roster; role provenance pending |
| ship-hashbrown | tape [03:50:25] |
| ship-host-finder | tape [05:33:26] |
| ship-kb-manager | tape [05:17:37] |
| ship-manager | tape [01:12:19] |
| ship-marky | tape [01:36:21] |
| ship-operator-research | tape [03:10:08] |
| ship-ops-bot | tape [02:37:13] |
| ship-pixel | tape [02:46:03] |
| ship-prioritizer | tape [02:10:30] |
| ship-prospecting-bot | tape [01:58:31, 03:10:08] |
| ship-slide-sonia | tape [00:30:25-01:12:19] |
| ship-steve | tape [02:01:04] |

## Proposed handoffs — runtime wiring not tested here

- ship-hashbrown reviews engineer-bot-repl and ship-eggbot outputs.
- ship-ops-bot coordinates ownership and handoffs.
- Keep one accountable owner, evidence location, reviewer, and approval boundary per task.
