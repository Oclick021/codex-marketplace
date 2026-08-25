---
name: commit-and-deploy
description: Prepare categorized Git commits and execute the repository's verified versioning and deployment procedure. Use when the user invokes CommitAndDeploy or explicitly asks to commit current changes as a project deployment or release.
---

# CommitAndDeploy

Commit the current changes and follow the project's established deployment procedure.

## Discover the deployment contract

Read applicable `AGENTS.md` files and inspect CI workflows, build and packaging scripts, version manifests, release configuration, and recent deployment commits. Identify:

- the authoritative version source and increment policy;
- all coupled version declarations that the project requires;
- the exact case-sensitive commit trigger marker;
- required build, test, package, changelog, signing, push, or publish steps;
- the branch and remote from which deployment is allowed.

If no reliable procedure can be established, report what was inspected and ask for the missing release convention. Do not guess a version bump, trigger marker, publication target, or deployment command.

## Commit and deploy

1. Inspect `git status` and all diffs. Exclude generated artifacts, secrets, customer data, and unrelated user changes.
2. Group changes by functional purpose. Follow the repository's message convention; otherwise use a suitable type such as `feat`, `fix`, `docs`, `refactor`, `build`, or `chore`.
3. Apply the project's version increment to its authoritative source and required coupled declarations. Do not update unrelated package or assembly versions.
4. Stage only the intended changes, review the staged diff, and run `git diff --cached --check` plus the deployment procedure's required validation.
5. Create the categorized commit with the project's deployment marker. If the project has no different case-sensitive convention, include `[Deploy]`, for example `feat: add export workflow [Deploy]`.
6. Verify the resulting commit and working tree before any external deployment action.
7. Push or publish only through the project's established non-force path. The `CommitAndDeploy` invocation authorizes the verified deployment procedure, but not unrelated releases, force-pushes, history rewriting, hook bypasses, or guessed external actions.
8. When deployment is asynchronous, report the trigger and available status evidence without claiming success before it completes.

Finish with the version change, commit hash and subject, validation results, pushed branch or publication target, and deployment status.
