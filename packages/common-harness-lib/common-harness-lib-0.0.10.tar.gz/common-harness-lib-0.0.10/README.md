# common-harness-lib
[H2H Toolkit] Common python library for harness functions within task docker images.


## Usage:
Create object with `CommonHarnessLib()`. To disable s3 features, use the `disable_s3=False` flag.

Methods:
* S3:
  * **handle_s3_exception(err: Exception)**: Handle's common s3 errors.
  * **get_object_content(bucket_name: str, object_key: str)**: Get's a s3 object content as a string.
  * **download_wordlists(wordlist_keys: List[str])**: Downloads a list of wordlists from s3 and combines them as one file.
* System:
  * **run_command(command: List[str])**: Run a command (i.e. ["echo", "hello world"])
* Validation:
  * **validate_dict({"firstname": str, "age": int})**: Validates that a dict matches required type entries
