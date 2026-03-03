import { useForm } from "@tanstack/react-form"
import { useEffect } from "react"
import { z } from "zod"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { RadioGroup } from "@/components/ui/radio-group"
import { DeviceResolutionExistingOption } from "@/features/auth/components/device-resolution-existing-option"
import { DeviceResolutionNewDeviceOption } from "@/features/auth/components/device-resolution-new-device-option"

function getDeviceResolutionSchema(allowExistingSelection) {
  return z
    .object({
      choice: z.string().min(1, "Select device option"),
      newDeviceName: z.string().max(60, "Device name must be at most 60 characters"),
    })
    .superRefine((value, ctx) => {
      if (!allowExistingSelection) {
        if (!value.newDeviceName.trim()) {
          ctx.addIssue({
            code: "custom",
            message: "Device name is required",
            path: ["newDeviceName"],
          })
        }
        return
      }

      if (value.choice === "__new__") {
        if (!value.newDeviceName.trim()) {
          ctx.addIssue({
            code: "custom",
            message: "Device name is required for a new device",
            path: ["newDeviceName"],
          })
        }
        return
      }

      if (value.newDeviceName.trim()) {
        ctx.addIssue({
          code: "custom",
          message: "Choose either an existing device or a new device name",
          path: ["newDeviceName"],
        })
      }
    })
}

export function DeviceResolutionDialog({
  open,
  mode,
  devices,
  currentDeviceInfo,
  isLoading,
  errorMessage,
  onSubmitResolution,
  onCancelResolution,
}) {
  const allowExistingSelection = mode === "login"

  const form = useForm({
    defaultValues: {
      choice:
        allowExistingSelection && devices.length === 1 ? String(devices[0].id) : "__new__",
      newDeviceName: "",
    },
    validators: {
      onSubmit: getDeviceResolutionSchema(allowExistingSelection),
    },
    onSubmit: async ({ value }) => {
      if (!allowExistingSelection || value.choice === "__new__") {
        await onSubmitResolution?.({
          action: "create",
          displayName: value.newDeviceName.trim(),
        })
        return
      }

      await onSubmitResolution?.({
        action: "rebind",
        targetDeviceId: value.choice,
      })
    },
  })

  useEffect(() => {
    if (!open) return

    form.reset({
      choice:
        allowExistingSelection && devices.length === 1 ? String(devices[0].id) : "__new__",
      newDeviceName: "",
    })
  }, [open, devices, allowExistingSelection, form])

  if (!open) {
    return null
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(nextOpen) => {
        if (!nextOpen) {
          onCancelResolution?.()
        }
      }}
    >
      <DialogContent className="max-w-xl">
        <DialogHeader>
          <DialogTitle>Device verification required</DialogTitle>
          <DialogDescription>
            {allowExistingSelection
              ? "We couldn't match this fingerprint. Choose an existing device or create a new one."
              : "Set a name for this device to finish registration."}
          </DialogDescription>
        </DialogHeader>

        <form
          onSubmit={(event) => {
            event.preventDefault()
            form.handleSubmit()
          }}
          className="space-y-4"
        >
          {allowExistingSelection ? (
            <>
              <p className="text-sm font-medium">Detected user devices:</p>

              <form.Field
                name="choice"
                children={(field) => (
                  <RadioGroup
                    value={field.state.value}
                    onValueChange={field.handleChange}
                    className="max-h-72 overflow-y-auto pr-1"
                  >
                    {devices.length > 0 ? (
                      devices.map((device) => (
                        <DeviceResolutionExistingOption
                          key={device.id}
                          device={device}
                          checked={field.state.value === String(device.id)}
                        />
                      ))
                    ) : (
                      <p className="text-muted-foreground px-1 text-xs">No saved devices found.</p>
                    )}

                    <p className="mt-2 text-sm font-medium">Or use this current device:</p>

                    <form.Field
                      name="newDeviceName"
                      children={(nameField) => {
                        const firstError = nameField.state.meta.errors?.[0]
                        const errorText =
                          typeof firstError === "string" ? firstError : firstError?.message

                        return (
                          <DeviceResolutionNewDeviceOption
                            value={nameField.state.value}
                            onChange={(event) => nameField.handleChange(event.target.value)}
                            currentDeviceInfo={currentDeviceInfo}
                            checked={field.state.value === "__new__"}
                            error={field.state.value === "__new__" ? errorText : ""}
                            disabled={isLoading}
                          />
                        )
                      }}
                    />
                  </RadioGroup>
                )}
              />
            </>
          ) : (
            <form.Field
              name="newDeviceName"
              children={(nameField) => {
                const firstError = nameField.state.meta.errors?.[0]
                const errorText = typeof firstError === "string" ? firstError : firstError?.message

                return (
                  <DeviceResolutionNewDeviceOption
                    value={nameField.state.value}
                    onChange={(event) => nameField.handleChange(event.target.value)}
                    currentDeviceInfo={currentDeviceInfo}
                    checked
                    error={errorText}
                    disabled={isLoading}
                    showSelector={false}
                  />
                )
              }}
            />
          )}

          {errorMessage ? (
            <Textarea
              readOnly
              className="min-h-0 resize-none text-sm"
              value={String(errorMessage)}
            />
          ) : null}

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onCancelResolution?.()}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Please wait..." : "Continue"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
