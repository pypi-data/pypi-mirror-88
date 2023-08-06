*************
Configuration
*************

Configuration file location
===========================

Pebble’s default configuration file is looked for, by default, under the
path ``$XDG_CONFIG_HOME/pebble/config``.

Another location may be specified using the ``-c`` or ``--config``
option.

In any case, the configuration file to use, be it the default one or one
specified with the ``-c`` option, must exist when ``pbl`` is called.
Pebble will *not* create a configuration file by itself.


Configuration file syntax
=========================

The configuration file’s general syntax is that of ``.ini`` files, as
supported by Python’s :py:mod:`configparser` module.

Briefly, the configuration file is organized into *sections* which start
by a bracket-enclosed header and contain key-value pairs.

You can use either a colon (``:``) or an equal sign (``=``) to separate
keys and values. Leading and trailing whitespaces are ignored, as well
as lines starting with either a semi-colon (``;``) or a number sign
(``#``).


Section types
=============

Pebble’s configuration file may contain two types of section: *vault
sections* and *server sections*.

.. _vault-sections:

Vault sections
--------------

A vault section describes a Passman vault. At a minimum, it must
provides the following informations:

* the hostname of the Nextcloud server to connect to;
* the username to connect with;
* the password associated with that username;
* the name of the vault, as chosen when creating the vault in Passman.

Those informations should be specified with the ``host``, ``user``,
``password``, and ``vault`` keys, respectively.

.. note::

   Note that the password does not need to be the user’s main Nextcloud
   password: it can be an *application password* specifically created to
   be used by Pebble. This is actually recommended.

The ``password`` key may be replaced by a ``password_command`` key,
whose value should be a command to be executed by Pebble and which
should print the password on its standard output.

If neither ``password`` nor ``password_command`` is specified, Pebble
will interactively ask for the password.

The three keys ``host``, ``user``, and ``password`` (or
``password_command``) may be replaced by a single ``server`` key, whose
value should refer to the name of a :ref:`server section
<server-sections>`.

Two optional keys control the caching behavior of Pebble:

* If ``nocache`` is set to ``true``, all caching is disabled. Pebble
  will then always download the vault’s contents from the server upon
  each invocation, and said contents will never be locally written to
  disks.
* The ``max_age`` key indicates for how long the cache is valid. The
  value should be a duration expressed either in seconds (without any
  units), or in minutes, hours, or days (if the value is suffixed with
  ``m``, ``h``, or ``d`` respectively). Pebble will refresh its cache if
  it is older than the specified value. The default ``max_age`` value is
  one day.

.. note::

   Setting ``max_age`` to 0 is not the same thing as disabling the cache
   by setting ``nocache`` to ``true``, as the vault’s contents would
   still be written to the disk.

The name of a vault section can be chosen freely. Pebble expects to find
one vault section named ``default``, and will use this section by
default. The ``-s`` or ``--section`` option may be used to chose another
section, by giving it as an argument the name of the section to use.


.. _server-sections:

Server sections
---------------

A server section provides the necessary informations to connect to a
given Nextcloud server; the use of such a section is optional, as those
informations may also be provided directly within a vault section as
described above. The purpose of a server section is to avoid duplicating
information when you have several vaults on a single server.

A server section should contain at least a ``host`` key indicating the
server to connect to and a ``user`` key indicating the username to
connect with. It may also contain either a ``password`` or a
``password_command`` key, otherwise the password will be asked for
interactively.

The name of a server section can be chosen freely. It has to match the
value of a ``server`` key in a vault section.


Examples
========

Here is the simplest configuration file, with only one vault section set
as a the default section:

.. code-block:: ini

   [default]
   host: cloud.example.org
   user: alice
   password: XXXXXX
   vault: MyVault

Here is a configuration with three vaults, two of them hosted on the
same server (whose parameters are set in a shared server section):

.. code-block:: ini

   # First vault, used by default
   [default]
   server: myserver
   vault: MyVault

   # Second vault, selected by '-s secondary'
   [secondary]
   server: myserver
   vault: MySecondaryVault
   max_age: 7d

   # Third vault, selected by '-s employer'
   [employer]
   host: employer.example.com
   user: alice
   password_command: get-password alice@employer@example.com
   vault: Main
   nocache: true

   # Server settings for the first two vaults
   [myserver]
   host: cloud.example.org
   user: alice
   password: XXXXXX
