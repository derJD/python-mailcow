# Changelog

### [1.0.3](https://gitlab.der-jd.de/python/mailcow/compare/1.0.2...1.0.3) (2021-02-05)


### Bug Fixes

* **__main__:** Replace expression with if case ([5daad56](https://gitlab.der-jd.de/python/mailcow/commit/5daad56ba482f988e90b4381db003ac997eb0367)), closes [#7](https://gitlab.der-jd.de/python/mailcow/issues/7)
* **config:** Remove else case from case_cfg ([b8c0042](https://gitlab.der-jd.de/python/mailcow/commit/b8c0042d4126e39be6436ed47765b820ee56d2ba)), closes [#16](https://gitlab.der-jd.de/python/mailcow/issues/16)
* **init:** Move response validation to utils ([2cf1346](https://gitlab.der-jd.de/python/mailcow/commit/2cf1346d22c4a8084e32fa4a45d4b40bb2dea458)), closes [#19](https://gitlab.der-jd.de/python/mailcow/issues/19)
* **menu:** Update sections default value ([a7e2060](https://gitlab.der-jd.de/python/mailcow/commit/a7e2060e4c86aed851fad7d6fe8f5e82160edcc7)), closes [#8](https://gitlab.der-jd.de/python/mailcow/issues/8)
* Call sys modules explicetly ([76395ac](https://gitlab.der-jd.de/python/mailcow/commit/76395ac9ec8b117b6c8fd5111242534cc411ae1d)), closes [#10](https://gitlab.der-jd.de/python/mailcow/issues/10)


### Continuous Integration

* **workflow:** skip chore releases and match source ([7ff7d1f](https://gitlab.der-jd.de/python/mailcow/commit/7ff7d1fc51c51fa34a04a5ed6509d2402b25c9c7))


### Styles

* Fix import order ([3a2b7f9](https://gitlab.der-jd.de/python/mailcow/commit/3a2b7f980178cb07d30c0bd088abf616dcdc7272)), closes [#15](https://gitlab.der-jd.de/python/mailcow/issues/15)


### Code Refactoring

* **__init__:** remove obsolete self.method call ([4c97889](https://gitlab.der-jd.de/python/mailcow/commit/4c978891b059c1800c4d6bf9b7c7d9d6e852eb69)), closes [#22](https://gitlab.der-jd.de/python/mailcow/issues/22)
* **__init__:** Rename variables json ([d2ae55c](https://gitlab.der-jd.de/python/mailcow/commit/d2ae55cc514e5da51091c71ff1675a3752d238a3)), closes [#21](https://gitlab.der-jd.de/python/mailcow/issues/21)
* Rename variables help and all ([8a005e2](https://gitlab.der-jd.de/python/mailcow/commit/8a005e2093615ced31250d37bd862bd9e3b0d138)), closes [#11](https://gitlab.der-jd.de/python/mailcow/issues/11)


### Documentation

* Add docstrings ([614a2e4](https://gitlab.der-jd.de/python/mailcow/commit/614a2e419717449a0a0e2c8016a9c46a80148ca1)), closes [#9](https://gitlab.der-jd.de/python/mailcow/issues/9) [#6](https://gitlab.der-jd.de/python/mailcow/issues/6)
* Add missing license string ([2e54d72](https://gitlab.der-jd.de/python/mailcow/commit/2e54d721e5c97cb172a4ce415153c1e027e4081a))

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
