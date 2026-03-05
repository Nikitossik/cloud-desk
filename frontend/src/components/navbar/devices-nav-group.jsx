import { useState } from "react"
import { MonitorCog } from "lucide-react"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { FaApple, FaDesktop, FaLinux, FaPen, FaWindows } from "react-icons/fa"
import { useUserSidebarQuery } from "@/features/user/hooks/use-user-sidebar-query"
import { useUpdateCurrentDeviceMutation } from "@/features/device/hooks/use-update-current-device-mutation"
import { Input } from "@/components/ui/input"
import {
  SidebarGroup,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar"

function getDeviceOsIcon(osName) {
  const normalized = (osName ?? "").toLowerCase()

  if (normalized.includes("windows")) return FaWindows
  if (normalized.includes("mac") || normalized.includes("darwin")) return FaApple
  if (normalized.includes("linux")) return FaLinux

  return FaDesktop
}

export function DevicesNavGroup() {
  const [editingDeviceId, setEditingDeviceId] = useState(null)
  const [editingName, setEditingName] = useState("")

  const { data: sidebarData, isLoading: isDevicesLoading } = useUserSidebarQuery()
  const userDevices = Array.isArray(sidebarData?.devices) ? sidebarData.devices : []
  const updateCurrentDeviceMutation = useUpdateCurrentDeviceMutation({
    onSuccess: () => {
      setEditingDeviceId(null)
      setEditingName("")
    },
  })

  const isSavingName = updateCurrentDeviceMutation.isLoading

  const startEditing = (deviceId, currentName) => {
    setEditingDeviceId(deviceId)
    setEditingName(currentName || "")
  }

  const cancelEditing = () => {
    setEditingDeviceId(null)
    setEditingName("")
  }

  const submitEditing = (device) => {
    if (!device.isActive) {
      cancelEditing()
      return
    }

    const nextName = editingName.trim()
    const currentName = (device.name || "").trim()

    if (!nextName || nextName === currentName) {
      cancelEditing()
      return
    }

    updateCurrentDeviceMutation.mutate(nextName)
  }

  const devices = userDevices.map((device) => ({
    id: device.id,
    name: device.display_name || "Unnamed device",
    osName: device.os_name,
    osRelease: device.os_release,
    osVersion: device.os_release_ver,
    architecture: device.architecture,
    macAddress: device.mac_address,
    isActive: Boolean(device.is_current),
  }))

  return (
    <SidebarGroup>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton className="cursor-default" tooltip="Devices">
            <MonitorCog />
            <span>Devices</span>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>

      <SidebarMenuSub>
        {isDevicesLoading ? (
          <SidebarMenuSubItem>
            <SidebarMenuSubButton asChild>
              <span className="text-muted-foreground">Loading device...</span>
            </SidebarMenuSubButton>
          </SidebarMenuSubItem>
        ) : devices.length === 0 ? (
          <SidebarMenuSubItem>
            <SidebarMenuSubButton asChild>
              <span className="text-muted-foreground">No devices</span>
            </SidebarMenuSubButton>
          </SidebarMenuSubItem>
        ) : (
          devices.map((device) => (
            <SidebarMenuSubItem key={device.id}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <SidebarMenuSubButton className="group/device-row">
                    <span className="flex w-full min-w-0 items-center justify-between gap-2">
                      <span className="flex min-w-0 items-center gap-2">
                        {(() => {
                          const DeviceOsIcon = getDeviceOsIcon(device.osName)
                          return <DeviceOsIcon className="size-4 shrink-0" />
                        })()}
                        {editingDeviceId === device.id ? (
                          <Input
                            autoFocus
                            value={editingName}
                            onChange={(event) => setEditingName(event.target.value)}
                            onClick={(event) => {
                              event.preventDefault()
                              event.stopPropagation()
                            }}
                            onBlur={() => submitEditing(device)}
                            onKeyDown={(event) => {
                              if (event.key === "Enter") {
                                event.preventDefault()
                                submitEditing(device)
                              }

                              if (event.key === "Escape") {
                                event.preventDefault()
                                cancelEditing()
                              }
                            }}
                            disabled={isSavingName}
                            className="h-6 border-0 bg-transparent px-0 shadow-none ring-0 focus-visible:ring-0 focus-visible:ring-offset-0"
                          />
                        ) : (
                          <span className="truncate">{device.name}</span>
                        )}
                      </span>
                      <span className="flex shrink-0 items-center gap-2">
                        {device.isActive && editingDeviceId !== device.id ? (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <button
                                type="button"
                                aria-label="Edit"
                                className="opacity-0 transition-opacity group-hover/device-row:opacity-100"
                                onClick={(event) => {
                                  event.preventDefault()
                                  event.stopPropagation()
                                  startEditing(device.id, device.name)
                                }}
                              >
                                <FaPen className="size-3 text-muted-foreground" />
                              </button>
                            </TooltipTrigger>
                            <TooltipContent side="top" sideOffset={4}>
                              Edit
                            </TooltipContent>
                          </Tooltip>
                        ) : null}

                        {device.isActive ? (
                          <span
                            className="h-2.5 w-2.5 rounded-full bg-green-500"
                            aria-label="Active device"
                          />
                        ) : null}
                      </span>
                    </span>
                  </SidebarMenuSubButton>
                </TooltipTrigger>
                <TooltipContent side="right" align="center" className="max-w-72">
                  <div className="space-y-1 text-xs">
                    <p><span className="font-medium">Name:</span> {device.name}</p>
                    <p><span className="font-medium">OS:</span> {device.osName || "-"}</p>
                    <p><span className="font-medium">Release:</span> {device.osRelease || "-"}</p>
                    <p><span className="font-medium">Version:</span> {device.osVersion || "-"}</p>
                    <p><span className="font-medium">Architecture:</span> {device.architecture || "-"}</p>
                    <p><span className="font-medium">MAC:</span> {device.macAddress || "-"}</p>
                  </div>
                </TooltipContent>
              </Tooltip>
            </SidebarMenuSubItem>
          ))
        )}
      </SidebarMenuSub>
    </SidebarGroup>
  )
}
