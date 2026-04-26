# Storage architecture

Where the bytes live.

This scaffold is **Git-only by default**. Text, frontmatter, and small images commit directly. For families who accumulate heavy binaries (video, long audio, high-res scans, large PDF corpora), Git alone doesn't scale — so the scaffold also supports a **hybrid** mode where binaries live in a cloud bucket and Git holds references.

The scaffold ships **no cloud tooling** — no upload helpers, no resolver libraries, no migration scripts. This document is guidance plus a filesystem convention (`.manifest.yml` stubs) and a public schema (`schema/raw-manifest.schema.json`). Actual tooling is out of scope today; families or host applications add their own.

---

## TL;DR decision tree

- **Small text + occasional photos, private repo, single-family use** → **Git-only**. Default, zero config. Just commit.
- **Heavy binaries** (hundreds of photos per year, long video, high-res scans, audio, large PDFs) → **Hybrid**. Text and frontmatter in Git; binaries in a cloud bucket; `sources:` references resolve via `.manifest.yml` stubs.
- **Never-Git tier** (medical imaging, entire video corpora, anything where even a manifest stub feels like too much exposure) → **Cloud-primary**. `raw/` holds only `.manifest.yml` stubs pointing at cloud object keys; pages still commit normally.

Most families are somewhere between the first two. Start Git-only; migrate specific categories to hybrid if repo size becomes a problem.

---

## The manifest convention

Each file under `raw/<category>/<YYYY-MM>/<name>.*` may be either:

**(A) the actual binary** — committed to Git. Works transparently; `sources:` entries in page frontmatter point at the file path.

**(B) a `<name>.manifest.yml` sibling** — a small YAML stub committed to Git, describing a binary that lives in a cloud bucket. Example:

```yaml
# raw/photos/2025-03/ava-birthday-cake.manifest.yml
storage: cloud
provider: s3                  # or gcs | b2 | custom
bucket: my-family-kb-raw
key: photos/2025-03/ava-birthday-cake.jpg
sha256: 8f3c…                 # integrity check
bytes: 4823104
media_type: image/jpeg
captured_at: 2025-03-14
notes: ""                     # optional
```

The **manifest** is what Git sees. The **binary** is in the bucket. Pages reference the raw source via `sources:` frontmatter as usual; agents (or humans) resolving a reference follow the manifest when the path ends in `.manifest.yml`.

The machine-readable schema for this stub is [`schema/raw-manifest.schema.json`](schema/raw-manifest.schema.json). Host applications may add provider-specific metadata as extra fields, but they should preserve the required keys so exports remain portable.

### Rules

- The manifest ends in `.manifest.yml` and sits where the binary would otherwise live.
- `sha256:` is required — it's how a resolver verifies the fetched binary matches what was committed.
- `bucket:` and `key:` together must uniquely identify the object.
- If the binary is later re-uploaded, update `sha256:`, `bytes:`, and (if changed) `key:` in the same commit.

---

## Provider choice is yours

The scaffold is cloud-agnostic. Any object store works. Typical picks:

- **Amazon S3** — ubiquitous, well-documented, pricey at scale.
- **Google Cloud Storage (GCS)** — similar to S3, integrates with Workspace.
- **Backblaze B2** — cheapest for family archives (often <$0.01/GB/month), S3-compatible API.
- **Cloudflare R2** — no egress fees; good when you actually read the archive back often.
- **Self-hosted MinIO** — if you run a home server and want zero vendor dependency.

### Access control (important)

- **Private bucket + signed URLs** for any access. Never public objects for family content.
- IAM / service-account scoped to the specific bucket — the credentials on your machine should not be able to reach any other storage.
- Encryption at rest (S3 default; GCS default; B2 default). Consider client-side encryption for medical or otherwise sensitive material.

---

## Self-hosted vs. platform-managed

**Self-hosted** (what this scaffold supports): you own the bucket, you manage credentials, you pay the bill. The scaffold describes the manifest convention and leaves you to wire up upload and resolution.

**Platform-managed**: a separate product layer (if you're using one) may provide managed storage as part of its setup. That's out of scope for the open-source scaffold — consult your host application's docs.

---

## Thresholds (guidance, not enforcement)

The scaffold doesn't block anything; these are rules of thumb for when Git starts feeling uncomfortable:

- **> 100 MB for a single file** — GitHub's soft warning threshold. Consider moving to cloud.
- **> 1 GB total `raw/`** — Git clone and blob storage start degrading. Definitely move the bulk to cloud; keep only thumbnails or representative samples in Git.
- **> 10 GB total `raw/`** — Git is the wrong tool. Cloud-primary for `raw/`; Git for text only.

### Git-LFS as a middle option

Git-LFS (Large File Storage) is a third way: binaries tracked through `.gitattributes` are stored separately by the forge (GitHub/GitLab/Gitea) and swapped in on checkout. Trade-offs:

- **+** Binaries stay in the Git workflow — no separate upload step.
- **+** Integrity checks and history come for free.
- **−** LFS has its own quotas and bandwidth costs on most forges.
- **−** Self-hosted Gitea LFS requires setup.
- **−** Doesn't help if the binary is genuinely too sensitive for the forge to hold.

LFS is fine for the middle zone (10 MB–1 GB files, modest volume). Beyond that, cloud-bucket-with-manifest wins on cost and isolation. The scaffold doesn't ship a `.gitattributes` config for LFS; set it up yourself if you want it.

---

## Migrating from Git-only to hybrid

If you started Git-only and a specific category is getting heavy:

1. Pick the category (e.g. `raw/video/`).
2. Upload each binary to your bucket.
3. Replace each binary in `raw/` with a sibling `.manifest.yml` describing it.
4. Commit the swap.
5. To purge the binary from Git history, use `git filter-repo` or `bfg-repo-cleaner`. Note: this rewrites history — coordinate with any other checkouts.

This is a one-time-per-category operation and doesn't need to be reversible.

---

## What this doc does NOT cover

- **Upload tooling** — no `scripts/upload-raw` in this scaffold. Use `aws s3 cp`, `gcloud storage cp`, `rclone`, or a host-application helper.
- **Resolver libraries** — no agent-side `.manifest.yml` follower ships today. Agents resolve manually (fetch the object, check the SHA). A host application may provide this.
- **Automated migration** between Git-only and hybrid — manual, per above.
- **Platform-managed storage tiers** — product-side, not in this scaffold.

When any of these becomes the right thing to build, it will likely live in a host application rather than the open-source scaffold, so the scaffold stays portable and dependency-free.
