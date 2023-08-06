RUN pip install python-openstackclient python-heatclient # this is not necessary to run tests but to cleanup leftovers when tests fail
RUN pip install tox
# BEGIN dependencies playbooks/infrastructure/test-pipelining.yml
RUN apt-get install -y python
# END dependencies playbooks/infrastructure/test-pipelining.yml
# BEGIN dependencies of test/ssh
RUN pip install tox yq
RUN apt-get install -y jq
# END dependencies of test/ssh
RUN git init
COPY requirements.txt requirements-dev.txt tox.ini setup.cfg setup.py README.md /opt/
RUN tox --notest
