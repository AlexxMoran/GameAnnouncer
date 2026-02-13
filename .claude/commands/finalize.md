---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(gh pr view:*), Bash(git switch -c:*)
description: Finalize changes made on the current branch by committing, pushing, and creating/updating a pull request.
---

## Context
- Current branch: !`git branch --show-current`
- Git status: !`git status --porcelain`
- All branches: !`git branch -a`
- Recent commits: !`git log --oneline -10`
- Changed files: !`git diff --name-status HEAD`
- Diff summary: !`git diff --stat HEAD`
- Existing PRs for this branch: !`gh pr view --json number,title,url || true`
- PR template: @.github/pull-request-template.md

## Your task

Guide the user through finalizing their work using selection options whenever possible:

### Step 1: Branch Check

If current branch is protected (dev, main, master, staging, release, production):
- Inform user they're on a shared branch
- Analyze recent commits and changed files
- Generate 3-5 descriptive branch names using conventional prefixes (feature/, fix/, refactor/, etc.)
- **Present as selection options**: the suggested names + "Enter custom name" option
- If user chooses custom name, then allow text input
- Check if chosen branch exists in branch list
- If exists, **present selection**: ["Delete and recreate branch", "Cancel and choose different name"]
- If user confirms deletion: run `git branch -D <name>` then `git checkout -b <name>`
- If branch doesn't exist: run `git checkout -b <name>`

### Step 2: Commit Changes

If there are uncommitted changes in git status:
- Analyze the diff to understand what changed
- Generate a clear, descriptive commit message following conventional commits format
- **CRITICAL**: Never mention AI, assistants, automation tools, or Claude Code in commit messages
- Write as if the developer wrote it themselves
- **Present as selection**: ["Commit with this message: '<message>'", "Edit commit message", "Skip commit"]
- If "Edit commit message" chosen, then allow text input for custom message
- If commit confirmed: run `git add -A` and `git commit -m "<message>"`
- Then **present selection**: ["Push to remote", "Skip push"]
- If push confirmed: run `git push -u origin <branch-name>`

### Step 3: Handle Pull Request

Check if PR already exists from the context:

**If PR exists**:
- Show the existing PR URL and title to user
- **Present selection**: ["Update PR description", "Keep PR as is", "View current PR"]
- If "View current PR" chosen: run `gh pr view <number> --json body -q .body` and show, then repeat the selection
- If "Update PR description" chosen:
    - Read current PR body with `gh pr view <number> --json body -q .body`
    - Generate updated description based on new commits and template
    - **CRITICAL**: Never mention AI assistance or automation in PR descriptions
    - **Present selection**: ["Update with this description", "Edit description", "Cancel"]
    - If "Edit description" chosen, allow text input
    - If update confirmed: run `gh pr edit <number> --body "<new-body>"`

**If no PR exists**:
- **Present selection**: ["Create PR", "Skip PR creation"]
- If "Create PR" chosen:
    - Generate PR title from branch name and commits
    - Generate PR body using template structure or standard format
    - **CRITICAL**: Never mention AI assistance or automation in PR content
    - **Present selection**: ["Create PR with generated content", "Edit title and description", "Cancel"]
    - If "Edit title and description" chosen, allow text input for both
    - If creation confirmed: run `gh pr create --title "<title>" --body "<body>"`
    - Show the new PR URL

## Guidelines

- **Always use selection options** instead of asking open-ended questions
- Only allow text input when user explicitly chooses "Edit" or "Custom" option
- Be conversational and explain what each option does
- All context commands run automatically without prompts
- If any command fails, explain the error and **present selection options** for next steps
- Keep all git history and PR content professional and human-written
- Never reference automated tools, AI, or Claude Code in any commits or PRs
- Use clear, action-oriented option labels like "Commit with this message" not "Yes/No"
