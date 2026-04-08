# GitHub Private Remote Setup

## Goal
Connect `D:\产品设计\New folder` to your own private GitHub repository without changing the source-of-truth rule.

## What Codex Can Prepare
- local Git repository
- hooks and commit template
- local commits and branches
- remote add or remote URL update once you provide the repository URL

## What You Must Do
- create the private repository in your own GitHub account
- decide whether to use HTTPS or SSH
- complete GitHub authentication on your machine

## Recommended Sequence
1. Create an empty private repository on GitHub.
2. Copy the repository URL.
3. Run:

```powershell
py -3 scripts\setup_github_remote.py --url <YOUR_REPO_URL>
```

4. Verify:

```powershell
git remote -v
```

5. Push the current branch:

```powershell
git push -u origin main
```

## Recommended URL Choice
- use SSH if your machine already has GitHub SSH keys configured
- use HTTPS if you prefer Git Credential Manager or browser sign-in

## Safety Rule
Do not push from any directory other than `D:\产品设计\New folder`.
