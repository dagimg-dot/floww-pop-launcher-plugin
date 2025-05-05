#!/usr/bin/env python3

import json
import sys
import os
import subprocess
import shlex

# Path to workflows
WORKFLOWS_PATH = os.path.expanduser("~/.config/floww/workflows")

# For debugging
DEBUG = True


def debug_log(message):
    if DEBUG:
        log_dir = os.path.expanduser("~/.local/state")
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "floww-plugin.log"), "a") as f:
            f.write(f"{message}\n")


def get_user_environment():
    try:
        shell = os.environ.get("SHELL", "/bin/bash")
        debug_log(f"Using shell: {shell}")

        cmd = [shell, "-l", "-c", "env"]
        debug_log(f"Running command to get environment: {shlex.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

        if result.returncode != 0:
            debug_log(
                f"Failed to get user environment (return code {result.returncode}): {
                    result.stderr
                }"
            )
            return os.environ.copy()

        env = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                env[key] = value

        debug_log(
            f"Successfully got user environment. PATH: {env.get('PATH', 'Not found')}"
        )
        return env
    except FileNotFoundError:
        debug_log(f"Error: Shell '{shell}' not found. Falling back to os.environ.")
        return os.environ.copy()
    except subprocess.TimeoutExpired:
        debug_log(
            "Error: Getting environment from shell timed out. Falling back to os.environ."
        )
        return os.environ.copy()
    except Exception as e:
        debug_log(
            f"Unexpected error getting user environment: {
                e
            }. Falling back to os.environ."
        )
        return os.environ.copy()


def get_workflows():
    workflows = []

    if not os.path.exists(WORKFLOWS_PATH):
        debug_log(f"Workflows path does not exist: {WORKFLOWS_PATH}")
        return workflows

    for file in os.listdir(WORKFLOWS_PATH):
        if file.endswith((".yaml", ".yml", ".json", ".toml")):
            workflow_path = os.path.join(WORKFLOWS_PATH, file)
            workflow_name = os.path.splitext(file)[0]  # Get name without extension

            description = ""
            try:
                with open(workflow_path, "r") as f:
                    for line in f:
                        if line.strip().startswith("description:"):
                            description = (
                                line.split(":", 1)[1].strip().strip('"').strip("'")
                            )
                            break
                    if not description:
                        description = "Floww workflow"
            except Exception:
                description = "Floww workflow"

            workflows.append((workflow_name, workflow_path, description))

    return workflows


def execute_floww_command(workflow_name, append):
    debug_log(f"Executing workflow: {workflow_name}")

    cmd = f"floww apply {shlex.quote(workflow_name)}"
    debug_log(f"Command string: {cmd}")

    append_arg = "-a" if append else ""
    debug_log(f"Append enabled: {append}")

    try:
        env = get_user_environment()

        if "PATH" not in env:
            debug_log(
                "Warning: PATH not found in retrieved environment. Using os.environ PATH."
            )
            env["PATH"] = os.environ.get("PATH", "")

        current_path = env.get("PATH", "")
        eget_bin = os.path.expanduser("~/.eget/bin")
        local_bin = os.path.expanduser("~/.local/bin")

        debug_log(f"current_path from shell: {current_path}")

        new_path_parts = [eget_bin, local_bin]
        if current_path:
            new_path_parts.extend(current_path.split(os.pathsep))

        seen = set()
        unique_path_parts = [
            p for p in new_path_parts if not (p in seen or seen.add(p))
        ]

        env["PATH"] = os.pathsep.join(unique_path_parts)
        debug_log(f"Using final modified PATH: {env['PATH']}")

        full_cmd = f"nohup {cmd} {append_arg} >/dev/null 2>&1 &"
        debug_log(f"Full command: {full_cmd}")

        process = subprocess.Popen(
            full_cmd,
            shell=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        try:
            stdout, stderr = process.communicate(timeout=1.0)
            if stdout:
                debug_log(f"stdout: {stdout.decode()}")
            if stderr:
                debug_log(f"stderr: {stderr.decode()}")
        except subprocess.TimeoutExpired:
            debug_log("Process running in background (communicate timed out).")

        debug_log(f"Command started with PID {process.pid}")
        return True
    except Exception as e:
        debug_log(f"Error executing workflow: {e}")
        return False


class WorkflowEntry:
    def __init__(self, name, path, description):
        self.name = name
        self.path = path
        self.description = description


# The plugin app
class App(object):
    def __init__(self):
        self.entries = []
        self.append = False

    def append_entries(self, entries):
        for entry in entries:
            self.entries.append(WorkflowEntry(entry[0], entry[1], entry[2]))

    # When the user activates an entry
    def activate(self, index):
        debug_log(f"Activate request received for index: {index}")
        if not self.entries or index >= len(self.entries):
            debug_log(f"Invalid index: {index}, entries count: {len(self.entries)}")
            return

        workflow_name = self.entries[index].name
        debug_log(f"Activating workflow: {workflow_name}")

        execute_floww_command(workflow_name, self.append)

        # Send Close response to pop-launcher
        sys.stdout.write(json.dumps("Close") + "\n")
        sys.stdout.flush()
        debug_log("Sent Close response to pop-launcher")

    # When the user types something in the search bar
    def search(self, query):
        debug_log(f"Search request received: {query}")
        self.entries = []

        all_workflows = get_workflows()
        debug_log(f"Found {len(all_workflows)} workflows")

        # Filter workflows if query contains more than just the prefix
        if query:
            # Handle both "fl", "fl ", "fa" and "fa " prefixes
            if query.startswith("fl ") or query.startswith("fa "):
                if query.startswith("fa "):
                    self.append = True
                search_term = query[3:].lower()
            elif query.startswith("fl") or query.startswith("fa"):
                if query.startswith("fa"):
                    self.append = True
                search_term = query[2:].lower()

            if search_term:
                filtered_workflows = [
                    w for w in all_workflows if search_term in w[0].lower()
                ]
                self.append_entries(filtered_workflows)
                debug_log(
                    f"Filtered to {len(filtered_workflows)} workflows with term '{
                        search_term
                    }'"
                )
            else:
                self.append_entries(all_workflows)
                debug_log(f"Showing all {len(all_workflows)} workflows")
        else:
            self.append_entries(all_workflows)
            debug_log(f"Showing all {len(all_workflows)} workflows")

        # Send results
        for index, entry in enumerate(self.entries):
            response = {
                "Append": {
                    "id": index,
                    "name": entry.name,
                    "description": entry.description,
                    "keywords": None,
                    "icon": None,
                    "exec": None,
                    "window": None,
                }
            }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            debug_log(f"Appended result: {entry.name}")

        sys.stdout.write(json.dumps("Finished") + "\n")
        sys.stdout.flush()
        debug_log("Sent Finished response")


# Main execution
def main():
    debug_log("Plugin started")
    app = App()

    for line in sys.stdin:
        try:
            debug_log(f"Received: {line.strip()}")
            request = json.loads(line)

            if isinstance(request, dict):
                if "Search" in request:
                    app.search(request["Search"])
                elif "Activate" in request:
                    app.activate(request["Activate"])
            elif request == "Interrupt":
                debug_log("Received Interrupt request")
            elif request == "Exit":
                debug_log("Received Exit request")
                break

        except json.decoder.JSONDecodeError as e:
            debug_log(f"JSON decode error: {e}, Line: {line}")
        except Exception as e:
            debug_log(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
