import {
  Field,
  FieldContent,
  FieldDescription,
  FieldLabel,
  FieldTitle,
} from "@/components/ui/field"
import { RadioGroupItem } from "@/components/ui/radio-group"

function formatDate(value) {
  if (!value) return "-"
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return "-"

  const datePart = date
    .toLocaleDateString("en-US", {
      month: "short",
      day: "2-digit",
      year: "numeric",
    })
    .replace(",", "")

  const timePart = date.toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  })

  return `${datePart}, ${timePart}`
}

export function DeviceResolutionExistingOption({ device, checked }) {
  const inputId = `device-option-${device.id}`
  const title = device.display_name || "Unnamed device"

  return (
    <FieldLabel htmlFor={inputId}>
      <Field orientation="horizontal" data-state={checked ? "checked" : "unchecked"}>
        <FieldContent>
          <FieldTitle>{title}</FieldTitle>
          <FieldDescription>
            OS: {device.os_name || "-"} • Release: {device.os_release || "-"} • Architecture: {device.architecture || "-"}
          </FieldDescription>
          <FieldDescription className="text-xs">
            Created: {formatDate(device.created_at)} • Last seen: {formatDate(device.last_seen_at)}
          </FieldDescription>
        </FieldContent>
        <RadioGroupItem value={device.id} id={inputId} />
      </Field>
    </FieldLabel>
  )
}
