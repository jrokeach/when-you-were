# Privacy

This knowledge base will, over time, contain deeply personal content about minors: their legal names, birthdates, schools, medical history, friends' names, quotes, fears, mistakes, reflections on family losses. Treat it accordingly.

## The rule

**Most families should not host this KB in a public repository.** The scaffold is public (so you can download it). Your instance of it should not be.

## Recommended setups

Pick one. They are all fine.

### Private GitHub / GitLab / self-hosted git

- Create a **private** repository. Double-check the visibility setting — GitHub shows "Public" vs "Private" at the top of the repo page.
- Only invite collaborators you'd trust with your kid's diary, because that is effectively what this is.
- Enable 2FA on your account.
- Be mindful of CI integrations, GitHub Actions logs, and any bot that has read access.

### Local-only with encrypted backups

- Keep the repo on your machine(s). Don't push to a remote.
- Use Time Machine with FileVault, or an encrypted cloud backup (Arq, Backblaze with private key, iCloud on an encrypted device), or both.
- Trade-off: no easy cross-device sync, no history survival if your machine dies without a backup.

### Private self-hosted git (e.g. a home NAS, Gitea, Forgejo)

- Most control, most setup work.
- Ensure the server itself is not exposed to the public internet.

## What NOT to do

- **Do not push to a public GitHub repo.** Once it's indexed, assume it's permanently archived.
- Do not commit from a shared / work machine you don't control.
- Do not paste a populated `AGENTS.md` (Family details), `AGENTS.local.md`, photos, or wiki content into public issue trackers, pastebins, or support threads.
- Do not use this KB as a demo in blog posts or conference talks with real names intact.
- Do not enable public GitHub Pages or similar rendering on the repo.

## If you accidentally pushed to a public repo

1. Make the repo private immediately.
2. Assume the content has been scraped or cached. GitHub, search engines, and archive.org may retain copies.
3. Rewriting history (`git filter-repo`) does not undo the exposure — it only cleans your repo.
4. If the content is sensitive enough (e.g. school name + child's full name + medical info), consider a full reset: create a fresh private repo, copy your `wiki/` content across, delete the public one. GitHub support can assist with DMCA / takedown for cached search results in some cases.
5. For anything you wouldn't want a stranger to read in ten years, reconsider whether to keep it in the KB at all.

## What the scaffold does to help

- On first setup, the agent explicitly warns you about public repos and records your acknowledgment.
- Until you acknowledge, on every session the agent re-checks the git remote and warns if it looks public.
- Once you acknowledge, the warning can be dismissed permanently (the agent will offer to remove the directive from `AGENTS.md`).
- The `.gitignore` does not protect `AGENTS.md`, `AGENTS.local.md`, or anything under `wiki/` by default — because the entire repo is expected to be private. Don't treat `.gitignore` as a safety net here.

## Special considerations

- **Teen and pre-teen kids.** Think about what your kid, when they turn 13, 17, 23, would want strangers to know about them. Some of what's cute at 6 reads differently at 16.
- **Letting the kid see it.** Part of the point is giving them this back someday. Keep that audience in mind as you write.
- **Divorce, separation, custody.** If the KB is co-maintained by two parents, discuss upfront what happens to it if the relationship changes. Write that down.
- **Medical and developmental info.** Useful to capture, but be thoughtful about where it ends up and who has access.
- **Other kids (friends, cousins).** You'll end up writing about them incidentally. Consider whether you'd share this with their parents.

## TL;DR

Private repo. Or no repo. Not public.
