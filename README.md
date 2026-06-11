# gcp-automation-lab
is a small Python script that updates Gmail email signatures in bulk using a list of users (name, department, phone). 
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
