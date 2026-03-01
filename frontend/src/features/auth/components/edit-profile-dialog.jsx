import { useEffect, useState } from "react"
import { useMutation } from "react-query"
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
import { useAuth } from "@/features/auth/hooks/use-auth"
import { updateMeRequest } from "@/features/auth/api/auth-api"

const editProfileSchema = z.object({
  name: z.string().trim().min(1, "Name is required"),
  surname: z.string().trim().min(1, "Surname is required"),
})

function getNameError(value) {
  const result = z.string().trim().min(1, "Name is required").safeParse(value)
  if (result.success) return ""
  return result.error.issues[0]?.message ?? "Name is required"
}

function getSurnameError(value) {
  const result = z.string().trim().min(1, "Surname is required").safeParse(value)
  if (result.success) return ""
  return result.error.issues[0]?.message ?? "Surname is required"
}

function getPasswordError(value) {
  const rawPassword = value ?? ""
  const trimmedPassword = rawPassword.trim()

  if (rawPassword.length === 0) {
    return ""
  }

  if (trimmedPassword.length === 0) {
    return "Password must not contain spaces"
  }

  if (/\s/.test(rawPassword)) {
    return "Password must not contain spaces"
  }

  if (trimmedPassword.length < 6) {
    return "Password must be at least 6 characters"
  }

  return ""
}

export function EditProfileDialog({ open, onOpenChange }) {
  const { userProfile, refreshUserProfile } = useAuth()
  const [name, setName] = useState("")
  const [surname, setSurname] = useState("")
  const [password, setPassword] = useState("")
  const [fieldErrors, setFieldErrors] = useState({})
  const [submitError, setSubmitError] = useState("")

  useEffect(() => {
    if (!open) return

    setName(userProfile?.name ?? "")
    setSurname(userProfile?.surname ?? "")
    setPassword("")
    setFieldErrors({})
    setSubmitError("")
  }, [open, userProfile])

  const updateProfileMutation = useMutation(
    async (payload) => updateMeRequest(payload),
    {
      onSuccess: async () => {
        await refreshUserProfile()
        onOpenChange(false)
      },
      onError: (error) => {
        const message =
          error?.response?.data?.detail ||
          error?.message ||
          "Failed to update profile"

        setSubmitError(String(message))
      },
    }
  )

  const handleSubmit = (event) => {
    event.preventDefault()
    const passwordError = getPasswordError(password)
    setSubmitError("")

    const validationResult = editProfileSchema.safeParse({
      name,
      surname,
    })

    if (!validationResult.success || passwordError) {
      const flattened = validationResult.success
        ? { name: [], surname: [] }
        : z.flattenError(validationResult.error).fieldErrors

      setFieldErrors({
        name: flattened.name?.[0] ?? "",
        surname: flattened.surname?.[0] ?? "",
        password: passwordError,
      })
      return
    }

    const trimmedName = validationResult.data.name.trim()
    const trimmedSurname = validationResult.data.surname.trim()
    const trimmedPassword = password.trim()

    const payload = {
      name: trimmedName,
      surname: trimmedSurname,
      ...(trimmedPassword ? { password: trimmedPassword } : {}),
    }

    updateProfileMutation.mutate(payload)
  }

  const handleNameChange = (event) => {
    const nextValue = event.target.value
    setName(nextValue)
    setFieldErrors((prev) => ({
      ...prev,
      name: getNameError(nextValue),
    }))
  }

  const handleSurnameChange = (event) => {
    const nextValue = event.target.value
    setSurname(nextValue)
    setFieldErrors((prev) => ({
      ...prev,
      surname: getSurnameError(nextValue),
    }))
  }

  const handlePasswordChange = (event) => {
    const nextValue = event.target.value
    setPassword(nextValue)
    setFieldErrors((prev) => ({
      ...prev,
      password: "",
    }))
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

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label className="text-sm font-medium">Name</label>
            <Input
              value={name}
              onChange={handleNameChange}
              placeholder="Name"
              disabled={updateProfileMutation.isLoading}
            />
            {fieldErrors.name && (
              <p className="text-destructive text-xs">{fieldErrors.name}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Surname</label>
            <Input
              value={surname}
              onChange={handleSurnameChange}
              placeholder="Surname"
              disabled={updateProfileMutation.isLoading}
            />
            {fieldErrors.surname && (
              <p className="text-destructive text-xs">{fieldErrors.surname}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Password</label>
            <Input
              type="password"
              value={password}
              onChange={handlePasswordChange}
              placeholder="Leave empty to keep current password"
              disabled={updateProfileMutation.isLoading}
            />
            {fieldErrors.password && (
              <p className="text-destructive text-xs">{fieldErrors.password}</p>
            )}
          </div>

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
