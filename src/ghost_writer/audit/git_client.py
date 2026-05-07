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
        # If it's the first commit, we diff against the empty tree
        parent = commit.parents[0] if commit.parents else git.NULL_TREE
        
        for diff in parent.diff(commit, create_patch=True):
            diffs.append({
                "file_path": diff.b_path,
                "diff_text": diff.diff.decode("utf-8", "ignore") if diff.diff else "",
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
