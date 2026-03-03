import { DevicesNavGroup } from "@/components/navbar/devices-nav-group"
import { SessionsNavGroup } from "@/components/navbar/sessions-nav-group"
import { StatisticsNavGroup } from "@/components/navbar/statistics-nav-group"

export function NavMain({ onAddSession }) {
  return (
    <>
      <DevicesNavGroup />
      <SessionsNavGroup onAddSession={onAddSession} />
      <StatisticsNavGroup />
    </>
  )
}
