import { Button } from "@/components/ui/button"
import { DialogFooter } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

export function SessionForm({
  form,
  isSubmitting,
  mutationError,
  showStart,
  onCancel,
  submitLabel,
}) {
  return (
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
            typeof firstError === "string" ? firstError : firstError?.message

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
                Leave empty to use server defaults.
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
            typeof firstError === "string" ? firstError : firstError?.message

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

      {showStart ? (
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
      ) : null}

      {mutationError ? <p className="text-destructive text-sm">{String(mutationError)}</p> : null}

      <DialogFooter>
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {submitLabel}
        </Button>
      </DialogFooter>
    </form>
  )
}
