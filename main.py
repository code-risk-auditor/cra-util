import json
import os
import shutil
import subprocess

# import git

# Get temp folder via API
# rw_dir = os.path.join(os.getcwd(), "temp")
# if os.path.exists(rw_dir):
#     shutil.rmtree(rw_dir)
# os.makedirs(rw_dir)
#
#
# empty_repo = git.Repo.init(os.path.join(rw_dir, "empty"))
# origin = empty_repo.create_remote("origin","https://github.com/celery/django-celery-beat")
#
# assert origin.exists()
#
# origin.fetch()
#
# # Checkout master
# empty_repo.create_head("main", origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
#
# # Now we can do a python env-things and install stuff
# # Create a venv in the folder
# os.system(f"python -m venv {rw_dir}/empty/venv")

print("Hello World")
print("Current working dir is ", os.getcwd())

# Install the requirements
req_file = "requirements.txt"
cmd = f'pip install -r {req_file}'
subprocess.call(cmd, shell=True, executable='/bin/bash')

# Second call for freeze
print("Freeze")
cmd = f'pip freeze'
result = subprocess.check_output(cmd, shell=True, executable='/bin/bash').decode("utf-8")

print("After Freeze")

# Parse req_file
original_requirements = {}
with open(f"{req_file}", "r") as f:
    reqs = f.readlines()
    for req in reqs:
        req = req.strip()
        if req:
            if "==" in req:
                dependency, version = req.split("==")
                original_requirements[dependency] = version
            elif ">=" in req:
                dependency, version = req.split(">=")
                original_requirements[dependency] = version
            else:
                print("Cannot parse line in req_file: ", req)

print("Parsed: {}".format(original_requirements))


# Parse the results
for line in result.splitlines():
    dependency, version = line.split("==")

    print(f"Dependency: {dependency}, version: {version} {'*' if dependency in original_requirements else ''}")


# Now do dependency tree
print("Dependency tree")
# cmd = f'source venv/bin/activate && pip install pipdeptree graphviz'
# subprocess.call(cmd, shell=True, executable='/bin/bash', cwd=f"{rw_dir}/empty")

cmd = f'pipdeptree -e pipdeptree --graph-output pdf > graph.pdf'
result = subprocess.check_output(cmd, shell=True, executable='/bin/bash').decode("utf-8")

cmd = f'pipdeptree -e pipdeptree,pip,setuptools,graphviz,packaging --json'
result = subprocess.check_output(cmd, shell=True, executable='/bin/bash').decode("utf-8")

deptree = json.loads(result)

