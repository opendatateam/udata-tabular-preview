# Changelog

## Current (in progress)

- Nothing yet

## 4.0.1 (2024-10-03)

- Remove useless max size setting [#41](https://github.com/opendatateam/udata-tabular-preview/pull/41)
- Improve explore button logic [#43](https://github.com/opendatateam/udata-tabular-preview/pull/43)

## 4.0.0 (2024-05-06)

- :warning: Plug udata-tabular-preview to tabular api and decomission of csvapi [#33](https://github.com/opendatateam/udata-tabular-preview/pull/33)
- Migrate to Python 3.11 following `udata` dependencies upgrade [#35](https://github.com/opendatateam/udata-tabular-preview/pull/35)
- Don't show preview if parsing has failed [#36](https://github.com/opendatateam/udata-tabular-preview/pull/36)
- Display the latest date of the preview [#37](https://github.com/opendatateam/udata-tabular-preview/pull/37)
- Set long description content type to markdown in dist [#39](https://github.com/opendatateam/udata-tabular-preview/pull/39)
- Publish .dev version on pypi [#40](https://github.com/opendatateam/udata-tabular-preview/pull/40)

## 4.0.0 (2024-03-22)

- Connect preview with hydra and remove csvapi + styles for preview [#32](https://github.com/opendatateam/udata-tabular-preview/pull/33)
 Current (in progress)
- Use pagination from package `@etalab/data.gouv.fr-components` [#34](https://github.com/opendatateam/udata-tabular-preview/pull/34)

## 3.1.0 (2024-01-23)

- Use either of analysis or header check mime [#32](https://github.com/opendatateam/udata-tabular-preview/pull/32)

## 3.0.4 (2024-01-09)

- Update mongoDB in CI [#25](https://github.com/opendatateam/udata-tabular-preview/pull/25)
- Use analysis extras on top of check:headers [#30](https://github.com/opendatateam/udata-tabular-preview/pull/30)

## 3.0.3 (2023-03-07)

- Specify version in static [#27](https://github.com/opendatateam/udata-tabular-preview/pull/27)
- Add python translations logic [#26](https://github.com/opendatateam/udata-tabular-preview/pull/26)

## 3.0.2 (2023-03-02)

- Add data structure component and explore button for hook `dataset.display.explore-button` [#19](https://github.com/opendatateam/udata-tabular-preview/pull/19)

## 3.0.1 (2023-02-06)

- Add sort to exploration preview component [#20](https://github.com/opendatateam/udata-tabular-preview/pull/20)
- Fix setuptools version used in CI [#23](https://github.com/opendatateam/udata-tabular-preview/pull/23)
- Add pagination to exploration preview component [#21](https://github.com/opendatateam/udata-tabular-preview/pull/21)

## 3.0.0 (2023-01-18)

- :warning: **Breaking change** Change preview behaviour [#14](https://github.com/opendatateam/udata-tabular-preview/pull/14)
    - remove `preview` route
    - add exploration preview Vue component
    - add explorable_ressources metadata
- Replace mongo legacy image in CI [#13](https://github.com/opendatateam/udata-tabular-preview/pull/13)
- Update json5 to fix CVE-2022-46175 [#16](https://github.com/opendatateam/udata-tabular-preview/pull/16)

## 2.0.3 (2022-07-11)

- Remove legacy manifest logic and dataexplorer integration [#12](https://github.com/opendatateam/udata-tabular-preview/pull/12)

## 2.0.2 (2020-10-16)

- Add a setting for SUPPORTED_MIME_TYPES [#9](https://github.com/opendatateam/udata-tabular-preview/pull/9)

## 2.0.1 (2020-06-17)

- Use extras attributes to enable preview [#8](https://github.com/opendatateam/udata-tabular-preview/pull/8)

## 2.0.0 (2020-03-11)

- Migrate to Python3 [#5](https://github.com/opendatateam/udata-tabular-preview/pull/5)

## 1.0.0 (2018-10-02)

Initial release
