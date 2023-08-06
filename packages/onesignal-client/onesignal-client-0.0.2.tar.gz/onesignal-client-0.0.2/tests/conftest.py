import os

import onesignal
import pytest


@pytest.fixture(scope='module')
def client():
    # Put your own credentials here
    return onesignal.OneSignal(
        os.environ['ONESIGNAL_API_KEY'],
        os.environ['ONESIGNAL_REST_API_KEY']
    )
