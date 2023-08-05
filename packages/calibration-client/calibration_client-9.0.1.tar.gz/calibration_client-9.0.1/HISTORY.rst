History
-------

v9.0.1 (8 December 2020)
++++++++++++++++++++++++
- Update external dependencies
- Adapt detectors APIs tests to changes in performed on CalCat service

  - Adapt to immutable identifiers in CalCat detectors' model.
  - Adapt to order in which Physical Detector Units are returned.

v9.0.0 (15 July 2020)
+++++++++++++++++++++
- Rename strategy 'closest_by_pdu' to 'pdu_closest_by_time'
- Rename strategy 'exactly_contained_by_pdu' to 'pdu_prior_in_time'
- Rename strategy 'closest_by_detector' to 'detector_closest_by_time'

v8.0.1 (29 June 2020)
+++++++++++++++++++++
- Reformat code
- Solve all pycodestyle findings

v8.0.0 (29 June 2020)
+++++++++++++++++++++
- Update CalCat APIs from version 1 to version 2
- Update APIs tests to validate CalCat version 2 APIs successfully
- Update retrieve and inject APIs to take into account the return strategy:

  - `closest_by_pdu`
  - `exactly_contained_by_pdu`
  - `closest_by_detector`
  - Default value is: `closest_by_detector`

- Add new APIs:

  - PhysicalDetectorUnitApi:

    - `get_all_physical_detector_units_by_detector_id_api`
    - `get_all_physical_detector_units_by_det_and_krbda_api`

  - DetectorApi:

    - `create_detector_api`
    - `delete_detector_api`
    - `update_detector_api`
    - `get_detector_by_id_api`
    - `get_all_detectors_by_name_api`
    - `get_all_detectors_by_identifier_api`

  - ReportApi:
  
    - `create_report_api`
    - `delete_report_api`
    - `update_report_api`
    - `get_report_by_id_api`
    - `get_all_reports_by_name_api`
    - `get_all_reports_by_name_and_file_path_api`
- Upgrade internal libraries versions in use

v7.0.0 (8 June 2020)
++++++++++++++++++++
- Improve README documentation
- Improve setup.py
- Upgrade tests to use pytest
- Upgrade internal libraries versions in use

v6.1.3 (21 August 2019)
+++++++++++++++++++++++
- Improve setup.py so that information in pypi.org is better rendered
- Upgrade oauth2_xfel_client library to version 5.1.1

v6.1.2 (16 August 2019)
+++++++++++++++++++++++
- Add gitlab-ci
- Solve issues in tests when executed in gitlab-ci due to long hostname

v6.1.1 (12 August 2019)
+++++++++++++++++++++++
- Minor tests related code improvements

v6.1.0 (6 August 2019)
++++++++++++++++++++++
- Update dependencies versions

v6.0.0 (6 August 2019)
++++++++++++++++++++++
- Applied change of strategy in the `retrieve_calibration_constant_version` API as discussed on MR10.

 - With the applied changes all conditions in the boundaries will be taken into account... and from them, the respective Calibration Constant Version `begin_at` with the closest ABSOLUTE (past or future) datetime interval to the desired `event_at` will be returned.
 - Please note that the API `retrieve_all_calibration_constant_versions` will return all the matching Calibration Constant Versions order by the closest ABSOLUTE datetime interval to the desired `event_at`

- Added new methods to calibration_client to return.

 - APIs:

  - `calibration_api -> get_all_calibration_constants_by_conditions_api` to get all avaialble calibration constants of several conditions
  - `calibration_constant_api -> get_closest_calibration_constant_version_api` to get the closest avaialble (smaller distance between provided event_at and CCV.begin_at) calibration constant version from several calibration constants
  - `calibration_constant_api -> get_all_calibration_constant_versions_api` to get all avaialble calibration constant versions from several calibration constants

 - Modules:

  - `calibration_constant -> get_all_by_conditions` to get all calibration constants from all matching conditions
  - `calibration_constant_version -> get_closest_by_time` that user API `get_closest_calibration_constant_version_api` method
  - `calibration_constant_version -> get_all_versions` that user API `get_all_calibration_constant_version_api` method

 - Statically available:

  - `search_possible_conditions_from_dict` to get all avaialble matching conditions ordered by closest date
  - `retrieve_all_calibration_constant_versions` to return all avaialble calibration constant versions of all avaialble matching conditions

v5.0.1 (6 December 2018)
++++++++++++++++++++++++
- Hotfix for returning newest CalibrationConstant by default

v5.0.0 (21 December 2017)
+++++++++++++++++++++++++
- Upgrade oauth2_client library to oauth2_xfel_client version 5.0.0
- Upgrade oauthlib library to version 2.0.6

v4.0.0 (1 November 2017)
++++++++++++++++++++++++
- Upgrade library to contain dependent libraries
- Update dependencies versions in use
- Update descriptions

v3.0.0 (7 March 2017)
+++++++++++++++++++++
- Separate this Python library from the KaraboDevices code.
- Clean code and remove all references to Karabo.
- Set up new project under ITDM group in Gitlab.

v2.0.0 (4 November 2016)
++++++++++++++++++++++++
- Update library dependencies
- Integrate this library with Karabo 2.0

v1.0.0 (4 December 2015)
++++++++++++++++++++++++
- First official release

v0.0.1 (20 June 2015)
+++++++++++++++++++++
- Initial code
