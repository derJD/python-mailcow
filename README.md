# python-mailcow

[![PyPI version](https://badge.fury.io/py/python-mailcow.svg)](https://badge.fury.io/py/python-mailcow)
[![pylint](https://gitlab.der-jd.de/python/mailcow/-/jobs/artifacts/main/raw/pylint.svg?job=test:pylint)](#python-mailcow)

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

* `git checkout main`
* `python setup.py sdist`
* `pip install dist/python-mailcow-9999.999.99.dev9.tar.gz`

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

**`mailcow alias add --help`**:

```help
usage: mailcow alias add [-h] [--active] [--address ADDRESS] [--goto GOTO] [--goto_ham] [--goto_null] [--goto_spam] [--sogo_visible]

optional arguments:
  -h, --help            show this help message and exit
  --active, --no-active
                        is alias active or not
  --address ADDRESS     alias address, for catchall use "@domain.tld"
  --goto GOTO           destination address, comma separated
  --goto_ham, --no-goto_ham
                        learn as ham
  --goto_null, --no-goto_null
                        silently ignore
  --goto_spam, --no-goto_spam
                        learn as spam
  --sogo_visible, --no-sogo_visible
                        toggle visibility in SoGo
```

Editing alias' active status and visibility should look like this:

```bash
mailcow alias edit --items 78 --active --sogo_visible
+---------+----------------------------------------------------------------------------------------+-------------------------------------------+
|   type  |                                          log                                           |                    msg                    |
+---------+----------------------------------------------------------------------------------------+-------------------------------------------+
| success | ['mailbox', 'edit', 'alias', {'id': ['78'], 'active': '1', 'sogo_visible': '1'}, None] | ['alias_modified', 'example@example.com'] |
+---------+----------------------------------------------------------------------------------------+-------------------------------------------+
```

### python

#### **Class `MailCow()`**

Connect to MailCow instance defined in config file and
interact via API Requests

`MailCow()` takes the same arguments as listed in [Config](#config) and one additional optional argument:

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `conf` | String | Path to config file |

Every argument is optional and accessible as attribute.

| Attributes | Type | Description |
| ---------- | ---- | ----------- |
| `data` | dict/None | Store API responses here and display response via methods `as_json`, `as_yaml`, `as_table` |
| `json` | dict/None | Store payload for API requests here |
| `request_url` | string | `{url}/api/v1` |
| `session` | object | Session used for requests |
| `schema` | dict | Schema retrieved from MailCows OpenApi |
| `endpoints` | dict | All endpoints from filtered from `schema` |

#### **Method `endpoint(endpoint)`**

Returns specific endpoint as `dict` or `None`

| Argument | Type | Description |
| -------- | ---- | ----------- |
| endpoint | string | Name of the endpoint. ie `"alias"` or `"mailbox"` |

#### **Method `deleteRequest(section, items)`**

Send delete request

| Argument | Type | Description |
| -------- | ---- | ----------- |
| section | string | section aka last part of the url. ie `alias` |
| items | list | List of items to delete. ie: `['5']` |

#### **Method `getRequest(section)`**

Send get request

| Argument | Type | Description |
| -------- | ---- | ----------- |
| section | string | section aka last part of the url. ie `alias/all` |

#### **Method `addRequest(section, json)`**

Send add request

| Argument | Type | Description |
| -------- | ---- | ----------- |
| section | string | section aka last part of the url. ie `alias` |
| json | dict | attributes send as payload. ie `{'active': '1', 'address': 'example@example.com'}` |

#### **Method `editRequest(section, items, attr, action)`**

Send edit request

| Argument | Type | Description |
| -------- | ---- | ----------- |
| section | string | section aka last part of the url. ie `alias` |
| items | list | items send as payload .ie `['5']` or `['domain.tld']` |
| attr | dict | attributes send as payload. ie `{'active': '1', 'address': 'example@example.com'}` |
| action | string | action send as payload. only needed by `mailq` section .ie `flush` |

#### **Method `as_json()`**

Return `data` as json

#### **Method `as_yaml()`**

Return `data` as yaml

#### **Method `as_table(vertical)`**

Return `data` as table. `vertical` expects boolean

| Argument | Type | Description |
| -------- | ---- | ----------- |
| vertical | bool | Enable/Disable vertical print of `data`. Defaults to `False` |

#### **Example**

```python
moo = MailCow()
logs = moo.getRequest(section='logs/api/5')
moo.data = logs
print(moo.as_table())
# returns:
# +------------+----------------------------------+--------+-----------+------+
# |    time    |               uri                | method |   remote  | data |
# +------------+----------------------------------+--------+-----------+------+
# | 1611102437 |      /api/v1/get/logs/api/5      |  GET   | xx.x.xx.x |      |
# | 1611096182 | /api/v1/get/rl-mbox/xx@examp.com |  GET   | xx.x.xx.x |      |
# | 1611087846 | /api/v1/get/rl-mbox/xx@examp.com |  GET   | xx.x.xx.x |      |
# | 1611087808 |    /api/v1/get/logs/dovecot/5    |  GET   | xx.x.xx.x |      |
# | 1611087797 | /api/v1/get/syncjobs/all/no_log  |  GET   | xx.x.xx.x |      |
# +------------+----------------------------------+--------+-----------+------+
```

## License

* Code released under [GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0.txt)

## Author

* [derJD](https://github.com/derJD/)
