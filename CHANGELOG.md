# Changelog

## [1.0.2](https://gitlab.der-jd.de/python/mailcow/compare/1.0.1...1.0.2) (2021-02-03)


### Bug Fixes

* **cli:** Remove obsolete custom argument ([1dc3b39](https://gitlab.der-jd.de/python/mailcow/commit/1dc3b39d9449c7775c3c00c9bca736328eb4a798)), closes [#3956](https://gitlab.der-jd.de/python/mailcow/issues/3956)

## Version 1.0.1

* Add Makefile
* Add CI job for linting
* Add pylint badge to README
* Update upload command in publish ci job
* Fix url in setup.py
* Fix dev-version string

## Version 1.0.0

### Features

* Add Class MailCow()
  * Add Method getOpenApiSchema()
  * Add Method endpoint()
  * Add Method deleteRequest()
  * Add Method getRequest()
  * Add Method addRequest()
  * Add Method editRequest()
  * Add Method as_json()
  * Add Method as_yaml()
  * Add Method as_table()
* Add config Function set_config_parser()
* Add config Decorator expand_path()
* Add config Function find_cfg()
* Add config Function load_cfg()
* Add config Function create_cfg()
* Add menu Function menu()
* Add menu Function build_argument()
* Add utils Function chomp()
* Add utils Function debug_mailcow()
* Add utils Function debug_msg()
* Add utils Function build_attributes()
* Add utils Function parse_fields()
* Add utils Function prepare_getRequest()
* Add utils Function filterOpenApiPath()
* Add utils Function describeOpenApiPath()
* Add utils Function getOpenApiParameters()
* Add utils Function etOpenApiProperties()

* Add README
* Add CONTRIBUTING
* Add License
* Add setup.py
