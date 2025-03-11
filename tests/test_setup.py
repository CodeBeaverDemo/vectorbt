import os
import runpy
import pytest
import shutil

def test_setup_invocation(monkeypatch, tmp_path):
    """Test that setup.py calls setuptools.setup with correct metadata using temporary dummy files."""
    # Create dummy README.md
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test long description")

    # Create dummy vectorbt/_version.py
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '9.9.9'")

    # Capture the arguments passed to setuptools.setup
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change the working directory to the temporary path
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Assert that the setup parameters were as expected
    assert captured.get("name") == "vectorbt"
    assert captured.get("version") == "9.9.9"
    assert captured.get("long_description") == "Test long description"
    assert "install_requires" in captured
    assert "extras_require" in captured
def test_setup_missing_readme(monkeypatch, tmp_path):
    """
    Test that setup.py fails with FileNotFoundError when README.md is missing.
    """
    # Create dummy vectorbt/_version.py so version extraction works
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '1.0.0'")

    # Capture the setup call (should not actually be called)
    import setuptools
    def fake_setup(*args, **kwargs):
        pass
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change working directory to the temporary path and copy the setup.py file
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        with pytest.raises(FileNotFoundError):
            runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

def test_setup_missing_version(monkeypatch, tmp_path):
    """
    Test that setup.py fails with FileNotFoundError when vectorbt/_version.py is missing.
    """
    # Create dummy README.md so the long description is provided
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test long description")

    # Do not create vectorbt/_version.py to simulate the version file missing

    # Change working directory to the temporary path and copy the setup.py file
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        with pytest.raises(FileNotFoundError):
            runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)
def test_setup_invalid_version(monkeypatch, tmp_path):
    """Test that setup.py fails with KeyError when __version__ is not defined in vectorbt/_version.py."""
    # Create dummy README.md to provide long description
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test long description")

    # Create dummy vectorbt/_version.py with missing __version__ definition
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("version = '1.0.0'")

    # Capture the setup call (it should not complete successfully)
    import setuptools
    monkeypatch.setattr(setuptools, "setup", lambda *args, **kwargs: None)

    # Change working directory to the temporary path and copy the setup.py file
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        import pytest
        with pytest.raises(KeyError):
            runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)
def test_setup_syntax_error_in_version(monkeypatch, tmp_path):
    """Test that setup.py fails with SyntaxError when vectorbt/_version.py has invalid syntax."""
    # Create dummy README.md so long description is available
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test long description")

    # Create dummy vectorbt/_version.py with invalid Python code that causes SyntaxError
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("this is not valid Python code")

    # Override setuptools.setup to avoid actual package installation
    import setuptools
    monkeypatch.setattr(setuptools, "setup", lambda *args, **kwargs: None)

    # Change working directory to the temporary path and copy the setup.py file
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        with pytest.raises(SyntaxError):
            runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)
def test_setup_metadata_fields(monkeypatch, tmp_path):
    """Test that setup.py passes complete metadata including author, url, license."""
    # Create dummy README.md
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Full description for metadata test")

    # Create dummy vectorbt/_version.py with a different version for testing
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '2.0.0'")

    # Capture the arguments passed to setuptools.setup
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change the working directory to the temporary path and copy setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Assert that the metadata fields are as expected.
    assert captured.get("name") == "vectorbt"
    assert captured.get("version") == "2.0.0"
    assert captured.get("description") == "Python library for backtesting and analyzing trading strategies at scale"
    assert captured.get("author") == "Oleg Polakow"
    assert captured.get("author_email") == "olegpolakow@gmail.com"
    assert captured.get("url") == "https://github.com/polakowo/vectorbt"
    assert captured.get("license") == "Apache 2.0 with Commons Clause"

def test_setup_package_data(monkeypatch, tmp_path):
    """Test that the package_data field in setup configuration is correct."""
    # Create dummy README.md
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test package data")

    # Create dummy vectorbt/_version.py
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '3.0.0'")

    # Capture the arguments passed to setuptools.setup
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change the working directory to the temporary path and copy setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Assert that package_data is correctly set
    assert captured.get("package_data") == {'vectorbt': ['templates/*.json']}
def test_setup_install_requires(monkeypatch, tmp_path):
    """Test that install_requires field is correctly set in setup configuration."""
    # Create dummy README.md
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test install requires")

    # Create dummy vectorbt/_version.py
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '5.5.5'")

    # Capture setup parameters
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change working directory and run setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    expected_install_requires = [
        'numpy>=1.16.5',
        'pandas',
        'scipy',
        'matplotlib',
        'plotly>=4.12.0',
        'ipywidgets>=7.0.0',
        "numba>=0.53.1, <0.57.0; python_version<'3.10'",
        "numba>=0.56.0, <0.57.0; python_version>='3.10' and python_version<'3.11'",
        "numba>=0.57.0; python_version>='3.11'",
        'dill',
        'tqdm',
        'dateparser',
        'imageio',
        'scikit-learn',
        'schedule',
        'requests',
        'pytz',
        'typing_extensions; python_version < "3.8"',
        'mypy_extensions'
    ]
    assert captured.get("install_requires") == expected_install_requires

