import { Monitor, Plus } from "lucide-react"
import { NavLink } from "react-router"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { useUserSidebarQuery } from "@/features/user/hooks/use-user-sidebar-query"
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

export function SessionsNavGroup({ onAddSession }) {
  const { data: sidebarData, isLoading: isSessionsLoading } = useUserSidebarQuery()
  const userSessions = Array.isArray(sidebarData?.sessions) ? sidebarData.sessions : []

  const sessions = userSessions
    .map((session) => ({
      slug: session.slugname || session.slug || "",
      name: session.name || "Unnamed session",
      isActive: Boolean(session.is_active),
    }))
    .filter((session) => Boolean(session.slug))

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
        {isSessionsLoading ? (
          <SidebarMenuSubItem>
            <SidebarMenuSubButton asChild>
              <span className="text-muted-foreground">Loading sessions...</span>
            </SidebarMenuSubButton>
          </SidebarMenuSubItem>
        ) : sessions.length === 0 ? (
          <SidebarMenuSubItem>
            <SidebarMenuSubButton asChild>
              <span className="text-muted-foreground">No sessions</span>
            </SidebarMenuSubButton>
          </SidebarMenuSubItem>
        ) : (
          sessions.map((session) => (
            <SidebarMenuSubItem key={session.slug}>
              <SidebarMenuSubButton asChild>
                <NavLink to={`/session/${session.slug}`}>
                  <span className="flex w-full min-w-0 items-center justify-between gap-2">
                    <span className="truncate">{session.name}</span>
                    {session.isActive ? (
                      <span
                        className="h-2.5 w-2.5 shrink-0 rounded-full bg-green-500"
                        aria-label="Active session"
                      />
                    ) : null}
                  </span>
                </NavLink>
              </SidebarMenuSubButton>
            </SidebarMenuSubItem>
          ))
        )}
      </SidebarMenuSub>
    </SidebarGroup>
  )
}
