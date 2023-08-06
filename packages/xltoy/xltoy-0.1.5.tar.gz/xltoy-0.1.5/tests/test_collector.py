import xltoy
from xltoy.collector import Collector
import os
import pytest

base_data_url = os.path.join(os.path.dirname(os.path.dirname(xltoy.__file__)),'data')



def coll(url):
    url=os.path.join(base_data_url,url)
    return Collector(url)


@pytest.mark.collector
@pytest.mark.parametrize("f", [src for src in list(os.walk(base_data_url))[0][2]])
def test_injestion(f):
    coll(f)