"""
Example of the output json:

```
[
    {
        "package": {
            "key": "amqp",
            "package_name": "amqp",
            "installed_version": "5.2.0"
        },
        "dependencies": [
            {
                "key": "vine",
                "package_name": "vine",
                "installed_version": "5.1.0",
                "required_version": ">=5.0.0,<6.0.0"
            }
        ]
    },
    {
        "package": {
            "key": "asgiref",
            "package_name": "asgiref",
            "installed_version": "3.8.1"
        },
        "dependencies": [
            {
                "key": "typing-extensions",
                "package_name": "typing_extensions",
                "installed_version": "4.12.1",
                "required_version": ">=4"
            }
        ]
    },
    {
        "package": {
            "key": "billiard",
            "package_name": "billiard",
            "installed_version": "4.2.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "celery",
            "package_name": "celery",
            "installed_version": "5.4.0"
        },
        "dependencies": [
            {
                "key": "billiard",
                "package_name": "billiard",
                "installed_version": "4.2.0",
                "required_version": ">=4.2.0,<5.0"
            },
            {
                "key": "click",
                "package_name": "click",
                "installed_version": "8.1.7",
                "required_version": ">=8.1.2,<9.0"
            },
            {
                "key": "click-didyoumean",
                "package_name": "click-didyoumean",
                "installed_version": "0.3.1",
                "required_version": ">=0.3.0"
            },
            {
                "key": "click-plugins",
                "package_name": "click-plugins",
                "installed_version": "1.1.1",
                "required_version": ">=1.1.1"
            },
            {
                "key": "click-repl",
                "package_name": "click-repl",
                "installed_version": "0.3.0",
                "required_version": ">=0.2.0"
            },
            {
                "key": "kombu",
                "package_name": "kombu",
                "installed_version": "5.3.7",
                "required_version": ">=5.3.4,<6.0"
            },
            {
                "key": "python-dateutil",
                "package_name": "python-dateutil",
                "installed_version": "2.9.0.post0",
                "required_version": ">=2.8.2"
            },
            {
                "key": "tzdata",
                "package_name": "tzdata",
                "installed_version": "2024.1",
                "required_version": ">=2022.7"
            },
            {
                "key": "vine",
                "package_name": "vine",
                "installed_version": "5.1.0",
                "required_version": ">=5.1.0,<6.0"
            }
        ]
    },
    {
        "package": {
            "key": "click",
            "package_name": "click",
            "installed_version": "8.1.7"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "click-didyoumean",
            "package_name": "click-didyoumean",
            "installed_version": "0.3.1"
        },
        "dependencies": [
            {
                "key": "click",
                "package_name": "click",
                "installed_version": "8.1.7",
                "required_version": ">=7"
            }
        ]
    },
    {
        "package": {
            "key": "click-plugins",
            "package_name": "click-plugins",
            "installed_version": "1.1.1"
        },
        "dependencies": [
            {
                "key": "click",
                "package_name": "click",
                "installed_version": "8.1.7",
                "required_version": ">=4.0"
            }
        ]
    },
    {
        "package": {
            "key": "click-repl",
            "package_name": "click-repl",
            "installed_version": "0.3.0"
        },
        "dependencies": [
            {
                "key": "click",
                "package_name": "click",
                "installed_version": "8.1.7",
                "required_version": ">=7.0"
            },
            {
                "key": "prompt-toolkit",
                "package_name": "prompt_toolkit",
                "installed_version": "3.0.45",
                "required_version": ">=3.0.36"
            }
        ]
    },
    {
        "package": {
            "key": "cron-descriptor",
            "package_name": "cron-descriptor",
            "installed_version": "1.4.3"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "django",
            "package_name": "Django",
            "installed_version": "4.2.13"
        },
        "dependencies": [
            {
                "key": "asgiref",
                "package_name": "asgiref",
                "installed_version": "3.8.1",
                "required_version": ">=3.6.0,<4"
            },
            {
                "key": "sqlparse",
                "package_name": "sqlparse",
                "installed_version": "0.5.0",
                "required_version": ">=0.3.1"
            }
        ]
    },
    {
        "package": {
            "key": "django-timezone-field",
            "package_name": "django-timezone-field",
            "installed_version": "6.1.0"
        },
        "dependencies": [
            {
                "key": "django",
                "package_name": "Django",
                "installed_version": "4.2.13",
                "required_version": ">=3.2,<6.0"
            }
        ]
    },
    {
        "package": {
            "key": "kombu",
            "package_name": "kombu",
            "installed_version": "5.3.7"
        },
        "dependencies": [
            {
                "key": "amqp",
                "package_name": "amqp",
                "installed_version": "5.2.0",
                "required_version": ">=5.1.1,<6.0.0"
            },
            {
                "key": "typing-extensions",
                "package_name": "typing_extensions",
                "installed_version": "4.12.1",
                "required_version": "Any"
            },
            {
                "key": "vine",
                "package_name": "vine",
                "installed_version": "5.1.0",
                "required_version": "Any"
            }
        ]
    },
    {
        "package": {
            "key": "packaging",
            "package_name": "packaging",
            "installed_version": "24.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "pip",
            "package_name": "pip",
            "installed_version": "24.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "pipdeptree",
            "package_name": "pipdeptree",
            "installed_version": "2.22.0"
        },
        "dependencies": [
            {
                "key": "packaging",
                "package_name": "packaging",
                "installed_version": "24.0",
                "required_version": ">=23.1"
            },
            {
                "key": "pip",
                "package_name": "pip",
                "installed_version": "24.0",
                "required_version": ">=23.1.2"
            }
        ]
    },
    {
        "package": {
            "key": "prompt-toolkit",
            "package_name": "prompt_toolkit",
            "installed_version": "3.0.45"
        },
        "dependencies": [
            {
                "key": "wcwidth",
                "package_name": "wcwidth",
                "installed_version": "0.2.13",
                "required_version": "Any"
            }
        ]
    },
    {
        "package": {
            "key": "python-crontab",
            "package_name": "python-crontab",
            "installed_version": "3.1.0"
        },
        "dependencies": [
            {
                "key": "python-dateutil",
                "package_name": "python-dateutil",
                "installed_version": "2.9.0.post0",
                "required_version": "Any"
            }
        ]
    },
    {
        "package": {
            "key": "python-dateutil",
            "package_name": "python-dateutil",
            "installed_version": "2.9.0.post0"
        },
        "dependencies": [
            {
                "key": "six",
                "package_name": "six",
                "installed_version": "1.16.0",
                "required_version": ">=1.5"
            }
        ]
    },
    {
        "package": {
            "key": "setuptools",
            "package_name": "setuptools",
            "installed_version": "58.0.4"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "six",
            "package_name": "six",
            "installed_version": "1.16.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "sqlparse",
            "package_name": "sqlparse",
            "installed_version": "0.5.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "typing-extensions",
            "package_name": "typing_extensions",
            "installed_version": "4.12.1"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "tzdata",
            "package_name": "tzdata",
            "installed_version": "2024.1"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "vine",
            "package_name": "vine",
            "installed_version": "5.1.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "wcwidth",
            "package_name": "wcwidth",
            "installed_version": "0.2.13"
        },
        "dependencies": []
    }
]
```
"""

# Now we write a recursive function to generate the graphviz file from aboves structure
dotfile = """digraph G {
    rankdir=TD;
"""

for package in deptree:
    dotfile += f'"{package["package"]["package_name"]}" [label="{package["package"]["package_name"]}"];\n'

    for dep in package["dependencies"]:
        dotfile += f'"{package["package"]["package_name"]}" -> "{dep["package_name"]}" [label="{dep["required_version"]}"];\n'

dotfile += "}"

print(dotfile)
