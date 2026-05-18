# Generate Announcement Bracket

Generates a single-elimination bracket for an announcement.

The HTTP route keeps authorization at the entrypoint. This operation owns the
business scenario: checking bracket preconditions, choosing eligible
participants, assigning seeds, creating matches, propagating BYEs, and moving
the announcement lifecycle forward.

## Invariants

- A bracket cannot be generated twice.
- Qualification brackets require finalized qualification.
- Direct brackets require `registration_closed` status.
- At least two eligible participants are required.
- Decisions operate on operation snapshots, not ORM models.

## Reads

- Announcement
- Announcement participants
- Existing matches

## Writes

- Participant seeds
- Match records
- Announcement bracket size
- Announcement lifecycle status

## Danger Zones

- `decisions.py`: tournament eligibility and seeding rules
- `gateway.py`: database writes and lifecycle transition
- `scenario.py`: orchestration order
