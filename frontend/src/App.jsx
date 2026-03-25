import { AppSidebar } from "@/components/app-sidebar"
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbPage,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { Navigate, Route, Routes, useLocation } from "react-router"
import { useState } from "react"
import { useAuth } from "@/features/auth/hooks/use-auth"
import { SessionPage } from "@/pages/session/session-page"
import { StatisticsPage } from "@/pages/statistics/statistics-page"
import { TrashPage } from "@/pages/trash/trash-page"
import { AuthPage } from "@/features/auth/pages/auth-page"
import { SessionDialog } from "@/features/session/components/session-dialog"
import { NotFoundPage } from "@/pages/not-found/not-found-page"
import { UnsupportedDevicePage } from "@/pages/unsupported-device/unsupported-device-page"
import { useUserSidebarQuery } from "@/features/user/hooks/use-user-sidebar-query"

export default function App() {
  const { pathname } = useLocation()
  const [isAddSessionOpen, setIsAddSessionOpen] = useState(false)
  const { isAuthenticated, isBootstrapped } = useAuth()
  const { data: sidebarData, isLoading: isSidebarLoading } = useUserSidebarQuery()
  const canRenderAuthPage = pathname === "/login"

  if (!isBootstrapped) {
    return null
  }

  if (!isAuthenticated) {
    return (
      <Routes>
        <Route path="/login" element={<AuthPage />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  if (canRenderAuthPage) {
    return (
      <Routes>
        <Route path="/login" element={<AuthPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    )
  }

  if (isSidebarLoading) {
    return null
  }

  const currentDevice = Array.isArray(sidebarData?.devices)
    ? sidebarData.devices.find((device) => device?.is_current) || null
    : null
  const isSupportedOs = currentDevice?.is_supported_os !== false
  const isUnsupportedOs = !isSupportedOs
  const unsupportedDeviceOs = currentDevice?.os_name
  const unsupportedReason = currentDevice?.unsupported_reason

  let pageTitle = "CloudDesk"
  if (pathname.startsWith("/session/")) pageTitle = "Session"
  else if (pathname === "/statistics") pageTitle = "Statistics"
  else if (pathname === "/trash") pageTitle = "Trash"
  else if (pathname === "/unsupported-device") pageTitle = "Unsupported device"

  return (
    <SidebarProvider>
      <AppSidebar
        onAddSession={() => setIsAddSessionOpen(true)}
        isSupportedOs={isSupportedOs}
      />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" />
            <Separator
              orientation="vertical"
              className="mr-2 data-[orientation=vertical]:h-4"
            />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbPage>{pageTitle}</BreadcrumbPage>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
        </header>
        <Routes>
          <Route path="/login" element={<Navigate to="/" replace />} />
          <Route
            path="/"
            element={<Navigate to={isUnsupportedOs ? "/unsupported-device" : "/statistics"} replace />}
          />
          <Route
            path="/session/:session_slug"
            element={isUnsupportedOs ? <Navigate to="/unsupported-device" replace /> : <SessionPage />}
          />
          <Route
            path="/session/trash/:session_slug"
            element={isUnsupportedOs ? <Navigate to="/unsupported-device" replace /> : <SessionPage />}
          />
          <Route
            path="/statistics"
            element={isUnsupportedOs ? <Navigate to="/unsupported-device" replace /> : <StatisticsPage />}
          />
          <Route
            path="/trash"
            element={isUnsupportedOs ? <Navigate to="/unsupported-device" replace /> : <TrashPage />}
          />
          <Route
            path="/unsupported-device"
            element={
              isUnsupportedOs ? (
                <UnsupportedDevicePage
                  deviceOs={unsupportedDeviceOs}
                  reason={unsupportedReason}
                />
              ) : (
                <Navigate to="/statistics" replace />
              )
            }
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </SidebarInset>
      <SessionDialog
        open={isAddSessionOpen}
        onOpenChange={setIsAddSessionOpen}
        mode="create"
      />
    </SidebarProvider>
  )
}
