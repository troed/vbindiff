# VBinDiff for openSUSE — design

2026-11-01 · status: draft for approval

## Intent

openSUSE Tumbleweed has no vbindiff package (confirmed: Repology tracks
openSUSE Factory/Tumbleweed and lists no entry for `vbindiff`), and the
upstream project has not been touched since 2017: last commit
`7e05618` (2017-09-15), no tags, no GitHub releases, 17 open issues and
5 open PRs, and the issue asking whether the project is abandoned
(`#28`, Oct 2023) has never been answered.

We use vbindiff, we already built it locally from upstream master plus
PR #23 (the `panel.h` fix that openSUSE specifically needs), and we want
other people to be able to install it. The plan is therefore:

- publish an OBS home project that builds and serves packages for
  openSUSE users;
- keep the source in a public fork (`https://github.com/troed/vbindiff`)
  which carries the fixes, so every change is a commit someone else can
  read;
- cherry-pick fixes from other distributors and from upstream's open PRs
  over time.

We are not applying to become the openSUSE package maintainer, and we are
not taking over the project upstream.

## Goals

1. On a current openSUSE Tumbleweed system, the following works and
   yields a working `vbindiff`:

   ```sh
   zypper ar -f https://download.opensuse.org/repositories/home:/troed:/vbindiff/openSUSE_Tumbleweed/ vbindiff
   zypper in vbindiff
   ```

2. The fork is the single source of truth for the code; OBS fetches from
   it, nothing is hand-uploaded.
3. The package identifies as `3.0~beta5` (upstream's last released
   version), with our patch level carried by the OBS-managed release
   counter, so each cherry-pick batch ships as an update.
4. Fixes from other packagers can be imported as commits, one batch at a
   time, without ever inventing a new version number.

## Non-goals

- Submitting to openSUSE:Factory, or maintaining the package for
  openSUSE/SUSE as a distribution maintainer.
- Publishing releases of the software itself (no upstream takeover, no
  new upstream release numbers, no Windows binaries).
- Leap 15.6 (end-of-life), 32-bit x86, or non-openSUSE distributions.
- A patch stack in the spec file: any change to the code is a commit in
  the fork, not a `.patch` in the OBS package.

## Anti-goals

- Building an alternative distribution channel (Flatpak, AppImage,
  standalone tarballs) — OBS is the channel.
- Diverging from upstream in ways that make a future merge from
  `madsen/vbindiff` painful (keep our commits small and separate).
- Silent drift between the fork and what OBS actually built.

## Constraints

- Licence is GPL-2.0-or-later, but the repository contains **no
  `COPYING`** file. openSUSE requires the licence text to be shipped, so
  the fork must add one and the spec must use `%license`.
- Upstream ships no tags and no releases; the only released artefact is
  `vbindiff-3.0_beta5.tar.gz` on `cjmweb.net`. We build from git, so
  `configure` and `vbindiff.1` do not exist in the tree and must be
  generated during the build (autotools + Perl Template Toolkit).
- `GetOpt/` is a git submodule pointing at `madsen/free-getopt`. OBS
  source services and `git archive` skip submodule contents.
- The build has never been run with autoconf 2.73 / automake 1.17; the
  local working tree already carries autoupdate fixes for that
  (`configure.ac`, `config.h.in`).
- Toolchain available on Tumbleweed: gcc, ncurses with the panel library,
  autoconf/automake, Perl.

## Approaches considered (source delivery)

1. **OBS `_service` pulling from the fork** — chosen. The fork stays the
   source of truth; `_servicedata` records the exact commit; OBS
   regenerates the tarball server-side. Flow: cherry-pick → push →
   update the pinned revision → regenerate → commit.
2. **Cut a tarball locally and upload it into the OBS package** —
   simplest to reason about, but every update is a manual re-cut and the
   OBS copy can drift from the fork unnoticed.
3. **Publish a tarball as a GitHub release asset and point `Source0` at
   it** — human-friendly, but still hand-cut, and the build depends on
   that URL staying put.

Option 1 was chosen because drift between the fork and the built package
is the failure mode we care about most, and because a dead upstream means
we will be publishing patch batches regularly.

## Decisions already taken (from the design conversation)

