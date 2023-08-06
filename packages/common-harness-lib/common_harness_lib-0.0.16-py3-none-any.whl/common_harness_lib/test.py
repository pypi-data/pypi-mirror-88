from common_harness_lib import CommonHarnessLib
from typing import Union, Optional

z = CommonHarnessLib(enable_s3=False, ignore_json_args=True)

z.validate_dict({
    "a": "a",
    "b": 5
}, {
    "a": Optional[Union[int, str]],
    "b": int
})
