python_sources(name="lib")

python_tests(
    name="tests"
)
python_aws_lambda_function(
    name="lambda",
    runtime="python3.10",
    handler="function.py:lambda_handler",
    output_path="aemo-inventory.zip"
)