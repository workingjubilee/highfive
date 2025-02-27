import json
import os

from highfive import payload


def load_fake(fake):
    fakes_dir = os.path.join(os.path.dirname(__file__), 'fakes')

    with open(os.path.join(fakes_dir, fake)) as fake:
        return fake.read()


def get_fake_filename(name):
    return os.path.join(os.path.dirname(__file__), 'fakes', name)


def get_repo_configs():
    return {
        'individuals_no_dirs': {
            "groups": {"all": ["@pnkfelix", "@nrc"]},
            "dirs": {},
        },
        'individuals_no_dirs_labels': {
            "groups": {"all": ["@pnkfelix", "@nrc"]},
            "dirs": {},
            "new_pr_labels": ["a", "b"],
        },
        'individuals_dirs': {
            "groups": {"all": ["@pnkfelix", "@nrc"]},
            "dirs": {"src/librustc": ["@aturon"]},
        },
        'individuals_dirs_2': {
            "groups": {"all": ["@pnkfelix", "@nrc"]},
            "dirs": {"src/foobazdir": ["@aturon"]},
        },
        'individual_files': {
            "groups": {"all": ["@pnkfelix", "@nrc"]},
            "dirs": {".travis.yml": ["@aturon"]},
        },
        'circular_groups': {
            "groups": {
                "all": ["some"],
                "some": ["all"],
            },
        },
        'nested_groups': {
            "groups": {
                "all": [],
                "a": ["@pnkfelix"],
                "b": ["@nrc"],
                "c": ["a", "b"]
            },
            "dirs": {"src/librustc_typeck": ["c"]},
        },
        'empty': {
            "groups": {"all": []},
            "dirs": {},
        },
        'mentions': {
            "groups": {"all": []},
            "dirs": {"compiler": ["@pnkfelix"]},
            "mentions": {
                "src/tools/cargo": {
                    "message": "this should not match startswith",
                    "reviewers": ["@ehuss"],
                },
                "error_codes.rs": {
                    "message": "bare .rs file should match endswith",
                    "reviewers": ["@GuillaumeGomez"],
                },
                "compiler/rustc": {
                    "message": "directory should match all files within",
                    "reviewers": ["@pnkfelix"],
                }
            }
        },
        'mentions_without_dirs': {
            "groups": {"all": ["@JohnTitor"]},
            "dirs": {},
            "mentions": {
                "README.md": {
                    "message": "should be pinged",
                    "reviewers": ["@JohnTitor"],
                }
            }
        },
        'teams': {
            "groups": {"all": ["@ehuss"], "a": ["@pnkfelix"], "d": ["@e"], "compiler-team": ["@niko"], "b/c": ["@nrc"]}
        }
    }


def get_global_configs():
    return {
        'base': {
            "groups": {
                "core": ["@alexcrichton"],
            }
        },
        'has_all': {
            "groups": {"all": ["@alexcrichton"]}
        },
    }


class Payload(object):
    @staticmethod
    def new_comment():
        with open(get_fake_filename('create-comment.payload'), 'r') as fin:
            p = json.load(fin)
        return payload.Payload(p)

    @staticmethod
    def new_pr(
            number=7, pr_body='The PR comment.', pr_url='https://the.url/',
            repo_name='repo-name', repo_owner='repo-owner', pr_author='prAuthor'
    ):
        with open(get_fake_filename('open-pr.payload'), 'r') as fin:
            p = json.load(fin)

        p['number'] = number
        p['pull_request']['body'] = pr_body
        p['pull_request']['url'] = pr_url
        p['pull_request']['base']['repo']['name'] = repo_name
        p['pull_request']['base']['repo']['owner']['login'] = repo_owner
        p['pull_request']['user']['login'] = pr_author

        return payload.Payload(p)
