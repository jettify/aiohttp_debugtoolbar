import platform
import sys
import time

import pytest


@pytest.mark.skipif(
    not sys.platform.startswith("linux") or platform.python_implementation() == "PyPy",
    reason="Unreliable",
)
def test_import_time(pytester: pytest.Pytester) -> None:
    """Check that importing aiohttp-debugtoolbar doesn't take too long.
    Obviously, the time may vary on different machines and may need to be adjusted
    from time to time, but this should provide an early warning if something is
    added that significantly increases import time.
    """
    best_time_ms = 1000
    cmd = "import time, timeit; time.sleep(1); print(int(timeit.timeit('import aiohttp_debugtoolbar', number=1) * 1000))"
    for _ in range(3):
        time.sleep(1)
        r = pytester.run(sys.executable, "-We", "-X", "importtime", "-c", cmd)

        print(r.stderr.str())
        assert not r.stderr.str()
        runtime_ms = int(r.stdout.str())
        if runtime_ms < best_time_ms:
            best_time_ms = runtime_ms

    assert best_time_ms < 200
