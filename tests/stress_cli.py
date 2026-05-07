
import pytest

@pytest.fixture
def client():
    client = GitClient(path)
    yield client
    client.close()  # Ensure the client is properly closed

def test_disposed_client(client):
    with pytest.raises(GitError):
        client.get_commits(limit=1)  # Should fail if the client is not disposed