- OBS home project, not Factory.
- Public fork at `https://github.com/troed/vbindiff`.
- Package version `3.0~beta5`; the patch counter is the OBS release
  number, not part of the version string. Never `beta6`.
- Fixes arrive as commits in the fork, cherry-picked from other
  packagers' patch sets and from upstream's open PRs.

## Design

### Fork layout

- `master` is a mirror of `madsen/vbindiff` master. Nothing is committed
  to it, so a future upstream commit merges cleanly.
- `opensuse` is the branch we build from. It starts at PR #23's commit
  `b8d4769` ("Handle 'panel.h' being in an 'ncurses' directory") and
  carries a small number of separate, individually reviewable commits:

  1. `configure.ac` / `config.h.in`: survive autoconf 2.73 and
     automake 1.17 (the autoupdate fixes already in the working tree).
  2. `AC_INIT` version back to `3.0_beta5`, so `vbindiff --version` and
     the generated man page agree with the package version.
  3. Vendor `GetOpt/` (drop `.gitmodules`, commit the three files), the
     way upstream's own release tarball contains them. One clone then
     builds without `git submodule` gymnastics.
  4. Add `COPYING` (GPL-2.0 text) for `%license`.
  5. `README.md`: a short "this fork" section — what it is, why, and the
     `zypper ar` line for openSUSE users.

- Nothing is tagged. `version` is fixed at `3.0~beta5`; the commit history
  is the patch log.
- History is **append-only**: `opensuse` is never rebased or force-pushed,
  because OBS pins full commit SHAs and a rewrite would make already-built
  revisions unfetchable. If upstream ever revives, `madsen/master` is
  merged into `opensuse`; it is not rebased onto it.
- The fork already exists (created 2026-11-01) and is byte-identical to
  upstream master. The local clone's `origin` still points at
  `madsen/vbindiff`; setup adds the fork as a remote (or repoints
  `origin`) and pushes `master`, `pr-23` and `opensuse`.

### OBS project

- Project `home:troed:vbindiff` (a subproject, so the repository URL reads
  `.../home:/troed:/vbindiff/<repo>/` and the package is not mixed with
  unrelated home-project packages). This assumes the OBS login is `troed`;
  if it differs, the project name, the repository URL and the `zypper ar`
  line in the fork's README change with it.
- Build repositories enabled:
  - `openSUSE_Tumbleweed` — x86_64
  - `16.0` (Leap 16) — x86_64
  - Slowroll: present but disabled initially.
- aarch64 is dropped for now: Tumbleweed's aarch64 packages come from
  `openSUSE:Factory:ARM`, not `openSUSE:Factory`, so it needs its own
  repository entry (and its own download path) rather than another
  `<arch>` on the same repository.
- No other architectures while the upstream code has no 64-bit-clean
  claims beyond what we test.

### Source service

- `_service` in the OBS package, a single `obs_scm` (or `tar_scm` if the
  former's version handling fights us) with:
  - `scm: git`
  - `url: https://github.com/troed/vbindiff`
  - `revision: <full SHA of the opensuse branch head>` — pinned, never a
    branch name, so builds are reproducible
  - `version: 3.0~beta5`
  - `submodules: false` (GetOpt is vendored)
- Output tarball `vbindiff-3.0~beta5.tar.gz`, plus the generated
  `_servicedata` committed next to it.
- The `~` in the version is expected to survive into the filename; if the
  service mangles it, fall back to generating `vbindiff-3.0.beta5.tar.gz`
  and naming `Source0` to match. Implementation detail, not a design
  change.
- **Current state:** server-side service runs on OBS answer `200 OK` but
  produce no files and no `_servicedata`, with no other mode
  (`manual`, `disabled`) making a difference. Until that is understood,
  the OBS package carries a tarball generated with `git archive` from the
  pinned commit; `_service` stays in the fork so the approach can be
  retried without redesign.

### Spec file

Single binary package, no subpackages.

- `Name: vbindiff`, `Version: 3.0~beta5`, `Release: 0` (OBS assigns the
  real number), `License: GPL-2.0-or-later`, `URL:` upstream homepage,
  `Source0: %{name}-%{version}.tar.gz`.
- `BuildRequires: gcc-c++ ncurses-devel autoconf automake make
  perl-Template-Toolkit perl-TimeDate` (the last two generate
  `vbindiff.1`; `Date::Format` comes from perl-TimeDate).
- `%prep`: `%autosetup -n %{name}-%{version}`.
- `%build`: `autoreconf -fi` then `%configure` then `%make_build`.
- `%install`: `%make_install` (Makefile.am installs the binary and the
  generated man page).
- `%files`: `%license COPYING`, `%doc README.md AUTHORS`,
  `%{_bindir}/vbindiff`, `%{_mandir}/man1/vbindiff.1%{?ext_man}`.
- `%changelog` entry describing the openSUSE package, with the upstream
  state noted (beta5, patches in fork).

The spec carries **no patches**: the `panel.h` fix and every later fix
live in the fork.

### Execution boundary

This workstation's sandbox has **no network egress** (GitHub and OBS do not
resolve) and neither `osc` nor `gh` is installed; `git`, `rpmbuild`, `gcc`,
autotools and `pod2man` are available.

