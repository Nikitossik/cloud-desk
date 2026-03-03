import {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldLabel,
  FieldTitle,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { RadioGroupItem } from "@/components/ui/radio-group"

export function DeviceResolutionNewDeviceOption({
  value,
  onChange,
  currentDeviceInfo,
  checked,
  error,
  disabled,
  showSelector = true,
}) {
  const inputId = "device-option-new"

  return (
    <FieldLabel htmlFor={inputId}>
      <Field orientation="horizontal" data-state={checked ? "checked" : "unchecked"}>
        <FieldContent>
          <FieldTitle>This is a new device</FieldTitle>
          <FieldDescription>
            OS: {currentDeviceInfo?.os_name || "-"} • Release: {currentDeviceInfo?.os_release || "-"} • Architecture: {currentDeviceInfo?.architecture || "-"}
          </FieldDescription>
          <Input
            value={value}
            onChange={onChange}
            placeholder="Device name"
            disabled={disabled}
            className="mt-2"
            onClick={(event) => event.stopPropagation()}
          />
          {error ? <FieldError>{error}</FieldError> : null}
        </FieldContent>
        {showSelector ? <RadioGroupItem value="__new__" id={inputId} /> : null}
      </Field>
    </FieldLabel>
  )
}
