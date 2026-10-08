---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Invoke `coding-engineer-skills:tdd` through the available skill invocation mechanism where possible, at pre-agreed seams. Do not reopen seam choices already approved for this work.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, review the work against the originating spec or tickets and the
repository's documented standards before committing.

Commit your work to the current branch.
