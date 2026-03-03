import { useEffect } from "react"
import { useForm } from "@tanstack/react-form"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

const loginSchema = z.object({
  email: z.string().trim().email("Enter a valid email"),
  password: z
    .string()
    .min(6, "Password must be at least 6 characters")
    .regex(/^\S+$/, "Password must not contain spaces"),
})

const signupSchema = loginSchema.extend({
  name: z.string().trim().min(1, "Name is required"),
  surname: z.string().trim().min(1, "Surname is required"),
})

export function AuthCredentialsForm({
  mode,
  isLoading,
  errorMessage,
  onSubmitValues,
}) {
  const form = useForm({
    defaultValues: {
      name: "",
      surname: "",
      email: "",
      password: "",
    },
    validators: {
      onSubmit: mode === "signup" ? signupSchema : loginSchema,
    },
    onSubmit: async ({ value }) => {
      await onSubmitValues?.({
        name: value.name.trim(),
        surname: value.surname.trim(),
        email: value.email.trim(),
        password: value.password,
      })
    },
  })

  useEffect(() => {
    form.reset()
  }, [mode])

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault()
        form.handleSubmit()
      }}
      className="space-y-4"
    >
      {mode === "signup" && (
        <>
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
                    placeholder="John"
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
                    placeholder="Doe"
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
        </>
      )}

      <form.Field
        name="email"
        children={(field) => {
          const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
          const firstError = field.state.meta.errors?.[0]
          const errorText =
            typeof firstError === "string"
              ? firstError
              : firstError?.message

          return (
            <div className="space-y-2">
              <label className="text-sm font-medium">Email</label>
              <Input
                type="email"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(event) => field.handleChange(event.target.value)}
                placeholder="john@company.com"
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
                placeholder="••••••••"
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

      {errorMessage ? <p className="text-destructive text-sm">{String(errorMessage)}</p> : null}

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? "Please wait..." : mode === "login" ? "Log in" : "Create account"}
      </Button>
    </form>
  )
}
