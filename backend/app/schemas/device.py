from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID


class DeviceBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "mac_address": "00:1A:2B:3C:4D:5E",
                    "os_name": "Windows",
                    "os_release": "10",
                    "os_release_ver": "10.0.19045",
                    "architecture": "AMD64",
                    "created_at": "2024-04-26T12:34:56.789Z",
                }
            ]
        },
    )

    id: UUID = Field(description="Unique identifier for the device.")
    mac_address: str = Field(
        max_length=17,
        description="The MAC address of the device. Must be a string of maximum 17 characters.",
    )
    os_name: str = Field(
        description="The name of the operating system (e.g., Windows, Linux, macOS)."
    )
    os_release: str = Field(
        description="The release version of the operating system (e.g., 10, 11, 22.04)."
    )
    os_release_ver: str = Field(
        description="The detailed version information of the operating system (e.g., 10.0.19045)."
    )
    architecture: str = Field(
        description="The system architecture (e.g., AMD64, x86_64)."
    )
    created_at: datetime = Field(
        description="The timestamp when the device was registered."
    )