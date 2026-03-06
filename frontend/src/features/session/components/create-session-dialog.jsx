import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useForm } from "@tanstack/react-form"
import { z } from "zod"
import { createSessionRequest } from "@/features/session/api/session-api"
import { USER_SIDEBAR_QUERY_KEY } from "@/features/user/lib/query-keys"
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

const createSessionSchema = z.object({
  name: z.string().max(100, "Session name must be at most 100 characters"),
  description: z.string().max(2000, "Description must be at most 2000 characters"),
  start: z.boolean(),
})

export function CreateSessionDialog({ open, onOpenChange }) {
  const queryClient = useQueryClient()

  const createSessionMutation = useMutation({
    mutationFn: (values) =>
      createSessionRequest({
        name: values.name,
        description: values.description,
        start: values.start,
      }),
  })

  const form = useForm({
    defaultValues: {
      name: "",
      description: "",
      start: true,
    },
    validators: {
      onSubmit: createSessionSchema,
    },
    onSubmit: async ({ value }) => {
      await createSessionMutation.mutateAsync(value)

      await queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
      form.reset()
      onOpenChange?.(false)
    },
  })

  const handleOpenChange = (nextOpen) => {
    if (!nextOpen) {
      createSessionMutation.reset()
      form.reset()
    }

    onOpenChange?.(nextOpen)
  }

  const isSubmitting = createSessionMutation.isPending
  const mutationError =
    createSessionMutation.error?.response?.data?.detail ||
    createSessionMutation.error?.message ||
    ""

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Create session</DialogTitle>
          <DialogDescription>
            Create a new session for the current device.
          </DialogDescription>
        </DialogHeader>

        <form
          onSubmit={(event) => {
            event.preventDefault()
            form.handleSubmit()
          }}
          className="space-y-4"
        >
          <form.Field
            name="name"
            children={(field) => {
              const firstError = field.state.meta.errors?.[0]
              const errorText =
                typeof firstError === "string"
                  ? firstError
                  : firstError?.message

              return (
                <div className="space-y-2">
                  <label className="text-sm font-medium">Session name</label>
                  <Input
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(event) => field.handleChange(event.target.value)}
                    placeholder="My work session"
                    disabled={isSubmitting}
                    aria-invalid={field.state.meta.isTouched && !field.state.meta.isValid}
                  />
                  <p className="text-muted-foreground text-xs">
                    If name is empty it will be generated automatically.
                  </p>
                  {errorText ? <p className="text-destructive text-xs">{errorText}</p> : null}
                </div>
              )
            }}
          />

          <form.Field
            name="description"
            children={(field) => {
              const firstError = field.state.meta.errors?.[0]
              const errorText =
                typeof firstError === "string"
                  ? firstError
                  : firstError?.message

              return (
                <div className="space-y-2">
                  <label className="text-sm font-medium">Description</label>
                  <Textarea
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(event) => field.handleChange(event.target.value)}
                    placeholder="Optional session description"
                    disabled={isSubmitting}
                    className="min-h-24"
                  />
                  {errorText ? <p className="text-destructive text-xs">{errorText}</p> : null}
                </div>
              )
            }}
          />

          <form.Field
            name="start"
            children={(field) => (
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={field.state.value}
                  onChange={(event) => field.handleChange(event.target.checked)}
                  disabled={isSubmitting}
                  className="accent-foreground"
                />
                Start right away
              </label>
            )}
          />

          {mutationError ? <p className="text-destructive text-sm">{String(mutationError)}</p> : null}

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => handleOpenChange(false)}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Creating..." : "Create"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
