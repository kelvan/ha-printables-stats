# Printables Stats for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

Home Assistant integration for [Printables.com](https://www.printables.com) user statistics.

## Features

- **Downloads**: Total number of downloads across all models.
- **Likes**: Total number of likes received.
- **Followers**: Number of followers.
- **Following**: Number of users you follow.
- **Models**: Total number of models published.
- **Joined Date**: When the account was created.
- **Badges**: Individual sensors for badge levels:
  - Designer
  - Maker
  - Download Maniac
  - Star of Design
  - Supporter
  - Continuous Supporter
  - Event Visitor

## Installation

### Via HACS (Recommended)

1. Open **HACS** in your Home Assistant instance.
2. Click on the three dots in the top right corner and select **Custom repositories**.
3. Add the following URL as a **Repository**: `https://gitlab.com/intheflow/ha-printables-stats`
4. Select **Integration** as the Category.
5. Click **Add**.
6. Find "Printables Stats" in the list and click **Download**.
7. Restart Home Assistant.

### Manual Installation

1. Download the latest release.
2. Copy the `custom_components/printables_stats` folder to your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

## Configuration

1. Go to **Settings** -> **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Printables Stats**.
4. Enter your Printables **User ID** (e.g., `kelvan_3864286`).

## Credits

Data provided by [Printables.com](https://www.printables.com). Built using the [printables-stats](https://github.com/fly0/printables-stats) library.
