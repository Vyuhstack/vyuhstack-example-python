# VyuhStack example: Python (FastAPI)

A FastAPI app served by uvicorn under systemd, with its own virtualenv. The page
and `/health` show the commit the process was started from, so you can see each
push go live.

## One-time VM setup

Run on the VM with sudo:

```bash
apt update && apt install -y git python3 python3-venv
```

Then connect the repo in VyuhStack (settings below) and click **Verify**, which
clones it into `/opt/app`. After that, install the service:

```bash
cp /opt/app/deploy/app.service /etc/systemd/system/app.service
systemctl daemon-reload
systemctl enable app
```

The first deploy creates the virtualenv, installs the dependencies and starts it.

## Deploy from Git settings

| Field | Value |
|---|---|
| Repository URL | `https://github.com/Vyuhstack/vyuhstack-example-python.git` |
| Branch | `main` |
| Folder on VM | `/opt/app` |
| Run as user | `vyuh-user` |
| Build | `[ -d .venv ] \|\| python3 -m venv .venv`<br>`.venv/bin/pip install -q -r requirements.txt` |
| Release | `sudo -n systemctl restart app` |

Application port in VyuhStack: `8000`.

The virtualenv lives in the repo folder and is git-ignored, so deploys keep it
and only install what changed.

`sudo -n` needs passwordless sudo for `vyuh-user`. VyuhStack VMs have it by
default; check with `runuser -l vyuh-user -c 'sudo -n true && echo ok'`.
Otherwise add a rule with `visudo -f /etc/sudoers.d/vyuhstack-deploy`:

```
vyuh-user ALL=(root) NOPASSWD: /usr/bin/systemctl restart app
```

## Check it

```bash
curl -s http://<vm-hostname>/health
```

Push a change and the `commit` value updates after the deploy finishes.

## Try a failed build

Pin a version that doesn't exist in `requirements.txt` (for example
`fastapi==0.0.0`) and push. The deploy fails at `pip install`, the release step
doesn't run, and the running app keeps serving the old commit.
