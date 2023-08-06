from enough.common import host


def test_host_factory(request, tmpdir):
    h = host.host_factory(config_dir=tmpdir, driver='openstack', domain='a.b')
    assert type(h).__name__ == 'HostOpenStack'
