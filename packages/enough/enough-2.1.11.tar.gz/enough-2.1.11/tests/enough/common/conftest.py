import pytest

from enough import settings
from enough.common import ansible_utils, dotenough


def pytest_configure(config):
    config.addinivalue_line("markers", "openstack_integration: mark tests "
                            "which require OpenStack credentials")


@pytest.fixture(scope='session')
def openstack_variables(request):
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    os_variables = ('openstack_flavor', 'openstack_image', 'openstack_network',
                    'network_primary_interface', 'network_secondary_interface',
                    '_provider')
    os_variables = "{%s}" % ', '.join(f'"{x}": {x}' for x in os_variables)
    # Any host could be used
    hostvars = ansible.get_variable(os_variables, 'bind-host')
    hostvars['openstack_provider'] = hostvars.pop('_provider')
    return hostvars


@pytest.fixture
def dot_openstack(tmp_config_dir, request):
    domain = settings.CONFIG_DIR.split('/')[-1]
    dot_openstack = dotenough.DotEnoughOpenStack(settings.CONFIG_DIR, domain)
    dot_openstack.ensure()
    yield dot_openstack
