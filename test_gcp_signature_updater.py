# Simple tests for gcp_signature_updater.py
# Goal: keep it readable and prove the core logic works.

import gcp_signature_updater as s


def test_build_signature():
    user = {"full_name": "Alex Kim", "department": "Engineering", "phone": "555-0101"}
    assert s.build_signature(user) == "Alex Kim | Engineering | 555-0101"
