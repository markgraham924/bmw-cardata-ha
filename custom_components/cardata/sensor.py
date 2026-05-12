"""Sensor platform for BMW CarData."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util
from homeassistant.const import UnitOfLength

from .const import DOMAIN
from .coordinator import CardataCoordinator
from .entity import CardataEntity

TRACKER_ONLY_DESCRIPTORS = {
    "vehicle.cabin.infotainment.navigation.currentLocation.latitude",
    "vehicle.cabin.infotainment.navigation.currentLocation.longitude",
    "vehicle.cabin.infotainment.navigation.currentLocation.heading",
}

DIAGNOSTIC_SENSOR_DESCRIPTORS = {
    "vehicle.vehicle.timeSetting",
    "vehicle.channel.ngtp.timeVehicle",
    "vehicle.cabin.infotainment.isMobilePhoneConnected",
    "vehicle.cabin.infotainment.displayUnit.distance",
    "vehicle.cabin.infotainment.hmi.distanceUnit",
    "vehicle.cabin.infotainment.navigation.currentLocation.altitude",
    "vehicle.cabin.infotainment.navigation.currentLocation.fixStatus",
    "vehicle.cabin.infotainment.navigation.currentLocation.numberOfSatellites",
    "vehicle.cabin.infotainment.navigation.destinationSet.latitude",
    "vehicle.cabin.infotainment.navigation.destinationSet.longitude",
    "vehicle.cabin.infotainment.navigation.destinationSet.arrivalTime",
    "vehicle.cabin.infotainment.navigation.remainingRange",
    "vehicle.cabin.infotainment.navigation.pointsOfInterests.max",
    "vehicle.channel.teleservice.status",
    "vehicle.channel.teleservice.lastAutomaticServiceCallTime",
    "vehicle.channel.teleservice.lastTeleserviceReportTime",
    "vehicle.channel.teleservice.lastBreakdownCallTime",
    "vehicle.channel.teleservice.lastManualCallTime",
    "vehicle.electronicControlUnit.diagnosticTroubleCodes.raw",
    "vehicle.serviceDemand.defect.id",
    "vehicle.sevice.preferredSevicePartner",
    "vehicle.status.checkControlMessages",
    "vehicle.status.conditionBasedServices",
    "vehicle.status.conditionBasedServicesCount",
    "vehicle.status.conditionBasedServicesAverageDistancePerDay",
    "vehicle.status.serviceDistance.yellow",
    "vehicle.status.serviceTime.yellow",
    "vehicle.status.serviceTime.hUandAuServiceYellow",
}

TIMESTAMP_SENSOR_DESCRIPTORS = {
    "vehicle.trip.segment.end.time",
    "vehicle.status.serviceTime.inspectionDateLegal",
    "vehicle.channel.teleservice.lastAutomaticServiceCallTime",
    "vehicle.channel.teleservice.lastTeleserviceReportTime",
    "vehicle.channel.teleservice.lastBreakdownCallTime",
    "vehicle.channel.teleservice.lastManualCallTime",
    "vehicle.cabin.infotainment.navigation.destinationSet.arrivalTime",
}


class CardataSensor(CardataEntity, SensorEntity):
    def __init__(self, coordinator: CardataCoordinator, vin: str, descriptor: str) -> None:
        super().__init__(coordinator, vin, descriptor)
        self._attr_should_poll = False
        self._unsubscribe = None
        self._apply_descriptor_metadata()

    def _apply_descriptor_metadata(self) -> None:
        descriptor = self._descriptor
        if descriptor in TIMESTAMP_SENSOR_DESCRIPTORS:
            self._attr_device_class = SensorDeviceClass.TIMESTAMP
        elif descriptor == "vehicle.vehicle.travelledDistance":
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
            self._attr_device_class = SensorDeviceClass.DISTANCE
        elif descriptor.endswith(".travelledDistance") or descriptor.endswith(".referenceDistance"):
            self._attr_device_class = SensorDeviceClass.DISTANCE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith("remainingRange") or descriptor.endswith("remainingFuel"):
            self._attr_device_class = SensorDeviceClass.DISTANCE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".stateOfCharge") or descriptor.endswith(".target") or descriptor.endswith(".targetMin"):
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".stateOfHealth.displayed"):
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_entity_category = EntityCategory.DIAGNOSTIC
        elif descriptor.endswith(".level") and "fuelSystem" in descriptor:
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith("remainingTime") or descriptor.endswith("timeToFullyCharged"):
            self._attr_device_class = SensorDeviceClass.DURATION
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".header") or descriptor.endswith(".level"):
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".power"):
            self._attr_device_class = SensorDeviceClass.POWER
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".acVoltage") or descriptor.endswith(".voltage"):
            self._attr_device_class = SensorDeviceClass.VOLTAGE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".acAmpere"):
            self._attr_device_class = SensorDeviceClass.CURRENT
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".temperature"):
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".pressure") or descriptor.endswith(".pressureTarget"):
            self._attr_device_class = SensorDeviceClass.PRESSURE
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif descriptor.endswith(".gridEnergy"):
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif descriptor.endswith(".fuel"):
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif descriptor.endswith(".hour") or descriptor.endswith(".minute"):
            self._attr_entity_category = EntityCategory.CONFIG
        elif descriptor.endswith(".action") or descriptor.endswith(".preference") or descriptor.endswith(".mode"):
            self._attr_entity_category = EntityCategory.CONFIG
        elif descriptor.endswith(".latitude") or descriptor.endswith(".longitude"):
            self._attr_entity_category = EntityCategory.DIAGNOSTIC
        elif descriptor.endswith(".heading"):
            self._attr_icon = "mdi:compass"
            self._attr_entity_category = EntityCategory.DIAGNOSTIC
        elif descriptor.endswith(".altitude"):
            self._attr_entity_category = EntityCategory.DIAGNOSTIC
        elif descriptor.endswith(".numberOfSatellites"):
            self._attr_icon = "mdi:satellite-variant"
            self._attr_entity_category = EntityCategory.DIAGNOSTIC
        elif descriptor.endswith(".fixStatus"):
            self._attr_icon = "mdi:crosshairs-gps"
            self._attr_entity_category = EntityCategory.DIAGNOSTIC
        elif "service" in descriptor or "diagnosis" in descriptor:
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

        if "tire" in descriptor:
            self._attr_icon = "mdi:car-tire-alert"
        elif "chargingPort" in descriptor or ".flap." in descriptor:
            self._attr_icon = "mdi:ev-plug-type2"
        elif "preConditioning" in descriptor or "preconditioning" in descriptor:
            self._attr_icon = "mdi:car-clock"
        elif "conditionBasedServices" in descriptor or "service" in descriptor:
            self._attr_icon = "mdi:wrench"

        if descriptor in DIAGNOSTIC_SENSOR_DESCRIPTORS:
            self._attr_entity_category = EntityCategory.DIAGNOSTIC
    
    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if getattr(self, "_attr_native_value", None) is None:
            last_state = await self.async_get_last_state()
            if last_state and last_state.state not in ("unknown", "unavailable"):
                if self._attr_device_class == SensorDeviceClass.TIMESTAMP:
                    parsed = dt_util.parse_datetime(last_state.state)
                    self._attr_native_value = parsed or last_state.state
                else:
                    self._attr_native_value = last_state.state
                unit = last_state.attributes.get("unit_of_measurement")
                if unit is not None:
                    self._attr_native_unit_of_measurement = unit
                    # If unit is a length/distance type, enable conversion
                    if unit in {u.value for u in UnitOfLength}:
                        self._attr_device_class = SensorDeviceClass.DISTANCE # Enables km/mi, m/ft, etc., conversion
                timestamp = last_state.attributes.get("timestamp")
                if not timestamp and last_state.last_changed:
                    timestamp = last_state.last_changed.isoformat()
                self._coordinator.restore_descriptor_state(
                    self.vin,
                    self.descriptor,
                    self._attr_native_value,
                    unit,
                    timestamp,
                )
        self._unsubscribe = async_dispatcher_connect(
            self.hass,
            self._coordinator.signal_update,
            self._handle_update,
        )
        self._handle_update(self.vin, self.descriptor)

    async def async_will_remove_from_hass(self) -> None:
        await super().async_will_remove_from_hass()
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

    def _handle_update(self, vin: str, descriptor: str) -> None:
        if vin != self.vin or descriptor != self.descriptor:
            return
        state = self._coordinator.get_state(vin, descriptor)
        if not state:
            return
        if self._attr_device_class == SensorDeviceClass.TIMESTAMP and isinstance(state.value, str):
            parsed = dt_util.parse_datetime(state.value)
            self._attr_native_value = parsed or state.value
        else:
            self._attr_native_value = state.value
        self._attr_native_unit_of_measurement = state.unit

        self.schedule_update_ha_state()


class CardataDiagnosticsSensor(SensorEntity, RestoreEntity):
    _attr_should_poll = False
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: CardataCoordinator,
        stream_manager,
        entry_id: str,
        sensor_type: str,
        quota_manager,
    ) -> None:
        self._coordinator = coordinator
        self._stream = stream_manager
        self._entry_id = entry_id
        self._sensor_type = sensor_type
        self._quota = quota_manager
        self._unsub = None
        if sensor_type == "last_message":
            suffix = "last_message"
            self._attr_name = "Last Message Received"
            self._attr_device_class = SensorDeviceClass.TIMESTAMP
        elif sensor_type == "last_telematic_api":
            suffix = "last_telematic_api"
            self._attr_name = "Last Telematics API Call"
            self._attr_device_class = SensorDeviceClass.TIMESTAMP
        elif sensor_type == "connection_status":
            suffix = "connection_status"
            self._attr_name = "Stream Connection Status"
        else:
            suffix = sensor_type
            self._attr_name = sensor_type
        self._attr_unique_id = f"{entry_id}_diagnostics_{suffix}"

    @property
    def device_info(self) -> DeviceInfo:
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "manufacturer": "BMW",
            "name": "CarData Debug Device",
        }

    @property
    def extra_state_attributes(self) -> dict:
        if self._sensor_type == "connection_status":
            attrs = dict(self._stream.debug_info)
            if self._coordinator.last_disconnect_reason:
                attrs["last_disconnect_reason"] = self._coordinator.last_disconnect_reason
            if self._quota:
                attrs["api_quota_used"] = self._quota.used
                attrs["api_quota_remaining"] = self._quota.remaining
                if next_reset := self._quota.next_reset_iso:
                    attrs["api_quota_next_reset"] = next_reset
            return attrs
        if self._sensor_type == "last_telematic_api":
            attrs: dict[str, Any] = {}
            if self._quota:
                attrs["api_quota_used"] = self._quota.used
                attrs["api_quota_remaining"] = self._quota.remaining
                if next_reset := self._quota.next_reset_iso:
                    attrs["api_quota_next_reset"] = next_reset
            return attrs
        return {}

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self._attr_native_value is None:
            last_state = await self.async_get_last_state()
            if last_state and last_state.state not in ("unknown", "unavailable"):
                if self._sensor_type in {"last_message", "last_telematic_api"}:
                    self._attr_native_value = dt_util.parse_datetime(last_state.state)
                else:
                    self._attr_native_value = last_state.state
        self._unsub = async_dispatcher_connect(
            self.hass,
            self._coordinator.signal_diagnostics,
            self._handle_update,
        )
        self._handle_update()

    async def async_will_remove_from_hass(self) -> None:
        if self._unsub:
            self._unsub()
            self._unsub = None

    def _handle_update(self) -> None:
        if self._sensor_type == "last_message":
            value = self._coordinator.last_message_at
            if value is not None:
                self._attr_native_value = value
        elif self._sensor_type == "last_telematic_api":
            value = self._coordinator.last_telematic_api_at
            if value is not None:
                self._attr_native_value = value
        elif self._sensor_type == "connection_status":
            value = self._coordinator.connection_status
            if value is not None:
                self._attr_native_value = value
        self.schedule_update_ha_state()

    @property
    def native_value(self):
        return self._attr_native_value


class CardataSocEstimateSensor(CardataEntity, SensorEntity):
    _attr_should_poll = False
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"
    _attr_icon = "mdi:battery-clock"

    def __init__(self, coordinator: CardataCoordinator, vin: str) -> None:
        super().__init__(coordinator, vin, "soc_estimate")
        self._base_name = "State Of Charge (Predicted on Integration side)"
        self._update_name(write_state=False)
        self._unsubscribe = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in ("unknown", "unavailable"):
            try:
                self._attr_native_value = float(last_state.state)
            except (TypeError, ValueError):
                self._attr_native_value = None
            else:
                restored_ts = last_state.attributes.get("timestamp")
                reference = dt_util.parse_datetime(restored_ts) if restored_ts else None
                if reference is None:
                    reference = last_state.last_changed
                if reference is not None:
                    reference = dt_util.as_utc(reference)
                if self._coordinator.get_soc_estimate(self.vin) is None:
                    self._coordinator.restore_soc_cache(
                        self.vin,
                        estimate=self._attr_native_value,
                        timestamp=reference,
                    )
        self._unsubscribe = async_dispatcher_connect(
            self.hass,
            self._coordinator.signal_soc_estimate,
            self._handle_update,
        )
        existing = self._coordinator.get_soc_estimate(self.vin)
        if existing is not None:
            self._attr_native_value = existing
            self.schedule_update_ha_state()

    async def async_will_remove_from_hass(self) -> None:
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

    def _handle_update(self, vin: str) -> None:
        if vin != self.vin:
            return
        value = self._coordinator.get_soc_estimate(vin)
        self._attr_native_value = value
        self.schedule_update_ha_state()


class CardataTestingSocEstimateSensor(CardataEntity, SensorEntity):
    _attr_should_poll = False
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"
    _attr_icon = "mdi:battery-clock"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: CardataCoordinator, vin: str) -> None:
        super().__init__(coordinator, vin, "soc_estimate_testing")
        self._base_name = "New Extrapolation Testing sensor"
        self._update_name(write_state=False)
        self._unsubscribe = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in ("unknown", "unavailable"):
            try:
                self._attr_native_value = float(last_state.state)
            except (TypeError, ValueError):
                self._attr_native_value = None
            else:
                restored_ts = last_state.attributes.get("timestamp")
                reference = dt_util.parse_datetime(restored_ts) if restored_ts else None
                if reference is None:
                    reference = last_state.last_changed
                if reference is not None:
                    reference = dt_util.as_utc(reference)
                if self._coordinator.get_testing_soc_estimate(self.vin) is None:
                    self._coordinator.restore_testing_soc_cache(
                        self.vin,
                        estimate=self._attr_native_value,
                        timestamp=reference,
                    )
        self._unsubscribe = async_dispatcher_connect(
            self.hass,
            self._coordinator.signal_soc_estimate,
            self._handle_update,
        )
        existing = self._coordinator.get_testing_soc_estimate(self.vin)
        if existing is not None:
            self._attr_native_value = existing
            self.schedule_update_ha_state()

    async def async_will_remove_from_hass(self) -> None:
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

    def _handle_update(self, vin: str) -> None:
        if vin != self.vin:
            return
        value = self._coordinator.get_testing_soc_estimate(vin)
        self._attr_native_value = value
        self.schedule_update_ha_state()


class CardataSocRateSensor(CardataEntity, SensorEntity):
    _attr_should_poll = False
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%/h"
    _attr_icon = "mdi:battery-clock"

    def __init__(self, coordinator: CardataCoordinator, vin: str) -> None:
        super().__init__(coordinator, vin, "soc_rate")
        self._base_name = "Predicted charge speed"
        self._update_name(write_state=False)
        self._unsubscribe = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in ("unknown", "unavailable"):
            try:
                self._attr_native_value = float(last_state.state)
            except (TypeError, ValueError):
                self._attr_native_value = None
            else:
                restored_ts = last_state.attributes.get("timestamp")
                reference = dt_util.parse_datetime(restored_ts) if restored_ts else None
                if reference is None:
                    reference = last_state.last_changed
                if reference is not None:
                    reference = dt_util.as_utc(reference)
                if self._coordinator.get_soc_rate(self.vin) is None:
                    self._coordinator.restore_soc_cache(
                        self.vin,
                        rate=self._attr_native_value,
                        timestamp=reference,
                    )
        self._unsubscribe = async_dispatcher_connect(
            self.hass,
            self._coordinator.signal_soc_estimate,
            self._handle_update,
        )
        existing = self._coordinator.get_soc_rate(self.vin)
        if existing is not None:
            self._attr_native_value = existing
            self.schedule_update_ha_state()

    async def async_will_remove_from_hass(self) -> None:
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None

    def _handle_update(self, vin: str) -> None:
        if vin != self.vin:
            return
        value = self._coordinator.get_soc_rate(vin)
        self._attr_native_value = value
        self.schedule_update_ha_state()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    runtime = hass.data[DOMAIN][entry.entry_id]
    coordinator: CardataCoordinator = runtime.coordinator

    entities: Dict[Tuple[str, str], CardataSensor] = {}
    soc_estimate_entities: Dict[str, CardataSocEstimateSensor] = {}
    soc_estimate_testing_entities: Dict[str, CardataTestingSocEstimateSensor] = {}
    soc_rate_entities: Dict[str, CardataSocRateSensor] = {}

    def ensure_soc_tracking_entities(vin: str) -> None:
        new_entities = []
        if vin not in soc_estimate_entities:
            estimate = CardataSocEstimateSensor(coordinator, vin)
            soc_estimate_entities[vin] = estimate
            new_entities.append(estimate)
        if vin not in soc_estimate_testing_entities:
            testing_estimate = CardataTestingSocEstimateSensor(coordinator, vin)
            soc_estimate_testing_entities[vin] = testing_estimate
            new_entities.append(testing_estimate)
        if vin not in soc_rate_entities:
            rate = CardataSocRateSensor(coordinator, vin)
            soc_rate_entities[vin] = rate
            new_entities.append(rate)
        if new_entities:
            async_add_entities(new_entities, True)

    def ensure_entity(vin: str, descriptor: str, *, assume_sensor: bool = False) -> None:
        ensure_soc_tracking_entities(vin)
        if (vin, descriptor) in entities:
            return
        
        # Filter out location descriptors - these are used by device_tracker only
        if descriptor in TRACKER_ONLY_DESCRIPTORS:
            return
        
        state = coordinator.get_state(vin, descriptor)
        if state:
            if isinstance(state.value, bool):
                return
        elif not assume_sensor:
            return
        entity = CardataSensor(coordinator, vin, descriptor)
        entities[(vin, descriptor)] = entity
        async_add_entities([entity])

    entity_registry = er.async_get(hass)
    legacy_unique_ids = {
        f"{entry.entry_id}_connection_status": f"{entry.entry_id}_diagnostics_connection_status",
        f"{entry.entry_id}_last_message": f"{entry.entry_id}_diagnostics_last_message",
    }
    for old_unique_id, new_unique_id in legacy_unique_ids.items():
        entity_id = entity_registry.async_get_entity_id("sensor", DOMAIN, old_unique_id)
        if entity_id:
            entity_registry.async_update_entity(
                entity_id, new_unique_id=new_unique_id
            )

    legacy_soc_rate_unique = f"{entry.entry_id}_diagnostics_soc_rate"
    legacy_soc_rate_entity = entity_registry.async_get_entity_id(
        "sensor", DOMAIN, legacy_soc_rate_unique
    )
    if legacy_soc_rate_entity:
        entity_registry.async_remove(legacy_soc_rate_entity)

    for entity_entry in er.async_entries_for_config_entry(
        entity_registry, entry.entry_id
    ):
        if entity_entry.domain != "sensor":
            continue
        if entity_entry.disabled_by is not None:
            continue
        unique_id = entity_entry.unique_id
        if not unique_id or "_" not in unique_id:
            continue
        if unique_id.startswith(f"{entry.entry_id}_diagnostics_"):
            continue
        vin, descriptor = unique_id.split("_", 1)
        if descriptor in {"soc_estimate", "soc_rate", "soc_estimate_testing"}:
            ensure_soc_tracking_entities(vin)
            continue
        ensure_entity(vin, descriptor, assume_sensor=True)

    for vin, descriptor in coordinator.iter_descriptors(binary=False):
        ensure_entity(vin, descriptor)

    for vin in list(coordinator.data.keys()):
        ensure_soc_tracking_entities(vin)

    async def async_handle_new(vin: str, descriptor: str) -> None:
        ensure_entity(vin, descriptor)

    entry.async_on_unload(
        async_dispatcher_connect(hass, coordinator.signal_new_sensor, async_handle_new)
    )

    async def async_handle_soc_estimate(vin: str) -> None:
        ensure_soc_tracking_entities(vin)

    entry.async_on_unload(
        async_dispatcher_connect(
            hass, coordinator.signal_soc_estimate, async_handle_soc_estimate
        )
    )

    diagnostic_entities: list[CardataDiagnosticsSensor] = []
    stream_manager = runtime.stream
    for sensor_type in ("connection_status", "last_message", "last_telematic_api"):
        if sensor_type == "last_message":
            unique_id = f"{entry.entry_id}_diagnostics_last_message"
        elif sensor_type == "last_telematic_api":
            unique_id = f"{entry.entry_id}_diagnostics_last_telematic_api"
        else:
            unique_id = f"{entry.entry_id}_diagnostics_connection_status"
        entity_id = entity_registry.async_get_entity_id("sensor", DOMAIN, unique_id)
        if entity_id:
            entity_entry = entity_registry.async_get(entity_id)
            if entity_entry and entity_entry.disabled_by is not None:
                continue
            existing_state = hass.states.get(entity_id)
            if existing_state and not existing_state.attributes.get("restored", False):
                continue
        diagnostic_entities.append(
            CardataDiagnosticsSensor(
                coordinator,
                stream_manager,
                entry.entry_id,
                sensor_type,
                runtime.quota_manager,
            )
        )

    if diagnostic_entities:
        async_add_entities(diagnostic_entities, True)
