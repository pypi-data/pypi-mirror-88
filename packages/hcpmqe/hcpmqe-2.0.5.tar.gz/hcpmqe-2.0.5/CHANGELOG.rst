Release History
===============

**2.0.5 - 2020-11-23**

    *   start and end time are now in ISO 8601 format, added field verification

**2.0.4 - 2020-11-17**

    *   db/csv columns are now sorted by name, to make sure they are uniform across multiple runs
    *   fixed a bug where columns in sqlite3 databases were incorrectly named, occasionally
    *   fixed the start- / end-times (needs to be converted to milliseconds to be accurate)

**2.0.3 - 2020-11-11**

    *   preparation for publishing
    *   corrected the URL for help/documentation

**2.0.2 - 2020-11-10**

    *   configuration file now saved/loaded via menu entries
    *   configuration file is auto-updated when changes happen
    *   logging to file now into hcpmqe.<pid>.log

**2.0.1 - 2020-11-08**

    *   automatically adopts to whatever metadata fields the HCP MQE API
        delivers

    *   allows to restart a canceled or interrupted query

**2.0.0 - 2020-11-03**

    *   complete re-write using tkinter through pySimpleGUI

    *   runs on all major platforms (Linux, Windows, macOS)

**1.0.x releases**

*   1.0.11 - 2014-08-21

    [..]

*   1.0.1 - 2012-09-06

    initial release for Windows only
