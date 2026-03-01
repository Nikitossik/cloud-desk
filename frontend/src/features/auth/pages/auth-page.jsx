import { useState } from "react"
import { Navigate, useNavigate } from "react-router"
import { useMutation } from "react-query"

import { useAuth } from "@/features/auth/hooks/use-auth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

export function AuthPage() {
  const navigate = useNavigate()
  const { isAuthenticated, login, signup } = useAuth()

  const [mode, setMode] = useState("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [name, setName] = useState("")
  const [surname, setSurname] = useState("")

  const loginMutation = useMutation(async () => login(email, password), {
    onSuccess: () => {
      navigate("/device/current-device", { replace: true })
    },
  })

  const signupMutation = useMutation(
    async () =>
      signup({
        name,
        surname,
        email,
        password,
      }),
    {
      onSuccess: () => {
        navigate("/device/current-device", { replace: true })
      },
    }
  )

  if (isAuthenticated) {
    return <Navigate to="/device/current-device" replace />
  }

  const isLoading = loginMutation.isLoading || signupMutation.isLoading
  const errorMessage =
    loginMutation.error?.response?.data?.detail ||
    signupMutation.error?.response?.data?.detail ||
    loginMutation.error?.message ||
    signupMutation.error?.message

  const handleSubmit = (event) => {
    event.preventDefault()

    if (mode === "login") {
      loginMutation.mutate()
      return
    }

    signupMutation.mutate()
  }

  return (
    <div className="flex min-h-svh items-center justify-center p-4">
      <div className="bg-card text-card-foreground w-full max-w-md rounded-xl border p-6">
        <div className="mb-6 space-y-1">
          <h1 className="text-2xl font-semibold">Cloud Desk</h1>
          <p className="text-muted-foreground text-sm">
            {mode === "login" ? "Log in to continue" : "Create a new account"}
          </p>
        </div>

        <div className="mb-4 grid grid-cols-2 gap-2">
          <Button
            type="button"
            variant={mode === "login" ? "default" : "outline"}
            onClick={() => setMode("login")}
            disabled={isLoading}
          >
            Login
          </Button>
          <Button
            type="button"
            variant={mode === "signup" ? "default" : "outline"}
            onClick={() => setMode("signup")}
            disabled={isLoading}
          >
            Sign up
          </Button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === "signup" && (
            <>
              <div className="space-y-2">
                <label className="text-sm font-medium">Name</label>
                <Input
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  placeholder="John"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Surname</label>
                <Input
                  value={surname}
                  onChange={(event) => setSurname(event.target.value)}
                  placeholder="Doe"
                />
              </div>
            </>
          )}

          <div className="space-y-2">
            <label className="text-sm font-medium">Email</label>
            <Input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="john@company.com"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Password</label>
            <Input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="••••••••"
            />
          </div>

          {errorMessage && (
            <Textarea
              readOnly
              className="min-h-0 resize-none text-sm"
              value={String(errorMessage)}
            />
          )}

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Please wait..." : mode === "login" ? "Log in" : "Create account"}
          </Button>
        </form>
      </div>
    </div>
  )
}
