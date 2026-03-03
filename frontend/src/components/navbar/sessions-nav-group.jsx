import { Monitor, Plus } from "lucide-react"
import { NavLink } from "react-router"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import {
  SidebarGroup,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar"

const mockSessions = [
  {
    title: "My First Session",
    slug: "my-first-session",
  },
]

export function SessionsNavGroup({ onAddSession }) {
  return (
    <SidebarGroup>
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
                <Plus className="size-3 text-muted-foreground" />
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
  )
}
