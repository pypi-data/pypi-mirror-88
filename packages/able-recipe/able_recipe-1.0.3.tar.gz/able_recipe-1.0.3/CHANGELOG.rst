Changelog
=========

1.0.3
-----

* Changed package version generation:

  - Version is set during the build, from the git tag
  - Development (git master) version is always "0.0.0"
* Added ATT MTU changing method and callback
* Added MTU changing example
* Fixed:

  - set `BluetoothDispatcher.gatt` attribute in GATT connection handler,
    to avoid possible `on_connection_state_change()` call before  the `gatt` attribute is set
