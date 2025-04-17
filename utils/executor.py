# utils/executor.py
import docker
from docker.errors import DockerException
from utils.packager import package_function, cleanup_temp_dir
from fastapi import HTTPException
import asyncio

async def execute_function(function_data: dict) -> dict:
    client = docker.from_env()
    language = function_data["language"]
    timeout = function_data["timeout"]
    image = "serverless-python" if language == "python" else "serverless-javascript"

    # Package the function
    temp_dir, file_name = package_function(function_data)

    try:
        # Create and start container
        container = client.containers.create(
            image,
            mem_limit="128m",  # 128MB memory limit
            auto_remove=True,
            volumes={temp_dir: {"bind": "/app", "mode": "rw"}},
        )
        container.start()

        # Enforce timeout using asyncio
        try:
            await asyncio.wait_for(
                asyncio.to_thread(container.wait), timeout=timeout
            )
        except asyncio.TimeoutError:
            raise HTTPException(status_code=500, detail="Function execution timed out")

        # Capture logs
        logs = container.logs().decode("utf-8")
        return {"output": logs, "success": True}

    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cleanup_temp_dir(temp_dir)
