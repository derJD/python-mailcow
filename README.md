# python-mailcow

[![PyPI version](https://badge.fury.io/py/python-mailcow.svg)](https://badge.fury.io/py/python-mailcow)
[![PyPI downloads](https://img.shields.io/pypi/dm/python-mailcow)](https://pypi.org/project/python-mailcow/)
[![pylint](https://gitlab.der-jd.de/python/mailcow/-/jobs/artifacts/main/raw/pylint.svg?job=lint:pylint)](#python-mailcow)

`python-mailcow` allows you to interact with the [MailCow](https://mailcow.email/) API. It comes with a cli `mailcow`.
All arguments for the cli are generated by parsing your MailCow instance's OpenApi schema.

See [demo.mailcow.email](https://demo.mailcow.email/api/) as OpenAPI scheme example.

This means that you can `add`, `get`, `edit` and `delete` everything that the MailCow API allows and changes to the API should be usable immediately.

...Famous last words... I know...

BTW: The look and feel of the cli and configuration is inspired by the [python-gitlab](https://github.com/python-gitlab/python-gitlab) project.

## Installation

* from pypi: `pip install python-mailcow`
* from github: `pip install git+https://github.com./derJD/python-mailcow.git`

### Local Build

```sh
git clone https://github.com/derJD/python-mailcow.git
cd python-mailcow
pip install .
```

## Usage

### quick start

* Generate a API token in the MailCow UI
* `mailcow --create-example-config`
* Edit settings in `~/.config/python-mailcow.cfg` to match your MailCow UI
* `mailcow --help` should now show all available options depending on your MailCow API version

### Config

python-mailcow read its settings from `~/.config/python-mailcow.cfg`.
An example configuration looks like this:

```ini
[defaults]
server = mailcow.example.com
ssl_verify = true
timeout = 5

[mailcow.example.com]
url = https://mailcow.example.com
token = 123456-abcde-123456-abcde-123456
```

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `server` | String | Name of the section providing further server information |
| `url`  | String | Base URL (MailCow UI location) for connection ie: `https://demo.mailcow.email` |
| `token` | String | Token for API-Access |
| `ssl_verify` | Boolean | Enable/Disable ssl verification |
| `timeout` | Integer | Connection timeout |

### CLI

If you installed python-mailcow for the first time you may run following
command and change the settings according to your needs:

```bash
mailcow --create-example-config
```

After that you should be able to run commands like these:

* `mailcow alias get --all/--id 5`
* `mailcow alias add --address moep@example.com --goto goto@example.com --no-active`
* `mailcow alias delete --items 5`

**`mailcow --help`**:

```help
usage: test.py [-h] [--create-example-config] [--conf CONF] [--vertical] [--json] [--yaml] [--table] [--debug]
               {alias,app-passwd,bcc,dkim,dkim_duplicate,domain,domain-admin,da-acl,domain-policy,fwdhost,mailbox,oauth2-client,recipient_map,relayhost,resource,syncjob,tls-policy-map,transport,mailq,qitem,fail2ban,pushover,quarantine_notification,user-acl,logs,policy_bl_domain,policy_wl_domain,quarantine,rl-mbox,rl-domain,status,syncjobs,spam-score}
               ...

Interact with mailcows API.

positional arguments:
  {alias,app-passwd,bcc,dkim,dkim_duplicate,domain,domain-admin,da-acl,domain-policy,fwdhost,mailbox,oauth2-client,recipient_map,relayhost,resource,syncjob,tls-policy-map,transport,mailq,qitem,fail2ban,pushover,quarantine_notification,user-acl,logs,policy_bl_domain,policy_wl_domain,quarantine,rl-mbox,rl-domain,status,syncjobs,spam-score}

optional arguments:
  -h, --help            show this help message and exit
  --create-example-config
                        Create configuration file
  --conf CONF, -c CONF  Defaults to: ~/.config/python-mailcow.conf
  --vertical, -v        Print (table) results vertically
  --json, -j            Print results as JSON
  --yaml, -y            Print results as YAML
  --table, -t           Print results as Table
  --debug, -d           Enable debugging
```

## Documentation

* [General documentation](https://der-jd.de/python-mailcow/intro/)
* [CLI usage](https://der-jd.de/python-mailcow/cli/)
* [API usage](https://der-jd.de/python-mailcow/python/)
* [Reference](https://der-jd.de/python-mailcow/reference/mailcow/)

## License

* Code released under [GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0.txt)

## Author

* [derJD](https://github.com/derJD/)
