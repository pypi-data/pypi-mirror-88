import json
from io import StringIO

import yaml
from click.testing import CliRunner

from tktl import main
from tktl.cli import get


def test_get(logged_in_context):
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(main.get_commands)
    assert result.exit_code == 0
    assert "deployments   Get deployment resources\n" in result.output
    assert "repositories  Get repository resources\n" in result.output
    assert "endpoints     Get endpoint resources\n" in result.output


def test_get_deployments(logged_in_context):
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(get.get_deployment_by_id)
    assert result.exit_code == 0
    assert "9b503d88-5f49-46d4-806a-aed3134ba973" in result.output
    assert "437445ed-edc1-4cb9-ad4f-4ef2af086eae" in result.output
    assert "f91b6781-405b-43df-b825-956627019c0b" in result.output
    as_io = StringIO(result.output)
    lines = as_io.readlines()
    assert len(lines) >= 4


def test_get_deployments_with_options(logged_in_context):
    runner = CliRunner()
    result_with_id = runner.invoke(
        get.get_deployment_by_id, "9b503d88-5f49-46d4-806a-aed3134ba973"
    )
    assert "refs/heads/main @ 3e2dd56" in result_with_id.output
    as_io = StringIO(result_with_id.output)
    lines = as_io.readlines()
    assert len(lines) == 2


def test_json_resources(logged_in_context):
    runner = CliRunner()
    for command in [
        get.get_deployment_by_id,
        get.get_repository_by_id,
        get.get_endpoint_by_id,
    ]:
        result = runner.invoke(command, ["-O", "json", "-a"])
        assert result.exit_code == 0
        as_io = StringIO(result.output)
        lines = as_io.read()
        loaded = json.loads(lines)
        assert isinstance(loaded, list)
        for item in loaded:
            assert "id" in item.keys()


def test_yaml_resources(logged_in_context):
    runner = CliRunner()
    for command in [
        get.get_deployment_by_id,
        get.get_repository_by_id,
        get.get_endpoint_by_id,
    ]:
        result = runner.invoke(command, ["-O", "yaml", "-a"])
        assert result.exit_code == 0
        as_io = StringIO(result.output)
        lines = as_io.read()
        loaded = [l for l in yaml.safe_load_all(lines)]
        assert len(loaded) >= 3
        assert all(["id" in k.keys() for k in loaded])
