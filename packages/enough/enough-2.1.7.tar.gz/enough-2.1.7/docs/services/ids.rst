.. _ids:

Intrusion Detection System
==========================

The `Wazuh <http://wazuh.com/>`_ Intrusion Detection System watches
over all hosts and will report problems to the `ids@example.com` mail
address.

The wazuh API user and password must be created to allow the agents
to register on the server. For instance:

.. code::

    $ cat ~/.enough/example.com/group_vars/all/wazuh.yml
    ---
    wazuh_api_username: apiuser
    wazuh_api_password: .S3cur3Pa75w0rd-#
    wazuh_mailto: contact@enough.community
    wazuh_email_from: contact@enough.community

.. note::

   The password must obey the `wazuh requirements <https://github.com/wazuh/wazuh/blob/79e4d3fd09b28c65fb7990148821b47742d867c4/framework/wazuh/security.py#L22>`__ to be valid. They are complex and the best way
   to make sure is to try the regular expression manually.

The service is created on the host specified by the `--host` argument:

.. code::

    $ enough --domain example.com service create --host wazuh-host wazuh
