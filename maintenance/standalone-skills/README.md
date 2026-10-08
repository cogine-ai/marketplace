# Standalone skill repairs — 2026-10-08

This record preserves the bounded repairs applied to existing standalone installations. It does not install another bundle or change invocation defaults.

`2026-10-08.patch` uses paths relative to the user home directory. Its companion JSON records the exact before/after SHA-256 of all 13 changed files. Check every target against its recorded before hash before applying the patch; if a target has changed, review the conflict rather than force the patch. Use `git apply --check` before application. Already-overlaid files must match the after hash and do not need another application.

- AI SEO: separate search, training and user-fetch controls; bound experimental claims; make machine-readable files conditional; preserve existing crawler path exclusions.
- Analytics and launch: remove references to eight absent tool/integration guides across the three marketing skills and use actual environment capabilities or existing bundled guides.
- Domain/setup/architecture: honor explicit glossary/context policy, preserve legacy layouts and terms, resolve the installed architecture dependency.
- CEO: align the two standalone entrypoints with the approved Founder/CEO adaptation. `ceo-source-2026-10-08.patch` applies the same scoped change inside the existing Cogine Dev source repository; other dirty work there is outside this record.

The installer `.skill-lock.json` remains unchanged. Its folder hashes are historical installer provenance, not claims that local overlays are byte-identical to upstream. Reconcile these exact repairs when updating those standalone skills later.

Existing third-party attribution applies: marketing source is MIT (`plugins/growth-and-gtm-skills/THIRD_PARTY_NOTICES.md`); Matt source is MIT (`plugins/coding-engineer-skills/THIRD_PARTY_NOTICES.md` and `LICENSES/MIT-Matt-Pocock.txt`); CEO is Cogine's existing attributed GStack-derived adaptation. Preserve those notices when redistributing.

These files are review and recovery material; they do not prove a running host selected a skill or that an external service changed.

The narrow `.gitattributes` rule recognizes whitespace in unified patch context markers. Payload integrity is checked by applying and reversing each patch, then comparing exact file hashes.
