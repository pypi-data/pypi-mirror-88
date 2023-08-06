# DR Files

Read and convert MECHBASE files (.dr) to known file formats

## MECHBASE

[MECHBASE](https://arpedon.com/products/mechbase/)® is a complete preventive solution that was developed by [Arpedon, P.C.](https://arpedon.com/), in order to help you store and trend your equipment status.

## MECHBASE files format

MECHBASE files have the following structure:

* 2 bytes - the size of the header in bytes, in little-endian short integer format
* next N bytes - the header, in [this protobuf format](pb/headers_pb2.proto)
* remaining bytes - the values of the signals, with each value represented in 2 bytes, like below (signal has 3 channels in this example):
    * next 2 bytes - first value of the first channel, in little-endian short integer format
    * next 2 bytes - first value of the second channel, in little-endian short integer format
    * next 2 bytes - first value of the third channel, in little-endian short integer format
    * next 2 bytes - second value of the first channel, in little-endian short integer format
    * next 2 bytes - second value of the second channel, in little-endian short integer format
    * next 2 bytes - second value of the third channel, in little-endian short integer format
    * ...

### Converting values to actual measured values

* divide the value by the maximum short value (32767)
* multiply the value with the channel reference value
* add the channel offset to the value
* multiply the value with 1000 and divide by the channel sensitivity value
* if channel db_reference exists and is positive
    * multiply the log10 of the absolute value divided by the db_reference with 20 - `20 * log10(abs(value) / db_reference)`
    * add the channel pregain to the value

Reference code can be found in the `value_converter` function.
