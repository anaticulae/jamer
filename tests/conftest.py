import os

import utila

from tests.resources import REQUIRED_RESOURCES
from tests.resources.update import install_requirements
from tests.resources.update import sync_resources

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

if not 'PYTEST_XDIST_WORKER' in os.environ:
    # master process only
    # ensure to avoid race condition if more than one thread tries to
    # install or use rawmaker

    if 'GENERATE' in os.environ or utila.test.LONGRUN:
        utila.log('install requirements')
        install_requirements()

        # ensure that all test resources exists
        utila.log('synchronize test resources')
        sync_resources()

        # utila.log('extract resources')
        # extract_examples()

for item in REQUIRED_RESOURCES:
    advice = 'run `baw --test=generate` to generate test data'
    msg = f'required test path does not exists: {item}, {advice}'
    assert os.path.exists(item), msg
