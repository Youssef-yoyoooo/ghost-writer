import docker
import os
from typing import Dict, Any

class DockerManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to Docker daemon: {str(e)}")

    def run_test(self, code_path: str, test_path: str, image: str = "python:3.9-slim") -> Dict[str, Any]:
        """
        Execute tests in a sandboxed Docker container.
        """
        # Define absolute paths for mounting
        code_path = os.path.abspath(code_path)
        test_path = os.path.abspath(test_path)
        
        container_code_path = "/app/code.py"
        container_test_path = "/app/test_code.py"
        
        # Build command to run pytest
        command = f"pip install pytest && pytest {container_test_path}"
        
        try:
            container = self.client.containers.run(
                image=image,
                command=["sh", "-c", command],
                volumes={
                    code_path: {"bind": container_code_path, "mode": "ro"},
                    test_path: {"bind": container_test_path, "mode": "ro"},
                },
                detach=True,
                remove=True
            )
            
            # Wait for completion and capture logs
            result = container.wait()
            logs = container.logs().decode("utf-8")
            
            return {
                "exit_code": result["StatusCode"],
                "logs": logs,
                "success": result["StatusCode"] == 0
            }
        except Exception as e:
            return {
                "exit_code": -1,
                "logs": str(e),
                "success": False
            }
