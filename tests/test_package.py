import seem_block_system
from seem_block_system.cli import main


def test_import_version():
    assert seem_block_system.__version__ == "0.1.0"


def test_cli_demo_exits_zero():
    assert main(["--steps", "30", "--dim", "32", "--seed", "0"]) == 0


def test_cli_json_exits_zero():
    assert main(["--json", "--steps", "10", "--dim", "16"]) == 0
