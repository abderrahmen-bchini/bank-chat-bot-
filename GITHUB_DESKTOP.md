# GitHub Desktop Workflow

This guide explains how we use GitHub Desktop for branch management and pull requests.

## Why GitHub Desktop?

- Visual interface (no terminal needed)
- Easy branch creation and switching
- Simple push/pull operations
- Clear visualization of file changes
- Integrated PR workflow
- Perfect for team collaboration

## Installation

Download GitHub Desktop: https://desktop.github.com/

## Initial Setup

1. Open GitHub Desktop
2. Click **File** → **Clone Repository**
3. Select `abderrahmen-bchini/bank-chat-bot-`
4. Choose local path
5. Click **Clone**

GitHub Desktop now shows the repository with `develop` as the default branch.

## Daily Workflow

### Starting New Work

1. **Update develop branch**
   - Click **Current Branch** tab
   - Select `develop`
   - Click **Fetch origin** button
   - Click **Pull origin** button

2. **Create feature branch**
   - Click **New Branch** button
   - Name: `feature/US-04-pdf-upload`
   - Base branch: `develop`
   - Click **Create Branch**
   - Click **Publish branch**

### Making Changes

1. **Edit files in your editor**
   - Open VS Code or your IDE
   - Make code changes
   - Save files

2. **Commit changes in GitHub Desktop**
   - GitHub Desktop shows modified files automatically
   - Review changes in the **Changes** tab
   - Enter commit message: `feat(ingestion): add PDF extraction`
   - (Optional) Add description
   - Click **Commit to feature/US-04-...**

3. **Push to remote**
   - Click **Push origin** button
   - Your branch is now on GitHub

### Multiple Commits

For multiple commits on one feature:

1. Make changes to files
2. Enter commit message
3. Click **Commit**
4. Make more changes
5. Enter new commit message
6. Click **Commit** again
7. Click **Push origin** to push all commits at once

## Creating a Pull Request

### After First Push

1. In GitHub Desktop, after pushing, you'll see a **Create Pull Request** button
2. Click it
3. GitHub opens in your browser
4. PR title auto-fills: `feature/US-04-pdf-upload`
5. Update title to: `[US-04] Add PDF file upload`
6. Add description:
   ```
   Closes #123

   Changes:
   - Add file upload endpoint
   - Validate file type and size
   - Store files securely
   ```
7. Click **Request a reviewer** → Select team member
8. Click **Create Pull Request**

### On GitHub Website

1. Click **Reviewers** and select team member
2. Team member reviews code
3. Team member approves or requests changes
4. Click **Squash and merge** (when approved)

## Code Review Process

### As an Author

1. **Wait for review** — GitHub sends notifications when comments are added
2. **Address feedback** — Make requested changes locally
3. **Commit and push** — New commits appear on the PR automatically
4. **Respond to comments** — Click Reply on GitHub comments
5. **Re-request review** — Click the refresh icon next to reviewer name
6. **Merge when approved** — Team merges via "Squash and merge"

### As a Reviewer

1. **Click PR link** — Opens on GitHub
2. **Review code** — Click **Files changed** tab
3. **Add comments** — Click line number to comment
4. **Approve or request changes** — Click **Review changes** button
5. **Submit review** — Select "Approve" or "Request changes"

## Switching Branches

1. Click **Current Branch** tab
2. See list of all branches
3. Click branch name to switch
4. GitHub Desktop updates files automatically

## Updating Your Branch

If `develop` has new commits and you need to update your feature branch:

1. Click **Current Branch** → Select `develop`
2. Click **Fetch origin** → **Pull origin**
3. Click **Current Branch** → Select your feature branch
4. Click **Branch** menu → **Update from develop**
5. (If conflicts exist, resolve them and commit)

## Viewing Changes

### Before Committing

- **Changes tab** — Shows all modified files
- Click file name to see line-by-line changes
- Red = removed, Green = added

### After Committing

- **History tab** — Shows all commits
- Click commit to see what changed
- Shows before/after for each file

## Syncing Multiple Computers

If working on different machines:

1. On new computer: Clone the repository (see Initial Setup)
2. **Fetch origin** regularly to get latest changes
3. **Pull origin** before starting new work
4. Create branches on each machine as needed
5. GitHub Desktop syncs everything automatically

## Merge Conflicts

If your branch conflicts with develop:

1. GitHub Desktop notifies you
2. Click **Merge develop into feature/US-XX**
3. Review conflicting files
4. Edit files to resolve conflicts
5. Mark as resolved in GitHub Desktop
6. Commit the merge
7. Push to origin

## Useful Buttons & Shortcuts

| Action | How |
|--------|-----|
| Create branch | New Branch button |
| Switch branch | Current Branch → Select branch |
| Fetch updates | Fetch origin button |
| Pull updates | Pull origin button |
| Push commits | Push origin button |
| View history | History tab |
| See changes | Changes tab |
| Open in editor | Right-click file → Open in VS Code |

## Common Issues

### Branch doesn't show on GitHub

- Click **Publish branch** button (if visible)
- Or go to GitHub website and verify

### Changes not appearing after pull

- Click **Pull origin** again
- Refresh your editor/IDE

### Can't merge — conflicts exist

- Update branch from develop (see "Updating Your Branch")
- Resolve conflicts manually
- Commit and push

### Wrong branch pushed to

- Don't panic! Create new PR from correct branch
- Close incorrect PR
- Delete incorrect branch locally and on GitHub

## Next Steps

1. Clone repository with GitHub Desktop
2. Create feature branch for US-04
3. Make your first commit
4. Push to origin
5. Create PR on GitHub
6. Request review from team member

---

**Questions?** Check [CONTRIBUTING.md](CONTRIBUTING.md) or ask your team lead.
