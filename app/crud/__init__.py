# app/crud/__init__.py

# ───── Franchises ─────
from .franchises import (
    add_franchise,
    get_franchises,
    update_franchise,
    soft_delete_franchise,
)

# ───── Locations ─────
from .locations import (
    add_location,
    get_locations,
    update_location,
    soft_delete_location,
    get_sensors_by_location,
)

# ───── Sensors ─────
from .sensors import (
    add_sensor,
    get_sensors,
    update_sensor,
    soft_delete_sensor,
)

# ───── Sensor Readings ─────
from .readings import (
    insert_sensor_reading,
    get_sensor_readings,
)
