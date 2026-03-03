import { useEffect } from "react"
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
import { useUserProfileQuery } from "@/features/user/hooks/use-user-profile-query"
import { useUpdateUserProfileMutation } from "@/features/user/hooks/use-update-user-profile-mutation"

const editProfileSchema = z.object({
  name: z.string().trim().min(1, "Name is required"),
  surname: z.string().trim().min(1, "Surname is required"),
  password: z
    .string()
    .refine(
      (value) => value.length === 0 || value.trim().length > 0,
      "Password must not contain spaces"
    )
    .refine(
      (value) => value.length === 0 || !/\s/.test(value),
      "Password must not contain spaces"
    )
    .refine(
      (value) => value.length === 0 || value.length >= 6,
      "Password must be at least 6 characters"
    ),
})

export function EditProfileDialog({ open, onOpenChange }) {
  const { data: userProfile } = useUserProfileQuery()
  const form = useForm({
    defaultValues: {
      name: userProfile?.name ?? "",
      surname: userProfile?.surname ?? "",
      password: "",
    },
    validators: {
      onSubmit: editProfileSchema,
    },
    onSubmit: async ({ value }) => {
      const trimmedPassword = value.password.trim()
      const payload = {
        name: value.name.trim(),
        surname: value.surname.trim(),
        ...(trimmedPassword ? { password: trimmedPassword } : {}),
      }

      await updateProfileMutation.mutateAsync(payload)
    },
  })

  const updateProfileMutation = useUpdateUserProfileMutation({
    onSuccess: async () => {
      onOpenChange(false)
    },
  })

  useEffect(() => {
    if (!open) return

    form.reset({
      name: userProfile?.name ?? "",
      surname: userProfile?.surname ?? "",
      password: "",
    })
  }, [open, userProfile, form])

  const submitError =
    updateProfileMutation.error?.response?.data?.detail ||
    updateProfileMutation.error?.message ||
    ""

  if (!open) {
    return null
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit profile</DialogTitle>
          <DialogDescription>
            Update your name, surname and password.
          </DialogDescription>
        </DialogHeader>

        <form
          className="space-y-4"
          onSubmit={(event) => {
            event.preventDefault()
            form.handleSubmit()
          }}
        >
          <form.Field
            name="name"
            children={(field) => {
              const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
              const firstError = field.state.meta.errors?.[0]
              const errorText =
                typeof firstError === "string"
                  ? firstError
                  : firstError?.message

              return (
                <div className="space-y-2">
                  <label className="text-sm font-medium">Name</label>
                  <Input
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(event) => field.handleChange(event.target.value)}
                    placeholder="Name"
                    disabled={updateProfileMutation.isLoading}
                    aria-invalid={isInvalid}
                  />
                  {isInvalid && errorText && (
                    <p className="text-destructive text-xs">{errorText}</p>
                  )}
                </div>
              )
            }}
          />

          <form.Field
            name="surname"
            children={(field) => {
              const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
              const firstError = field.state.meta.errors?.[0]
              const errorText =
                typeof firstError === "string"
                  ? firstError
                  : firstError?.message

              return (
                <div className="space-y-2">
                  <label className="text-sm font-medium">Surname</label>
                  <Input
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(event) => field.handleChange(event.target.value)}
                    placeholder="Surname"
                    disabled={updateProfileMutation.isLoading}
                    aria-invalid={isInvalid}
                  />
                  {isInvalid && errorText && (
                    <p className="text-destructive text-xs">{errorText}</p>
                  )}
                </div>
              )
            }}
          />

          <form.Field
            name="password"
            children={(field) => {
              const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
              const firstError = field.state.meta.errors?.[0]
              const errorText =
                typeof firstError === "string"
                  ? firstError
                  : firstError?.message

              return (
                <div className="space-y-2">
                  <label className="text-sm font-medium">Password</label>
                  <Input
                    type="password"
                    value={field.state.value}
                    onBlur={field.handleBlur}
                    onChange={(event) => field.handleChange(event.target.value)}
                    placeholder="Leave empty to keep current password"
                    disabled={updateProfileMutation.isLoading}
                    aria-invalid={isInvalid}
                  />
                  {isInvalid && errorText && (
                    <p className="text-destructive text-xs">{errorText}</p>
                  )}
                </div>
              )
            }}
          />

          {submitError && (
            <p className="text-destructive text-sm">{submitError}</p>
          )}

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={updateProfileMutation.isLoading}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={updateProfileMutation.isLoading}>
              {updateProfileMutation.isLoading ? "Updating..." : "Update"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
