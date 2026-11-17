# Functions SSE adapter correction

Tool candidate: `ddfab5d13bd01a1f244a4446cd10764c9091f65a`.
Reviewed skill content: `e5c0dabd3ecee8ea758ec2775d94d7cc4ee56e7d`.

BUG-043 affected the CLI adapter. SDK 1.101 returns an async SSE context manager;
the CLI treated it as bytes and failed before opening the HTTP stream. Existing
REST-085 SDK SSE evidence remains valid and covers a different layer.

The adapter now consumes typed SSE within the retry and client scopes. It buffers
each event's JSON payload and writes NDJSON once after successful completion.
Failed attempts discard partial output. Attempt counts and legacy bytes support
remain unchanged. Typed execution-error records remain visible in the output;
callers must inspect them even when the command exits successfully.

- [Independent QA](independent-qa.json) reproduces the original failure and verifies
  real SDK SSE decoding, retry, timeout, cancellation, cleanup, framing and UTF-8.
  Tests passed: 103 on SDK 1.101 and 46 on SDK 1.111.
- [Initial findings](initial-findings.json) preserve the original code and page
  defects. [Page retest](page-retest.json) accepts all six corrected pages and
  seven examples at their recorded hashes.
- [GitHub CI](github-ci.json) records all eight successful checks at the exact
  tool head, including four Windows/Linux and Python 3.11/3.12 test jobs.
- [Tracker closure](bug-closure.json) records independent QA approval, BUG-043
  Closed with resolution Done, and removal of only its verified blocking link.

All requests used synthetic inputs and mocked transport. No live tenant execution,
package upload or feature release approval is claimed. Earlier six-install package
evidence remains tied to `657215f`; these reports do not claim those packages were
rebuilt for this candidate.
