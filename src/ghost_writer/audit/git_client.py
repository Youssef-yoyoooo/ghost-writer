import git
from typing import List, Dict, Any
import os

class GitClient:
    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        try:
            self.repo = git.Repo(self.repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Path '{repo_path}' is not a valid git repository.")

    def get_commits(self, limit: int = 100) -> List[git.Commit]:
        """Retrieve recent commits from the repository."""
        return list(self.repo.iter_commits(max_count=limit))

    def get_commit_diffs(self, commit: git.Commit) -> List[Dict[str, Any]]:
        """Extract diffs for a specific commit."""
        diffs = []
        if not commit.parents:
            # Root commit: diff against empty tree
            diff_index = commit.diff(git.NULL_TREE, reverse=True, create_patch=True)
        else:
            # Normal commit: diff against first parent
            diff_index = commit.parents[0].diff(commit, create_patch=True)
        
        for diff in diff_index:
            diff_text = ""
            if diff.diff:
                try:
                    diff_text = diff.diff.decode("utf-8", "ignore")
                except AttributeError:
                    # In some cases diff.diff might be a string already or other type
                    diff_text = str(diff.diff)

            diffs.append({
                "file_path": diff.b_path if diff.b_path else diff.a_path,
                "diff_text": diff_text,
                "is_new": diff.new_file,
                "is_deleted": diff.deleted_file,
            })
        return diffs

    def get_commit_metadata(self, commit: git.Commit) -> Dict[str, Any]:
        """Extract metadata like message, author, and timestamp."""
        return {
            "hexsha": commit.hexsha,
            "message": commit.message.strip(),
            "author": commit.author.name,
            "email": commit.author.email,
            "timestamp": commit.authored_datetime,
            "stats": commit.stats.total,
        }
