import { format, formatDuration, intervalToDuration, isToday } from "date-fns"

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

function compactDurationLabel(value) {
  return value
    .replace(/(\d+)\s*hours?/g, "$1h")
    .replace(/(\d+)\s*minutes?/g, "$1m")
    .replace(/(\d+)\s*seconds?/g, "$1s")
    .trim()
}

export function formatUiDurationSeconds(totalSeconds) {
  const value = Math.floor(Number(totalSeconds || 0))

  if (value <= 0) {
    return "0m"
  }

  const duration = intervalToDuration({
    start: 0,
    end: value * 1000,
  })

  if ((duration.hours || 0) > 0) {
    return compactDurationLabel(
      formatDuration(duration, {
        format: ["hours", "minutes"],
        delimiter: " ",
        zero: true,
      }),
    )
  }

  if ((duration.minutes || 0) > 0) {
    return compactDurationLabel(
      formatDuration(duration, {
        format: ["minutes", "seconds"],
        delimiter: " ",
        zero: true,
      }),
    )
  }

  return compactDurationLabel(
    formatDuration(duration, {
      format: ["seconds"],
      delimiter: " ",
      zero: true,
    }),
  )
}
