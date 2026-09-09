# Timed mocks

The textbook is complete, but this folder remains a **personal evidence layer**. A mock file should
exist only when I actually run that session; generated textbook content does not count as a mock.

Default format:

```text
90 minutes
3 problems
no AI
no category labels
no previous solutions
```

Copy [`TEMPLATE.md`](TEMPLATE.md) for a session.

The CLI can generate the same answer-hidden structure without creating any fake result:

```bash
python3 scripts/mock.py --duration 90 --problems 3
```

It writes session metadata only when the learner actually starts the command. After the timer, run
`python3 scripts/mock.py --review mocks/sessions/<session>.json` to record solved state, pattern
identification, time-to-identify, time-to-implement, wrong turns, and hint use.

Problem selection can come from `python3 scripts/practice.py --mixed 3 --seed <number>`. Keep the
answer key closed until the 90-minute block ends.
