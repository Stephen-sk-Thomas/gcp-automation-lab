# gcp-automation-lab
Python batch job that updates Gmail signatures from user data (name/department/phone), with dry-run, retries, and a run report.

## Run
Plan (dry-run):

- `python3 gcp_signature_updater.py plan`
Apply:

- `python3 gcp_signature_updater.py apply`
Notes:

This demo does not call Google APIs. It simulates updates by writing to directory.json.
A run_report.json file is generated each run.
Both files are generated output and are ignored by git.
If you run apply twice, the second run should show changed: 0 (idempotent updates).
