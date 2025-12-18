from datetime import date, datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.dt import UTC

from .const import DOMAIN
from .coordinator import PrintablesDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: PrintablesDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        PrintablesDownloadsSensor(coordinator),
        PrintablesLikesSensor(coordinator),
        PrintablesFollowersSensor(coordinator),
        PrintablesFollowingSensor(coordinator),
        PrintablesModelsSensor(coordinator),
        PrintablesJoinDateSensor(coordinator),
        PrintablesDesignerBadgeSensor(coordinator),
        PrintablesMakerBadgeSensor(coordinator),
        PrintablesDownloadManiacBadgeSensor(coordinator),
        PrintablesStarOfDesignBadgeSensor(coordinator),
        PrintablesSupporterBadgeSensor(coordinator),
        PrintablesContinuousSupporterBadgeSensor(coordinator),
        PrintablesEventVisitorBadgeSensor(coordinator),
    ]

    async_add_entities(sensors)


class PrintablesBaseSensor(
    CoordinatorEntity[PrintablesDataUpdateCoordinator], SensorEntity
):
    _attr_has_entity_name = True

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_attribution = "Data provided by Printables.com"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.user_id)},
            "name": f"Printables User {coordinator.user_id}",
            "manufacturer": "Printables",
            "model": "User Stats",
            "configuration_url": (
                f"https://www.printables.com/{coordinator.user_id}"
            ),
        }


class PrintablesDownloadsSensor(PrintablesBaseSensor):
    _attr_translation_key = "downloads"
    _attr_native_unit_of_measurement = "downloads"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:download"
    _attr_unique_id_suffix = "downloads"

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_downloads"
        self._attr_name = "Downloads"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("downloads")


class PrintablesLikesSensor(PrintablesBaseSensor):
    _attr_translation_key = "likes"
    _attr_native_unit_of_measurement = "likes"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:heart"

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_likes"
        self._attr_name = "Likes"

    @property
    def native_value(self) -> int | None:
        return self.coordinator.data.get("likes")


class PrintablesFollowersSensor(PrintablesBaseSensor):
    _attr_translation_key = "followers"
    _attr_native_unit_of_measurement = "followers"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:account-group"

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_followers"
        self._attr_name = "Followers"

    @property
    def native_value(self) -> int | None:
        return self.coordinator.data.get("followers")


class PrintablesFollowingSensor(PrintablesBaseSensor):
    _attr_translation_key = "following"
    _attr_native_unit_of_measurement = "following"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:account-arrow-right"

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_following"
        self._attr_name = "Following"

    @property
    def native_value(self) -> int | None:
        return self.coordinator.data.get("following")


class PrintablesModelsSensor(PrintablesBaseSensor):
    _attr_translation_key = "models"
    _attr_native_unit_of_measurement = "models"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:cube"

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_models"
        self._attr_name = "Models"

    @property
    def native_value(self) -> int | None:
        return self.coordinator.data.get("models_count")


class PrintablesJoinDateSensor(PrintablesBaseSensor):
    _attr_translation_key = "joined_date"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:calendar-account"

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_joined_date"
        self._attr_name = "Joined Date"

    @property
    def native_value(self) -> datetime | None:
        val = self.coordinator.data.get("joined_date")
        if isinstance(val, datetime):
            return val.replace(tzinfo=UTC) if val.tzinfo is None else val
        if isinstance(val, date):
            return datetime.combine(val, datetime.min.time(), tzinfo=UTC)
        if isinstance(val, str):
            try:
                dt = datetime.fromisoformat(val)
                return dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt
            except ValueError:
                return None
        return None


class PrintablesDesignerBadgeSensor(PrintablesBaseSensor):
    _attr_translation_key = "designer_badge"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:medal"
    _attr_native_unit_of_measurement = ""

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_designer_badge"
        self._attr_name = "Designer Badge"

    @property
    def native_value(self) -> int:
        badges = self.coordinator.data.get("badges", {})
        return badges.get("Designer", 0)


class PrintablesMakerBadgeSensor(PrintablesBaseSensor):
    _attr_translation_key = "maker_badge"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:medal"
    _attr_native_unit_of_measurement = ""

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_maker_badge"
        self._attr_name = "Maker Badge"

    @property
    def native_value(self) -> int:
        badges = self.coordinator.data.get("badges", {})
        return badges.get("Maker", 0)


class PrintablesDownloadManiacBadgeSensor(PrintablesBaseSensor):
    _attr_translation_key = "download_maniac_badge"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:medal"
    _attr_native_unit_of_measurement = ""

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_download_maniac_badge"
        self._attr_name = "Download Maniac Badge"

    @property
    def native_value(self) -> int:
        badges = self.coordinator.data.get("badges", {})
        return badges.get("Download Maniac", 0)


class PrintablesStarOfDesignBadgeSensor(PrintablesBaseSensor):
    _attr_translation_key = "star_of_design_badge"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:medal"
    _attr_native_unit_of_measurement = ""

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_star_of_design_badge"
        self._attr_name = "Star of Design Badge"

    @property
    def native_value(self) -> int:
        badges = self.coordinator.data.get("badges", {})
        return badges.get("Star of Design", 0)


class PrintablesSupporterBadgeSensor(PrintablesBaseSensor):
    _attr_translation_key = "supporter_badge"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:medal"
    _attr_native_unit_of_measurement = ""

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_supporter_badge"
        self._attr_name = "Supporter Badge"

    @property
    def native_value(self) -> int:
        badges = self.coordinator.data.get("badges", {})
        return badges.get("Supporter", 0)


class PrintablesContinuousSupporterBadgeSensor(PrintablesBaseSensor):
    _attr_translation_key = "continuous_supporter_badge"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:medal"
    _attr_native_unit_of_measurement = ""

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_continuous_supporter_badge"
        self._attr_name = "Continuous Supporter Badge"

    @property
    def native_value(self) -> int:
        badges = self.coordinator.data.get("badges", {})
        return badges.get("Continuous Supporter", 0)


class PrintablesEventVisitorBadgeSensor(PrintablesBaseSensor):
    _attr_translation_key = "event_visitor_badge"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:medal"
    _attr_native_unit_of_measurement = ""

    def __init__(self, coordinator: PrintablesDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.user_id}_event_visitor_badge"
        self._attr_name = "Event Visitor Badge"

    @property
    def native_value(self) -> int:
        badges = self.coordinator.data.get("badges", {})
        return badges.get("Event Visitor", 0)

