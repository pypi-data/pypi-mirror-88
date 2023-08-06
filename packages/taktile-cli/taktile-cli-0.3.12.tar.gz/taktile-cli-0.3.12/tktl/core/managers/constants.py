TEMPLATE_PROJECT_DIRS = [
    "src/",
    "assets/",
    "tests/",
]

TEMPLATE_PROJECT_FILES = [
    "template/src/endpoints.py",
    "template/assets/model.joblib",
    "template/assets/loans_test.pqt",
    "template/tests/test_accuracy.py",
    "template/tests/test_plausibility.py",
    "template/tests/test_schema.py",
    "template/.gitignore",
    "template/.gitattributes",
    "template/.buildfile",
    "template/.dockerignore",
    "template/README.md",
    "template/requirements.txt",
]


CONFIG_FILE_TEMPLATE = """
# If this option is set only commits with a commit message starting
# by the deployment_prefix will be deployed
# deployment_prefix: "#deploy"

service:

  # The number of replicas of your service
  # Replicas are exact copies of your service, each request will be randomly
  # directed to each of them
  replicas: 1

  # Format: <instance_kind>.<instance_size>
  # Only 'gp' (general purpose) instance_kind is supported for now
  # instance_size can be: small, medium, large, xlarge, or xxlarge
  instance_type: gp.small

  # Can be rest or grpc
  service_type: rest

version: {version}
"""
