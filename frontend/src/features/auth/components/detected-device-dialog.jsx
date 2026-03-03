import { useForm } from "@tanstack/react-form"
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
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

const deviceNameSchema = z.object({
  deviceName: z
    .string()
    .max(60, "Device name must be at most 60 characters")
    .refine(
      (value) => value.length === 0 || value.trim().length > 0,
      "Device name must not be only spaces"
    ),
})

export function DetectedDeviceDialog({
  open,
  detectedDevice,
  initialDeviceName,
  isLoading,
  errorMessage,
  onSubmitDeviceName,
}) {
  const form = useForm({
    defaultValues: {
      deviceName: initialDeviceName ?? "",
    },
    validators: {
      onSubmit: deviceNameSchema,
    },
    onSubmit: async ({ value }) => {
      await onSubmitDeviceName?.(value.deviceName.trim())
    },
  })

  if (!open) {
    return null
  }

  return (
    <Dialog open={open} onOpenChange={() => {}}>
      <DialogContent showCloseButton={false}>
        <DialogHeader>
          <DialogTitle>Detected device</DialogTitle>
          <DialogDescription>
            We detected this device. You can provide a name before entering the app.
          </DialogDescription>
        </DialogHeader>

        <form
          onSubmit={(event) => {
            event.preventDefault()
            form.handleSubmit()
          }}
          className="space-y-4"
        >
          <div className="rounded-md border p-3 text-sm space-y-1">
            <p><span className="font-medium">OS:</span> {detectedDevice?.os_name || "-"}</p>
            <p><span className="font-medium">Release:</span> {detectedDevice?.os_release || "-"}</p>
            <p><span className="font-medium">Architecture:</span> {detectedDevice?.architecture || "-"}</p>
          </div>

          <form.Field
            name="deviceName"
            children={(field) => {
              const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
              const firstError = field.state.meta.errors?.[0]
              const errorText =
                typeof firstError === "string"
                  ? firstError
                  : firstError?.message

              return (
                <div className="space-y-2">
                  <label className="text-sm font-medium">Device name</label>
                  <Input
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(event) => field.handleChange(event.target.value)}
                    placeholder="My Windows PC"
                    disabled={isLoading}
                    aria-invalid={isInvalid}
                  />
                  {isInvalid && errorText && (
                    <p className="text-destructive text-xs">{errorText}</p>
                  )}
                </div>
              )
            }}
          />

          {errorMessage && (
            <Textarea
              readOnly
              className="min-h-0 resize-none text-sm"
              value={String(errorMessage)}
            />
          )}

          <DialogFooter>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Please wait..." : "Enter app"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
