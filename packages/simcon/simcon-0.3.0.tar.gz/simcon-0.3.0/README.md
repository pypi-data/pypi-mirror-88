# py-simcon

This is a Python wrapper for SimConnect library which is used to talk to
Microsoft Flight Simulator. This wrapper provides natural pythonic interface.
It can be used in both synchronous and asynchronous (asyncio) applications.
In both cases it is thread safe.

## Features

  * Listen to system events (aircraft loaded, game paused, etc)
  * Receive data updates
  * Async and sync interfaces, which can work together simultaneously

## Examples

#### Conventional (synchronous)

```python
import pprint

from simcon import Sim, DataField, PERIOD


with Sim("asd") as sim: 
    data_request = sim.request_data_on_sim_object(
        [
            DataField("Plane latitude", "degrees"),
            DataField("Plane longitude", "degrees"),
            DataField("Plane altitude", "feet"),
            DataField("GPS ground true track", "degrees"),
            DataField("GPS ground speed", "knots"),
            DataField("Zulu time", "seconds"),
        ],
        PERIOD.SIMCONNECT_PERIOD_SECOND,
    )
    count = 0
    for data in data_request:
        pprint.pprint(data)
        count += 1
        if count >= 10:
            break
```

Result:
```
{'GPS ground speed': 97.83114326014487,
 'GPS ground true track': 307.4598039853386,
 'Plane altitude': 8501.684970335986,
 'Plane latitude': 39.3924225392898,
 'Plane longitude': -125.57142850592173,
 'Zulu time': 3287.369384765625}
{'GPS ground speed': 97.83704928992589,
 'GPS ground true track': 307.45556123353225,
 'Plane altitude': 8501.840396854732,
 'Plane latitude': 39.39269706474836,
 'Plane longitude': -125.57189141562071,
 'Zulu time': 3288.369384765625}
...
```

#### Asynchronous (asyncio):

```python
import asyncio
import pprint

from simcon import Sim, DataField, PERIOD


async def show_data():
    async with Sim("asd") as sim: 
        data_request = sim.request_data_on_sim_object(
            [
                DataField("Plane latitude", "degrees"),
                DataField("Plane longitude", "degrees"),
                DataField("Plane altitude", "feet"),
                DataField("GPS ground true track", "degrees"),
                DataField("GPS ground speed", "knots"),
                DataField("Zulu time", "seconds"),
            ],
            PERIOD.SIMCONNECT_PERIOD_SECOND,
        )
        count = 0
        async for data in data_request:
            pprint.pprint(data)
            count += 1
            if count >= 10:
                break

asyncio.run(show_data())
```

Results will be the same as in the example above


## Release History

### 0.3.0
  * Added support for strings, integer, and float32 data types
  * Added a helper to request data once

### 0.2.0

  * Added `start()` and `stop()` methods. All event and data listeners
    will throw Closed() exception if they are still being awaited when
    Sim stops, or if it is already stopped when wait() is called.

### 0.1.0
  * Initial release
