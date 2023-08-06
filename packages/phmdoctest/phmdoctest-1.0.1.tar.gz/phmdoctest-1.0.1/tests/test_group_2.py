"""Second group of pytest test cases for phmdoctest."""
import phmdoctest
import phmdoctest.cases
import phmdoctest.main
import phmdoctest.simulator
import verify


def test_skip_first():
    """Verify --skip FIRST."""
    command = (
        'phmdoctest doc/example2.md --skip "Python 3.7" -sFIRST'
        ' --skip LAST --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py3         9  skip-code     "FIRST"' in stdout
    assert 'FIRST         9' in stdout


def test_skip_second():
    """Verify --skip SECOND."""
    command = (
        'phmdoctest doc/example2.md --skip SECOND'
        ' --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py3        20  skip-code    "SECOND"' in stdout
    assert 'SECOND        20' in stdout


def test_skip_first_session():
    """Verify --skip FIRST skips a session block."""
    command = (
        'phmdoctest tests/twentysix_session_blocks.md -sFIRST'
        ' --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'pycon        3  skip-session  "FIRST"' in stdout
    assert 'FIRST         3' in stdout


def test_skip_second_session():
    """Verify --skip SECOND skips a session block."""
    command = (
        'phmdoctest tests/twentysix_session_blocks.md -sSECOND'
        ' --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py           8  skip-session  "SECOND"' in stdout
    assert 'SECOND        8' in stdout


def test_skip_second_when_only_one():
    """Verify --skip SECOND selects no block when only 1 code block."""
    command = (
        'phmdoctest tests/one_code_block.md -sFIRST'
        ' --skip SECOND --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    assert 'def test_nothing_passes()' in simulator_status.outfile
    assert 'SECOND\n' in simulator_status.runner_status.stdout


def test_skip_second_when_more_than_one():
    """Verify --skip SECOND when more than 1 code block."""
    command = (
        'phmdoctest doc/example2.md -sFIRST'
        ' --skip SECOND --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py3        20  skip-code    "SECOND"' in stdout
    assert 'SECOND        20' in stdout


def test_skip_code_that_has_no_output_block():
    """Skip code with no output block."""
    command = (
        'phmdoctest doc/example2.md --skip SECOND --skip="while a < 1000:"'
        ' --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py3        20  skip-code    "SECOND"' in stdout
    assert 'py3        37  skip-code    "while a < 1000:"' in stdout
    assert 'SECOND           20' in stdout
    assert 'while a < 1000:  37' in stdout


def test_skip_matches_start_of_contents():
    """Skip pattern matching first characters of code block."""
    command = (
        'phmdoctest doc/example2.md --skip SECOND --skip="Python 3.7"'
        '  --skip="words =" --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-vv']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'words =       44' in stdout


def test_multiple_skips_report():
    """More than one skip applied to the same Python code block."""
    command = 'phmdoctest doc/example2.md --report -sprint -slen'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert '                            "len"' in stdout
    assert 'len           44' in stdout


def test_one_skip_many_matches():
    """Every block matches the skip pattern presenting multi-line report."""
    command = (
        'phmdoctest tests/twentysix_session_blocks.md'
        ' --skip=">>>" --report'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    stdout = simulator_status.runner_status.stdout

    with open('tests/twentysix_report.txt', 'r', encoding='utf-8') as f:
        want = f.read()
    verify.a_and_b_are_the_same(want, stdout)
