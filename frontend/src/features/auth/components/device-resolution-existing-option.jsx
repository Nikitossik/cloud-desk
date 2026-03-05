import {
  Field,
  FieldContent,
  FieldDescription,
  FieldLabel,
  FieldTitle,
} from "@/components/ui/field"
import { RadioGroupItem } from "@/components/ui/radio-group"
import { formatUiDateTime } from "@/shared/lib/date-time"

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
            Created: {formatUiDateTime(device.created_at)} • Last seen: {formatUiDateTime(device.last_seen_at)}
          </FieldDescription>
        </FieldContent>
        <RadioGroupItem value={device.id} id={inputId} />
      </Field>
    </FieldLabel>
  )
}
