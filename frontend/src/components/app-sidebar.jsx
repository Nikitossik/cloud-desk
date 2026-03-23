"use client"

import {
  GalleryVerticalEnd,
  Trash2,
} from "lucide-react"
import { NavLink } from "react-router"
import { Badge } from "@/components/ui/badge"
import { useUserSidebarQuery } from "@/features/user/hooks/use-user-sidebar-query"

import { NavMain } from "@/components/navbar/nav-main"
import { NavUser } from "@/components/nav-user"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"

export function AppSidebar({
  onAddSession,
  ...props
}) {
  const { data: sidebarData } = useUserSidebarQuery()
  const deletedSessionsCount = Number(sidebarData?.deleted_sessions_count || 0)

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" className="cursor-default">
              <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                <GalleryVerticalEnd className="size-4" />
              </div>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-semibold">CloudDesk</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain onAddSession={onAddSession} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip="Trash">
              <NavLink to="/trash">
                <Trash2 />
                <span className="flex w-full min-w-0 items-center justify-between gap-2">
                  <span>Trash</span>
                  {deletedSessionsCount > 0 ? (
                    <Badge variant="secondary" className="px-1.5 py-0 text-[10px]">
                      {deletedSessionsCount}
                    </Badge>
                  ) : null}
                </span>
              </NavLink>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
        <NavUser />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
