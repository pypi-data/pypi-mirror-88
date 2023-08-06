import os
import pytest
import shutil
import yaml

from enough.common import Enough
from tests import make_config_dir, prepare_config_dir


def pytest_addoption(parser):
    parser.addoption(
        "--enough-no-create",
        action="store_true",
        help="Do not run the create step"
    )
    parser.addoption(
        "--enough-no-tests",
        action="store_true",
        help="Do not run the tests step"
    )
    parser.addoption(
        "--enough-no-destroy",
        action="store_true",
        help="Do not run the destroy step"
    )


def pytest_configure(config):
    pass


def get_hosts(session, enough):
    hosts = session.config.getoption("--enough-hosts").split(',')
    updated = enough.service.add_vpn_hosts_if_needed(hosts)
    return (enough.service.get_vpn_host(), updated)


def pytest_sessionstart(session):
    if session.config.getoption("--enough-no-create"):
        return

    if not session.config.getoption("--enough-no-destroy"):
        enough_destroy(session)

    service_directory = session.config.getoption("--enough-service")
    domain = f'{service_directory}.test'
    enough_dot_dir = session.config.cache.makedir('dotenough')
    config_dir = prepare_config_dir(domain, enough_dot_dir)

    e = Enough(config_dir, '.',
               domain=domain,
               driver='openstack',
               inventory=[f'playbooks/{service_directory}/inventory'],
               route_to_internal=False)
    (vpn_host, hosts) = get_hosts(session, e)
    r = e.create_missings(hosts)
    with open(f'{e.config_dir}/inventory/group_vars/all/domain.yml', 'r') as f:
        data = yaml.safe_load(f)
    if len(r) > 0 or data.get('domain') == domain:
        e.heat.create_test_subdomain('enough.community')
    if vpn_host in hosts:
        if not e.vpn_has_credentials():
            bind_host = e.service.service2group.get('bind')[0]
            e.playbook.run([
                '--private-key', f'{e.config_dir}/infrastructure_key',
                '-i', f'playbooks/openvpn/inventory',
                f'--limit={vpn_host},{bind_host},localhost',
                'playbooks/openvpn/conftest-playbook.yml',
            ])
        e.vpn_connect()

    hosts = ','.join(hosts)
    e.playbook.run([
        '--private-key', f'{e.config_dir}/infrastructure_key',
        '-i', f'playbooks/{service_directory}/inventory',
        f'--limit={hosts},localhost',
        f'playbooks/{service_directory}/playbook.yml',
    ])
    if vpn_host and vpn_host in hosts:
        e.vpn_disconnect()


def pytest_runtest_setup(item):
    if item.config.getoption("--enough-no-tests"):
        pytest.skip("--enough-no-tests specified, skipping all tests")


def pytest_sessionfinish(session, exitstatus):
    if not session.config.getoption("--enough-no-destroy"):
        enough_destroy(session)


def enough_destroy(session):
    service_directory = session.config.getoption("--enough-service")
    domain = f'{service_directory}.test'
    enough_dot_dir = session.config.cache.makedir('dotenough')
    config_dir = make_config_dir(domain, enough_dot_dir)
    all_dir = f'{config_dir}/inventory/group_vars/all'
    if not os.path.exists(all_dir):
        os.makedirs(all_dir)
    shutil.copyfile('inventory/group_vars/all/clouds.yml', f'{all_dir}/clouds.yml')
    e = Enough(config_dir, '.',
               domain=domain,
               driver='openstack',
               inventory=[f'playbooks/{service_directory}/inventory'])
    e.destroy()


def pytest_unconfigure(config):
    pass
