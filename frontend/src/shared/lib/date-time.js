import { format } from "date-fns"

export function formatUiDateTime(value) {
  if (!value) return "-"

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return "-"

  return format(date, "MMM dd yyyy, HH:mm:ss")
}
