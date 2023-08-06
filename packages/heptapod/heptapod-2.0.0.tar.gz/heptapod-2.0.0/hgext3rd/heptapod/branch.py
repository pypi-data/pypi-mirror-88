# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Heptapod specific branch facilities.

GitLab branches:

  GitLab branches are pointers to Mercurial changesets that the Rails
  application believes to be actual Git branches. They are updated
  automatically by each transaction, applying several rules tailored for
  good interaction with other GitLab components. They are not implemented
  as bookmarks because they are not meant to be exposed to Mercurial clients.

  GitLab branches are kept in a file that represents the last state that was
  exposed to other GitLab components (notably, the Rails application). In case
  there is an ongoing transaction, the file represents the state at the
  beginning of the transaction, and is updated at the end of transaction.
  Its uses include:

  - sending pre- and post-receive calls to the Rails application based on
    comparisons with the previous state.
  - fast querying by GitLab branch in HGitaly. While it is possible for HGitaly
    to implement the mapping to GitLab branches in a stateless way, it is very
    bad for performance to do it in all read operations.

  The state cannot be reconstructed, since it records what other components
  have already seen. But it can be reinitialized: GitLab will fail to update
  the Merge Requests that should have been affected by the current transaction,
  fail to create new Pipelines and generally miss all the consequences of
  the current transaction. Initializing it at import or in an otherwise
  empty transaction should not create any problem.

  File format: version preamble (common to all versions):

  - first 3 bytes: decimal string representation of the version number, padded
    with left zeros (spaces also accepted for reading)
  - byte 4: Unix End-Of-Line (LF, 0x10)

  File format: version 1 (after version preamble)

  - line-based, each line terminated the Unix way (LF, 0x10)
  - one GitLab branch per line
  - each line is made of the hexadecimal Mercurial changeset ID, followed by
    exactly one space character, then by the GitLab branch name (bytes with
    no encoding assumption). Example::

        01ca23fe01ca23fe01ca23fe01ca23fe01ca23fe branch/default

Default GitLab branch:
  This a GitLab branch, e.g., ``branch/default`` rather than a Mercurial
  branch, e.g., ``default``.

  It is stored inside the repository directory, but not in the main store.
  In principle, different shares could have different default GitLab branches,
  if that were to be useful.

  For comparison, GitLab uses the value of `HEAD` on Git repositories for
  this.
"""
from mercurial.i18n import _
from mercurial import (
    hg,
    error,
)

DEFAULT_GITLAB_BRANCH_FILE_NAME = b'default_gitlab_branch'
GITLAB_BRANCHES_FILE_NAME = b'gitlab.branches'
GITLAB_BRANCHES_FILE_CURRENT_VERSION = 1


def read_gitlab_branches_file_version(fobj):
    """Read the version and leave `fobj` at the start of actual data.
    """
    version_line = fobj.read(4)
    # TODO proper exception
    assert version_line.endswith(b'\n')
    return int(version_line)  # ignores left 0 padding, whitespace and EOL


def write_gitlab_branches_file_version(
        fobj,
        version=GITLAB_BRANCHES_FILE_CURRENT_VERSION):
    fobj.write(b"%03d\n" % version)


def read_gitlab_branches(repo):
    """Return the GitLab branches mapping, as a dict.
    """
    # TODO proper exception
    with repo.svfs(GITLAB_BRANCHES_FILE_NAME, mode=b'rb') as fobj:
        # TODO proper exception
        assert read_gitlab_branches_file_version(fobj) == 1
        return {branch.strip(): sha for sha, branch in
                (line.split(b' ', 1) for line in fobj)}


def write_gitlab_branches(repo, gl_branches):
    """Write the GitLab branches mapping atomically.
    """
    with repo.lock():
        with repo.svfs(GITLAB_BRANCHES_FILE_NAME,
                       mode=b'wb',
                       atomictemp=True,
                       checkambig=True) as fobj:
            write_gitlab_branches_file_version(fobj)
            for gl_branch, sha_hex in gl_branches.items():
                fobj.write(b"%s %s\n" % (sha_hex, gl_branch))
            # atomictempfile does not expose flush(), so there's no
            # point trying an fsync(). Mercurial does not seem to use
            # fsync() anyway.


def get_default_gitlab_branch(repo):
    """Return the default GitLab branch name, or ``None`` if not set."""
    branch = repo.vfs.tryread(DEFAULT_GITLAB_BRANCH_FILE_NAME)
    # (hg 5.4) tryread returns empty strings for missing files
    if not branch:
        return None
    return branch


def set_default_gitlab_branch(repo, target):
    if not target:
        raise error.Abort(_("The default GitLab branch cannot be an "
                            "empty string."))
    shared_from = hg.sharedreposource(repo)
    if shared_from is not None:
        repo = shared_from

    with repo.wlock():
        repo.vfs.write(DEFAULT_GITLAB_BRANCH_FILE_NAME, target)
