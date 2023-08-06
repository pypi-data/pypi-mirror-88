# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import time
from mercurial import (
    pycompat,
)
from hgext3rd.heptapod.branch import set_default_gitlab_branch

from hgitaly.tests.common import (
    make_empty_repo,
    make_tree_shaped_repo,
)

from hgitaly.stub.commit_pb2 import (
    CommitIsAncestorRequest,
    CommitsBetweenRequest,
    FindCommitRequest,
    FindCommitsRequest,
    CountCommitsRequest,
    CountDivergingCommitsRequest,
    LastCommitForPathRequest,
    ListCommitsByOidRequest,
    ListCommitsByRefNameRequest,
)
from hgitaly.stub.commit_pb2_grpc import CommitServiceStub


def test_is_ancestor(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    _, grpc_repo, changesets = make_tree_shaped_repo(server_repos_root)

    def hex_is_ancestor(hex1, hex2):
        resp = grpc_stub.CommitIsAncestor(
            CommitIsAncestorRequest(repository=grpc_repo,
                                    ancestor_id=hex1,
                                    child_id=hex2,
                                    ))
        return resp.value

    def is_ancestor(key1, key2):
        return hex_is_ancestor(changesets[key1].hex(), changesets[key2].hex())

    assert is_ancestor('base', 'top1')
    assert not is_ancestor('other_base', 'default')
    assert is_ancestor('default', 'default')
    assert is_ancestor('other_base', 'wild2')

    base_hex = changesets['base'].hex()
    # id in message *has* logically to be 40 chars
    # technically, on current Mercurial if short_id is str, repo[short_id]
    # does not work but repo[full_id] does.
    unknown_hex = '1234dead' * 5

    assert hex_is_ancestor(base_hex, unknown_hex) is False
    assert hex_is_ancestor(unknown_hex, base_hex) is False


def test_is_ancestor_obsolete(grpc_channel, server_repos_root):
    # still works if one of the changesets becomes obsolete
    grpc_stub = CommitServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    ctx1 = wrapper.write_commit('foo')
    ctx2 = wrapper.write_commit('foo2')

    # TODO prune arg treatment is a pain, add it in testhelpers
    wrapper.command('amend', message=b'amended')
    assert grpc_stub.CommitIsAncestor(
        CommitIsAncestorRequest(repository=grpc_repo,
                                ancestor_id=ctx1.hex(),
                                child_id=ctx2.hex(),
                                ))


# TODO test with tags. In particular they have precedence in Mercurial
# over branches
def test_find_commit(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    now = time.time()
    ctx = wrapper.write_commit('foo',
                               utc_timestamp=now,
                               user="HGitaly Test <hgitaly@heptapod.test>")
    ctx2 = wrapper.write_commit('foo',
                                parent=ctx,
                                message="Foo deux\n\nA very interesting bar")

    request = FindCommitRequest(repository=grpc_repo, revision=ctx.hex())
    response = grpc_stub.FindCommit(request)

    commit = response.commit
    assert commit is not None
    assert commit.id == ctx.hex().decode()
    assert commit.parent_ids == []
    assert commit.author.name == b"HGitaly Test"
    assert commit.author.email == b"hgitaly@heptapod.test"
    assert commit.author.date.seconds == int(now)

    request = FindCommitRequest(repository=grpc_repo, revision=ctx2.hex())
    response = grpc_stub.FindCommit(request)

    commit2 = response.commit
    assert commit2 is not None
    assert commit2.subject == b'Foo deux'
    assert commit2.body == b"Foo deux\n\nA very interesting bar"
    assert commit2.parent_ids == [ctx.hex().decode()]

    # TODO check with two parents, it'd be nice to have a helper to create
    # merge commits very quickly

    request = FindCommitRequest(repository=grpc_repo,
                                revision=b'branch/default')
    response = grpc_stub.FindCommit(request)
    assert response.commit == commit2

    # default GitLab branch not being set, it fallbacks on branch/default
    request = FindCommitRequest(repository=grpc_repo, revision=b'HEAD')
    assert response.commit == commit2

    wrapper.write_commit('animals',
                         message="in topic",
                         topic='antelope',
                         parent=ctx)
    request = FindCommitRequest(repository=grpc_repo,
                                revision=b'topic/default/antelope')
    response = grpc_stub.FindCommit(request)

    commit_top = response.commit
    assert commit_top is not None
    assert commit_top.subject == b"in topic"

    # with revision given in full "ref" form
    request = FindCommitRequest(repository=grpc_repo,
                                revision=b'refs/heads/topic/default/antelope')
    response = grpc_stub.FindCommit(request)
    assert response.commit == commit_top

    # with explicitely set GitLab branch:
    set_default_gitlab_branch(wrapper.repo, b'topic/default/antelope')
    request = FindCommitRequest(repository=grpc_repo, revision=b'HEAD')
    response = grpc_stub.FindCommit(request)
    assert response.commit == commit_top

    request = FindCommitRequest(repository=grpc_repo, revision=b'unknown')
    response = grpc_stub.FindCommit(request)
    assert not response.HasField('commit')


def test_commits_between(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    _, grpc_repo, changesets = make_tree_shaped_repo(server_repos_root)

    def do_rpc(gl_from, gl_to):
        request = CommitsBetweenRequest(repository=grpc_repo, to=gl_to)
        setattr(request, 'from', gl_from)
        resp = grpc_stub.CommitsBetween(request)
        return [pycompat.sysbytes(commit.id)
                for chunk in resp for commit in chunk.commits]

    base = changesets['base']
    top1, top2 = changesets['top1'], changesets['top2']
    assert do_rpc(base.hex(), b'topic/default/zzetop') == [
        top1.hex(), top2.hex()]

    # This is counter intuitive, check the docstring for CommitsBetween.
    # The actual expected result was checked by comparing with the reponse of
    # a reference Golang Gitaly 12.10.6 server working on conversion to Git of
    # this precise testing repo.
    assert do_rpc(b'branch/other', b'topic/default/zzetop') == [
        top1.hex(), top2.hex()]
    assert do_rpc(base.hex(), b'branch/other') == [
        changesets['other_base'].hex(), changesets['wild2'].hex()]

    assert do_rpc(base.hex(), b'does-not-exist') == []
    assert do_rpc(b'does-not-exist', base.hex()) == []


def test_find_commits(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    # prepare repo as:
    #
    #   2 (branch/default)
    #   |
    #   1
    #   |  3 (topic/default/feature)
    #   | /
    #   0
    #
    def do_rpc(revision=None, limit=None):
        request = FindCommitsRequest(repository=grpc_repo,
                                     revision=revision,
                                     limit=limit)
        resp = grpc_stub.FindCommits(request)
        return [pycompat.sysbytes(commit.id)
                for chunk in resp for commit in chunk.commits]

    ctx0 = wrapper.write_commit('foo')
    ctx1 = wrapper.write_commit('bar', parent=ctx0)
    ctx2 = wrapper.write_commit('baz', parent=ctx1)
    ctx3 = wrapper.write_commit('animals',
                                topic='feature',
                                parent=ctx0)
    # find commits on branch/default
    assert do_rpc(revision=b'branch/default') == [
        ctx2.hex(), ctx1.hex(), ctx0.hex()]
    # find commits on topic/default/feature
    assert do_rpc(revision=b'topic/default/feature') == [
        ctx3.hex(), ctx0.hex()]
    # when no revision passed; return all for now
    assert do_rpc() == [ctx3.hex(), ctx2.hex(), ctx1.hex(), ctx0.hex()]
    # when limit passed
    assert do_rpc(limit=2) == [ctx3.hex(), ctx2.hex()]


def test_list_commits_by_ref_name(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    def do_rpc(ref_names):
        request = ListCommitsByRefNameRequest(repository=grpc_repo,
                                              ref_names=ref_names)
        response = grpc_stub.ListCommitsByRefName(request)
        res = dict()
        for message in response:
            for pair in message.commit_refs:
                res[pair.ref_name] = pycompat.sysbytes(pair.commit.id)
        return res

    # prepare repo as:
    #
    #   2 (branch/default)
    #   |
    #   1
    #   |  3 (topic/default/feature)
    #   | /
    #   0
    #
    ctx0 = wrapper.write_commit('foo')
    wrapper.write_commit('bar')
    ctx2 = wrapper.write_commit('baz')
    ctx3 = wrapper.write_commit('animals', topic='feature', parent=ctx0)

    resp = do_rpc([b"branch/default", b"topic/default/feature", b"not_exists"])
    assert resp[b"branch/default"] == ctx2.hex()
    assert len(resp) == 2
    assert resp[b"topic/default/feature"] == ctx3.hex()


def test_count_divergening_commits(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    def do_rpc(gl_from, gl_to, max_count=None):
        request = CountDivergingCommitsRequest(repository=grpc_repo,
                                               to=gl_to,
                                               max_count=max_count)
        setattr(request, 'from', gl_from)
        response = grpc_stub.CountDivergingCommits(request)
        return [response.left_count, response.right_count]

    # prepare repo as:
    #
    #   2 (branch/default)
    #   |
    #   1
    #   |  3 (topic/default/feature)
    #   | /
    #   0
    #
    ctx0 = wrapper.write_commit('foo')
    wrapper.write_commit('bar')
    wrapper.write_commit('baz')
    wrapper.write_commit('animals', topic='feature', parent=ctx0)

    assert do_rpc(b"branch/default", b"topic/default/feature") == [2, 1]
    # count 0 for the same "from" and "to"
    assert do_rpc(b"branch/default", b"branch/default") == [0, 0]
    # when one of them is invalid ref
    assert do_rpc(b"branch/default", b"does-not-exists") == [0, 0]
    assert do_rpc(b"does-not-exists", b"branch/default") == [0, 0]
    # count bounded with max_count
    for max_count in [1, 2, 3]:
        resp = do_rpc(b"branch/default", b"topic/default/feature", max_count)
        assert (resp[0] + resp[1]) == max_count
        resp = do_rpc(b"topic/default/feature", b"branch/default", max_count)
        assert (resp[0] + resp[1]) == max_count


def test_count_commits(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    # prepare repo as:
    #
    #   2 (branch/default)
    #   |
    #   1
    #   |  3 (topic/default/feature)
    #   | /
    #   0
    #
    ctx0 = wrapper.write_commit('foo')
    ctx1 = wrapper.write_commit('bar', parent=ctx0)
    wrapper.write_commit('baz', parent=ctx1)
    wrapper.write_commit('animals',
                         topic='feature',
                         parent=ctx0)
    # count commits on branch/default
    request = CountCommitsRequest(repository=grpc_repo,
                                  revision=b'branch/default')
    response = grpc_stub.CountCommits(request)
    assert response.count == 3

    # when no revision passed, return total commits in repo
    request = CountCommitsRequest(repository=grpc_repo)
    response = grpc_stub.CountCommits(request)
    assert response.count == 4

    # test max_count, when no revision passed return total commits in repo
    request = CountCommitsRequest(repository=grpc_repo, max_count=2)
    response = grpc_stub.CountCommits(request)
    assert response.count == 2

    # count commits with target topic/default/feature
    request = CountCommitsRequest(repository=grpc_repo,
                                  revision=b'topic/default/feature')
    response = grpc_stub.CountCommits(request)
    assert response.count == 2

    # range notation
    request = CountCommitsRequest(
        repository=grpc_repo,
        revision=b'topic/default/feature..branch/default')
    response = grpc_stub.CountCommits(request)
    assert response.count == 2

    request = CountCommitsRequest(
        repository=grpc_repo,
        revision=b'branch/default..topic/default/feature')
    response = grpc_stub.CountCommits(request)
    assert response.count == 1

    # cases of revision not found
    for revision in (b'branch/default..unknown',
                     b'unknown..topic/default/feature',
                     b'unknown',
                     ):
        request = CountCommitsRequest(repository=grpc_repo, revision=revision)
        assert grpc_stub.CountCommits(request).count == 0


def test_last_commit_for_path(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    # prepare repo as:
    #
    #   1 (branch/default) changes 'foo'
    #   |
    #   |  2 (branch/other) creates 'sub/bar'
    #   | /
    #   0 creates 'foo'
    #
    ctx = wrapper.write_commit('foo')
    ctx1 = wrapper.write_commit('foo')
    # TODO should be done by testhelpers!
    (wrapper.path / 'sub').mkdir()
    ctx2 = wrapper.write_commit('sub/bar', branch='other', parent=ctx)

    def do_rpc(revision, path):
        """Call the method, returning directly commit.id, as bytes"""
        request = LastCommitForPathRequest(repository=grpc_repo,
                                           revision=revision,
                                           path=path)
        return pycompat.sysbytes(
            grpc_stub.LastCommitForPath(request).commit.id)

    assert do_rpc(revision=b'branch/default', path=b'foo') == ctx1.hex()
    assert do_rpc(revision=b'branch/other', path=b'foo') == ctx.hex()
    assert not do_rpc(revision=b'branch/default', path=b'sub/bar')
    assert do_rpc(revision=b'branch/other', path=b'sub/bar') == ctx2.hex()
    # recursive directory matching (see Rails tests for validation
    # that we must match on directories)
    assert do_rpc(revision=b'branch/other', path=b'sub') == ctx2.hex()


def test_list_commits_by_oid(grpc_channel, server_repos_root):
    grpc_stub = CommitServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    def do_rpc(oids):
        request = ListCommitsByOidRequest(repository=grpc_repo,
                                          oid=oids)
        resp = grpc_stub.ListCommitsByOid(request)
        return [pycompat.sysbytes(commit.id)
                for chunk in resp for commit in chunk.commits]

    ctx = wrapper.write_commit('foo')
    ctx2 = wrapper.write_commit('foo')

    # with 39, chances of collision are very thin and it still demonstrates
    # that prefix lookup works
    short = ctx.hex()[:39]
    short2 = ctx2.hex()[:39]

    assert do_rpc([short]) == [ctx.hex()]
    assert do_rpc([short, short2]) == [ctx.hex(), ctx2.hex()]

    assert do_rpc([]) == []

    unknown_sha = "6caf" * 9  # prefix of length 36, very unlikey to match
    assert do_rpc([unknown_sha]) == []
    assert do_rpc([unknown_sha, short]) == [ctx.hex()]
