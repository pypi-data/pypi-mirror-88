from common_harness_lib import CommonHarnessLib
from typing import Union, Optional, List  # NOQA

common = CommonHarnessLib(enable_s3=False, ignore_json_args=True)

common.validate_dict({
    "url": "test",
    "method": "test",
    "wordlists": ["test", "5"],
    "request_body": "1",
    "request_headers": ["5"]
}, {
    # Required
    "url": str,
    "method": str,
    "wordlists": List[str],
    # # Optional
    "request_body": Optional[str],
    "request_headers": Optional[List[str]]
})
