import { format, isToday } from "date-fns"

export function formatUiDateTime(value, options = {}) {
  const { withSeconds = true, todayAsTime = false } = options

  if (!value) return "-"

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return "-"

  if (todayAsTime && isToday(date)) {
    return format(date, withSeconds ? "HH:mm:ss" : "HH:mm")
  }

  return format(date, withSeconds ? "MMM dd yyyy, HH:mm:ss" : "MMM dd yyyy, HH:mm")
}
