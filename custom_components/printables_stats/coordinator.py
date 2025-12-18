from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from printables_stats import PrintablesClient

from .const import DOMAIN, LOGGER, SCAN_INTERVAL_MINUTES


class PrintablesDataUpdateCoordinator(DataUpdateCoordinator):
    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        super().__init__(
            hass,
            LOGGER,
            name=f"{DOMAIN}_{config_entry.data['user_id']}",
            update_interval=timedelta(minutes=SCAN_INTERVAL_MINUTES),
        )
        self.config_entry = config_entry
        self.client = PrintablesClient()
        self.user_id = config_entry.data["user_id"]

    async def _async_update_data(self):
        """Fetch data from Printables."""
        try:
            # The library is synchronous, so we run it in an executor
            stats = await self.hass.async_add_executor_job(
                self.client.get_user_stats, self.user_id
            )

            if not stats:
                raise UpdateFailed(
                    "Failed to fetch data from Printables (returned None)."
                )

            return stats
        except Exception as err:
            raise UpdateFailed(
                f"Error communicating with Printables: {err}"
            ) from err