def test_setup_extras_require(monkeypatch, tmp_path):
    """Test that extras_require field is correctly set in setup configuration."""
    # Create dummy README.md
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test extras requires")

    # Create dummy vectorbt/_version.py with a version for testing extras_require
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '6.6.6'")

    # Capture setup parameters
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change working directory and run setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    expected_extras_require = {
        'full': [
            'yfinance>=0.2.22',
            'python-binance',
            'ccxt>=4.0.14',
            'alpaca-py',
            'ray>=1.4.1',
            'ta',
            'pandas_ta',
            'TA-Lib',
            'python-telegram-bot>=13.4,<20.0',
            'quantstats>=0.0.37'
        ],
        'cov': [
            'pytest',
            'pytest-cov',
            'codecov'
        ]
    }
    assert captured.get("extras_require") == expected_extras_require

def test_setup_version_exec_error(monkeypatch, tmp_path):
    """Test that setup.py fails with ValueError when _version.py raises an error during execution."""
    # Create dummy README.md
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test version exec error")

    # Create dummy vectorbt/_version.py that raises ValueError when executed
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("raise ValueError('Version file error')")

    # Override setuptools.setup to avoid actual package installation
    import setuptools
    monkeypatch.setattr(setuptools, "setup", lambda *args, **kwargs: None)

    # Change working directory and copy setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        import pytest
        with pytest.raises(ValueError, match="Version file error"):
            runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)
def test_setup_empty_readme(monkeypatch, tmp_path):
    """Test that setup.py correctly sets long_description to an empty string when README.md is empty."""
    # Create an empty README.md file
    readme_file = tmp_path / "README.md"
    readme_file.write_text("")

    # Create dummy vectorbt/_version.py
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '8.8.8'")

    # Capture the setup arguments passed to setuptools.setup
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change working directory to the temporary path and copy setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Assert that long_description is empty
    assert captured.get("long_description") == ""

def test_setup_called_once(monkeypatch, tmp_path):
    """Test that setuptools.setup is called exactly once during setup.py execution."""
    # Create dummy README.md and vectorbt/_version.py
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Call count test")

    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '10.10.10'")

    # Initialize a counter to track calls to setup
    call_count = [0]
    def fake_setup(*args, **kwargs):
        call_count[0] += 1

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change working directory to the temporary path and copy setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Assert that setuptools.setup was called exactly once
    assert call_count[0] == 1
def test_setup_python_requires_and_classifiers(monkeypatch, tmp_path):
    """Test that python_requires and classifiers are correctly set in setup configuration."""
    # Create dummy README.md
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Python requires and classifiers test")

    # Create dummy vectorbt/_version.py with version info
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '11.11.11'")

    # Capture the arguments passed to setuptools.setup
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change the working directory to the temporary path and copy setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Assert that python_requires and classifiers are as expected
    assert captured.get("python_requires") == ">=3.6"
    assert isinstance(captured.get("classifiers"), list)
    assert "Programming Language :: Python :: 3.12" in captured.get("classifiers", [])

def test_setup_with_package_and_init(monkeypatch, tmp_path):
    """Test that setup.py includes packages discovered by find_packages when __init__.py is present."""
    # Create dummy README.md
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Test package with __init__.py")

    # Create dummy vectorbt package with __init__.py and _version.py
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    init_file = vectorbt_dir / "__init__.py"
    init_file.write_text("")
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '12.12.12'")

    # Capture the arguments passed to setuptools.setup
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change the working directory to the temporary path and copy setup.py
    import os, runpy, shutil
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Check that 'packages' is in captured and that it contains 'vectorbt'
    packages = captured.get("packages", [])
    assert isinstance(packages, list)
    assert "vectorbt" in packages
def test_setup_multiline_readme(monkeypatch, tmp_path):
    """Test that setup.py correctly reads a multi-line README.md file."""
    multiline = "Line1\nLine2\nLine3"
    readme_file = tmp_path / "README.md"
    readme_file.write_text(multiline)

    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '13.0.0'")

    # Capture the arguments passed to setuptools.setup
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import os, runpy, shutil, setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    # Change directory and run setup.py in the temporary path
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    assert captured.get("long_description") == multiline

def test_setup_additional_version_metadata(monkeypatch, tmp_path):
    """Test that setup.py works correctly when _version.py contains extra metadata."""
    readme_file = tmp_path / "README.md"
    readme_file.write_text("Extra metadata test")

    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '14.14.14'\n__build__ = 'beta'")

    # Capture the arguments passed to setuptools.setup
    captured = {}
    def fake_setup(*args, **kwargs):
        captured.update(kwargs)

    import os, runpy, shutil, setuptools
    monkeypatch.setattr(setuptools, "setup", fake_setup)

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Only __version__ should be used for version
    assert captured.get("version") == "14.14.14"
def test_setup_readme_encoding_error(monkeypatch, tmp_path):
    """Test that setup.py ignores encoding errors in README.md and uses an empty long description."""
    # Write a README.md file containing invalid UTF-8 bytes.
    readme_file = tmp_path / "README.md"
    readme_file.write_bytes(b'\xff')

    # Create dummy vectorbt/_version.py with a valid version.
    vectorbt_dir = tmp_path / "vectorbt"
    vectorbt_dir.mkdir()
    version_file = vectorbt_dir / "_version.py"
    version_file.write_text("__version__ = '15.15.15'")

    # Capture the setup arguments passed to setuptools.setup.
    captured = {}
    import os, runpy, shutil, setuptools
    monkeypatch.setattr(setuptools, "setup", lambda *args, **kwargs: captured.update(kwargs))

    # Change working directory to the temporary path and copy setup.py.
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    src_setup = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
    shutil.copy(src_setup, tmp_path / "setup.py")
    try:
        runpy.run_path(str(tmp_path / "setup.py"))
    finally:
        os.chdir(old_cwd)

    # Since the invalid bytes are ignored, the long_description should be empty.
    assert captured.get("long_description") == ""