import { BarChart3, Monitor, MonitorCog, Plus } from "lucide-react";
import { NavLink } from "react-router";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"

import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar"

const mockDevices = [
  {
    id: "current-device",
    name: "My Windows PC",
  },
]

const mockSessions = [
  {
    title: "My First Session",
    slug: "my-first-session",
  },
]

export function NavMain({ onAddSession }) {
  return (
    <>
      <SidebarGroup>
        <SidebarGroupLabel>Devices</SidebarGroupLabel>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton className="cursor-default" tooltip="Devices">
              <MonitorCog />
              <span>Devices</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>

        <SidebarMenuSub>
          {mockDevices.length === 0 ? (
            <SidebarMenuSubItem>
              <SidebarMenuSubButton asChild>
                <span className="text-muted-foreground">No devices</span>
              </SidebarMenuSubButton>
            </SidebarMenuSubItem>
          ) : (
            mockDevices.map((device) => (
              <SidebarMenuSubItem key={device.id}>
                <SidebarMenuSubButton asChild>
                  <NavLink to={`/device/${device.id}`}>
                    <span>{device.name}</span>
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
            ))
          )}
        </SidebarMenuSub>
      </SidebarGroup>

      <SidebarGroup>
        <SidebarGroupLabel>Sessions</SidebarGroupLabel>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton className="cursor-default" tooltip="Sessions">
              <Monitor />
              <span>Sessions</span>
            </SidebarMenuButton>
            <Tooltip>
              <TooltipTrigger asChild>
                <SidebarMenuAction
                  showOnHover
                  aria-label="Add session"
                  onClick={(event) => {
                    event.preventDefault()
                    event.stopPropagation()
                    onAddSession?.()
                  }}
                >
                  <Plus />
                </SidebarMenuAction>
              </TooltipTrigger>
              <TooltipContent side="bottom" sideOffset={2}>
                Add new session
              </TooltipContent>
            </Tooltip>
          </SidebarMenuItem>
        </SidebarMenu>

        <SidebarMenuSub>
          {mockSessions.length === 0 ? (
            <SidebarMenuSubItem>
              <SidebarMenuSubButton asChild>
                <span className="text-muted-foreground">No sessions</span>
              </SidebarMenuSubButton>
            </SidebarMenuSubItem>
          ) : (
            mockSessions.map((session) => (
              <SidebarMenuSubItem key={session.slug}>
                <SidebarMenuSubButton asChild>
                  <NavLink to={`/session/${session.slug}`}>
                    <span>{session.title}</span>
                  </NavLink>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
            ))
          )}
        </SidebarMenuSub>
      </SidebarGroup>

      <SidebarGroup>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip="Statistics">
              <NavLink to="/statistics">
                <BarChart3 />
                <span>Statistics</span>
              </NavLink>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </>
  );
}
