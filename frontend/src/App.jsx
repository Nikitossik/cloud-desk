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

export default function App() {
  const { pathname } = useLocation()
  const [isAddSessionOpen, setIsAddSessionOpen] = useState(false)
  const { isAuthenticated, isBootstrapped } = useAuth()
  const canRenderAuthPage = pathname === "/login"

  if (!isBootstrapped) {
    return null
  }

  if (!isAuthenticated || canRenderAuthPage) {
    return (
      <Routes>
        <Route path="/login" element={<AuthPage />} />
        <Route
          path="*"
          element={<Navigate to={isAuthenticated ? "/" : "/login"} replace />}
        />
      </Routes>
    )
  }

  let pageTitle = "CloudDesk"
  if (pathname.startsWith("/session/")) pageTitle = "Session"
  else if (pathname === "/statistics") pageTitle = "Statistics"
  else if (pathname === "/trash") pageTitle = "Trash"

  return (
    <SidebarProvider>
      <AppSidebar onAddSession={() => setIsAddSessionOpen(true)} />
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
          <Route path="/" element={<Navigate to="/statistics" replace />} />
          <Route path="/session/:session_slug" element={<SessionPage />} />
          <Route path="/statistics" element={<StatisticsPage />} />
          <Route path="/trash" element={<TrashPage />} />
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
