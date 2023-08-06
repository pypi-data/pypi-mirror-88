#!/usr/bin/env python3
import typing
import sys
from os import environ
from json import loads
from subprocess import Popen, CalledProcessError


def error_shortener(error_type, value, traceback):
    print(error_type.__name__ + ": " + str(value))


class CommonHarnessLib:

    def __init__(
            self,
            enable_s3: bool = True,
            ignore_json_args: bool = False,
            shorten_errors: bool = True
         ):
        # Get JSON parameters from harness
        if not ignore_json_args:
            self.get_json_args()
        # Deal with s3 initialization
        if enable_s3:
            self.init_s3()
        # Hide error traceback
        if shorten_errors:
            sys.excepthook = error_shortener

    """
        Parse JSON from argv[1], which is standard harness input format
    """
    def get_json_args(self):
        try:
            self.json_args = loads(sys.argv[1])
        except IndexError:
            raise ValueError("Harness JSON args not given.")
        except ValueError:
            raise ValueError("Invalid JSON harness args.")
        except Exception as e:
            raise ValueError(type(e).__name__ + ": " + e)

    """
        Initiliase and verify s3 details
    """
    def init_s3(self):
        # Only import s3 libraries if s3 is enabled (unholy but efficient)
        import boto3
        from botocore.client import Config
        # Validate environ vars exist
        try:
            self.validate_dict(environ, {
                    "AWS_WORDLIST_BUCKET": str,
                    "S3_URL": typing.Optional[str],
                    "AWS_ACCESS_KEY_ID": str,
                    "AWS_SECRET_ACCESS_KEY": str,
                    "AWS_REGION": str
                })
        except ValueError as e:
            error = e.args[0].replace("parameter", "environment variable")
            raise ValueError(error) from None
        # Create S3 resources from environ
        self.AWS_WORDLIST_BUCKET = environ.get("AWS_WORDLIST_BUCKET")
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=environ.get("S3_URL"),
            aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
            region_name=environ.get("AWS_REGION")
        )
        # Validate bucket details valid
        try:
            self.s3.meta.client.head_bucket(
                Bucket=self.AWS_WORDLIST_BUCKET
            )
        except Exception as e:
            self.handle_s3_exception(e)

    """
        Handle common s3 exceptions
    """
    def handle_s3_exception(self, error: Exception):
        error_type = type(error)
        if error_type == self.s3.meta.client.exceptions.ClientError:
            raise ValueError("Forbidden.") from None
        elif error_type == self.s3.meta.client.exceptions.NoSuchBucket:
            raise ValueError("Bucket does not exist.") from None
        elif error_type == self.s3.meta.client.exceptions.NoSuchKey:
            raise ValueError("File does not exist.") from None
        else:
            raise error from None

    """
        Get content of a bucket object as a string.
    """
    def get_object_content(self, bucket_name: str, object_key: str):
        s3_object = self.s3.Object(bucket_name, object_key)
        try:
            return s3_object.get()["Body"].read().decode("utf-8")
        except self.s3.meta.client.exceptions.NoSuchKey:
            raise ValueError(f"File {object_key} does not exist.") from None
        except Exception as e:
            self.handle_s3_exception(e)

    """
        Download a list of wordlist keys, and join to create one wordlist.
    """
    def download_wordlists(self, wordlist_keys: str):
        # Create file
        with open("wordlist.txt", "w") as f:
            f.write("")
        # Download each wordlist
        for idx, key in enumerate(wordlist_keys):
            # Get s3 content and handle errors
            try:
                content = self.get_object_content(
                    self.AWS_WORDLIST_BUCKET, key
                )
            except Exception as e:
                self.handle_s3_exception(e)
            # Append to file (so we don't keep all text in memory)
            with open("wordlist.txt", "a") as f:
                f.write(content.strip())
                # Add newline (if not final)
                if idx != len(wordlist_keys) - 1:
                    f.write("\n")
        # Return wordlist filepath
        return "wordlist.txt"

    """
        Validate dictionary entries by type
        i.e.
            validate_dict({"wordlists": [], "company": "a"}, {
                "wordlists": List[str],
                "company": str
            })
    """
    # Validate dictionary entries match required type
    def validate_dict(self, args: dict, required: dict):
        # Iterate through required entries
        for required_param, required_type in required.items():
            # If given type is typing.Any (or similar), don't check
            if isinstance(required_type, typing._SpecialForm):
                continue
            # Get user's input (if exists)
            user_input = args.get(required_param)

            # If typing.List or typing.Union given, get "inner" types
            if hasattr(required_type, "__args__"):
                allowed_types = required_type.__args__
            else:
                allowed_types = (required_type,)

            # Skip if permissable nonetype
            if user_input is None and type(None) in allowed_types:
                continue

            # If dict is required, run recursively
            if type(required_type) is dict:
                if type(user_input) is dict:
                    self.validate_dict(user_input or {}, required_type)
                    continue
                else:
                    self.validate_dict({}, {required_param: dict})
                    continue

            LIST_FAILED = ValueError(
                f"Parameter {required_param} must be a list with types: {allowed_types}."  # NOQA: E501
            )

            # If any sub-lists in union, check sublists
            for arg in allowed_types:
                if getattr(arg, "_name", "") == "List":
                    # If valid, replace pylint List type with basic list
                    if self.validate_list(arg, user_input):
                        allowed_types = list(allowed_types)
                        allowed_types.remove(arg)
                        allowed_types.append(list)
                        allowed_types = tuple(allowed_types)
                    else:
                        raise LIST_FAILED

            # If type is list, check each item
            if getattr(required_type, "_name", "") == "List":
                if self.validate_list(required_type, user_input):
                    continue
                else:
                    raise LIST_FAILED

            # Validate non-dict non-list matches
            if not isinstance(user_input, allowed_types):
                if type(user_input) is None:
                    raise ValueError(f"Missing required parameter {required_param} of type {required_type}.")  # NOQA: E501
                else:
                    raise ValueError(
                        f"Provided parameter {required_param} should be type {required_type}."  # NOQA: E501
                    )

    """
        Validate a list type against a list
        i.e. validate_list(List[str], ["test"])
    """
    def validate_list(self, typ, li):
        if type(li) is not list:
            return False
        allowed_types = typ.__args__
        return all(
            isinstance(i, allowed_types) for i in li
        )

    """
        Run simple command with subprocess Popen
    """
    def run_command(
            self,
            command,  # Command to run in array
            keep_alive=True,  # Whether to keep python open until complete
            throw_errors=False,  # Raise an error if the program errors
         ):
        popen = Popen(command, universal_newlines=True)
        if keep_alive:
            return_code = popen.wait()
            if return_code and throw_errors:
                raise CalledProcessError(return_code, command)