So the build delivers, locally and verifiably:

- the five commits on `opensuse`;
- `vbindiff.spec` and `_service` as files;
- a `rpmbuild` run against a tarball produced locally with `git archive`
  (valid because `GetOpt/` is vendored), with the resulting RPM inspected
  and smoke-tested;
- a runbook for the parts that need a human: add the fork remote and push,
  create `home:troed:vbindiff`, upload the spec and service, regenerate,
  commit, watch builds, and run the `zypper ar` acceptance test.

If egress or credentials are made available later, those runbook steps
become executable tasks; the design does not depend on that.

### Verification

GitHub Actions runs on every push (`.github/workflows/build.yml`), in
`opensuse/tumbleweed` and `opensuse/leap:16.0` containers: build the tree,
check the version strings, build and lint the RPM from the spec, install it
and check the packaged files. That is the per-commit gate; OBS builds the
same spec for the published repositories.

Before announcing the repository:

1. OBS builds succeed for every enabled repository and architecture.
2. `rpmlint` output clean (or every remaining warning explained).
3. Smoke test of the built binary: `vbindiff -L` exits 0, and a
   two-file comparison of two small known-different files renders
   without crashing.
4. On the workstation: `zypper ar` the repository, install, run
   `vbindiff --version` (expect `3.0_beta5`) and an interactive
   comparison.
5. `rpm -qp --license`, `rpm -qlp` inspected: binary, man page, licence,
   docs present, nothing stray.

### Maintenance loop

- Cherry-pick sources, in priority order: upstream open PRs (#23 already
  in; #10 SIGINT handling; #12 CMake — probably not wanted; #33
  colours/side-by-side, needs review), then Debian's patch queue
  (9 patches, unforwarded; needs a local `dget`/git clone because the
  Debian services block this sandbox), then anything from Fedora (still
  on beta4, so unlikely).
- Each batch: commit in the fork → update `revision` in `_service` →
  regenerate → `osc commit` → check OBS builds → smoke test.
- OBS build-failure notifications are enabled; a Tumbleweed snapshot that
  breaks the build is our problem to fix.

## Calls made here (adjustable)

- OBS project named `home:troed:vbindiff` (subproject rather than the
  bare home project).
- Leap 16.0 enabled, Leap 15.6 skipped (EOL), Slowroll present but off.
- aarch64 enabled alongside x86_64.
- Packaging files live in the OBS package only; the fork holds source
  and docs (including this design), not the spec.
- GetOpt vendored rather than tracked as a submodule.
- `opensuse` history is append-only (no rebase, no force-push) because OBS
  pins SHAs; upstream, if it revives, is merged in.
- The implementation stops at local `rpmbuild` + runbook, since this
  sandbox has no network or `osc`; pushing and OBS work is the human's
  step.
- The OBS login is assumed to be `troed` (matching GitHub); confirm at
  first login.

## Risks

- Perl-generated man page is the most fragile part of the build; if
  perl-TimeDate/Template-Toolkit churn breaks it, the fallback is to ship
  the man page generated once and committed, and drop the Perl
  BuildRequires.
- OBS service runs depend on GitHub being reachable; a pinned SHA plus
  the stored tarball in the package mitigates it (OBS keeps generated
  files once committed).
- Upstream could revive; if it does, our `opensuse` branch rebases onto
  the new master and most commits drop away.
- Nobody else watches this package: if we stop, it rots. That is the
  accepted cost of a `home:` project.
