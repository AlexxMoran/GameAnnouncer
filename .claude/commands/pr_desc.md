# PR Description Generator

Generate a comprehensive Pull Request description based on recent commits.

## Instructions

When this command is invoked:

1. **Analyze commits**: Run `git log origin/main..HEAD --oneline` and `git diff origin/main...HEAD --stat`
2. **Generate PR description** using the template below
3. **Language**: English
4. **Style**: Professional and concise

## Template Structure

```markdown
## What Changed & Why

[2-4 sentences explaining what was changed and the motivation behind it. Focus on business value and technical necessity.]

## Database Changes

- [ ] This PR includes migrations
- [ ] This PR modifies existing data
- [x] This PR has no changes in database

## Areas Affected

[List of main files, modules, or features affected by this PR:]
- [Module/Feature 1] (path/to/file.ext)
- [Module/Feature 2] (path/to/file.ext)
- [API endpoints / Components / Services affected]

## Test Plan

- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed
- [ ] [Specific test scenarios if applicable]

## Screenshots / Demo

[Include if there are UI changes - otherwise remove this section]

## Breaking Changes

⚠️ [List any breaking changes, or state "No breaking changes"]

## Deployment Notes

[Any special steps needed for deployment, environment variables, configuration changes - or remove if not applicable]

## Rollback Plan

[How to rollback if something goes wrong - or remove if standard rollback applies]
```

## Best Practices to Include

When generating the PR description, consider adding these sections if relevant:

- **Performance Impact**: Any performance improvements or concerns
- **Security Considerations**: Security-related changes or implications
- **Dependencies**: New dependencies added or updated (with versions)
- **Related Issues/Tickets**: Link to related issues, tickets, or documentation
- **Documentation**: Whether docs need to be updated
- **Backward Compatibility**: How this affects existing functionality

## Output Guidelines

- Be specific about what changed, not just "updated files"
- Explain WHY changes were made, not just WHAT
- Group related changes together
- Use checkboxes for actionable items
- Link to relevant files using markdown format: `[file.py](path/to/file.py)`
- Keep it scannable - use lists and short paragraphs
- Remove sections that don't apply (don't leave empty sections)
