import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useForm } from "@tanstack/react-form"
import { useNavigate } from "react-router"
import { z } from "zod"
import {
  createSessionRequest,
  updateSessionByIdRequest,
} from "@/features/session/api/session-api"
import { SESSION_BY_SLUG_QUERY_KEY } from "@/features/session/lib/query-keys"
import { USER_SIDEBAR_QUERY_KEY } from "@/features/user/lib/query-keys"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { SessionForm } from "@/features/session/components/session-form"

const sessionSchema = z.object({
  name: z.string().max(100, "Session name must be at most 100 characters"),
  description: z.string().max(2000, "Description must be at most 2000 characters"),
  start: z.boolean(),
})

function normalizeText(value) {
  const normalized = typeof value === "string" ? value.trim() : ""
  return normalized.length > 0 ? normalized : null
}

export function SessionDialog({
  open,
  onOpenChange,
  mode = "create",
  session,
  sessionSlug,
}) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const isEditMode = mode === "edit"

  const mutation = useMutation({
    mutationFn: async (values) => {
      if (isEditMode) {
        const payload = {
          name: normalizeText(values.name),
          description: normalizeText(values.description),
        }

        return updateSessionByIdRequest(session?.id, payload)
      }

      return createSessionRequest({
        name: normalizeText(values.name),
        description: normalizeText(values.description),
        start: values.start,
      })
    },
  })

  const form = useForm({
    defaultValues: {
      name: session?.name ?? "",
      description: session?.description ?? "",
      start: true,
    },
    validators: {
      onSubmit: sessionSchema,
    },
    onSubmit: async ({ value }) => {
      const response = await mutation.mutateAsync(value)

      if (isEditMode) {
        const previousSlug = sessionSlug || session?.slugname || ""
        const nextSlug = response?.slugname || previousSlug

        if (previousSlug) {
          queryClient.setQueryData(
            SESSION_BY_SLUG_QUERY_KEY(previousSlug),
            (current) => ({ ...(current || {}), ...response }),
          )
        }

        if (nextSlug && nextSlug !== previousSlug) {
          queryClient.setQueryData(
            SESSION_BY_SLUG_QUERY_KEY(nextSlug),
            (current) => ({ ...(current || {}), ...response }),
          )
        }

        queryClient.setQueryData(USER_SIDEBAR_QUERY_KEY, (current) => {
          if (!current || !Array.isArray(current.sessions)) {
            return current
          }

          return {
            ...current,
            sessions: current.sessions.map((item) => {
              const itemSlug = item.slugname || item.slug
              const isTarget =
                (session?.id && item.id && item.id === session.id) ||
                (previousSlug && itemSlug === previousSlug)

              if (!isTarget) {
                return item
              }

              return {
                ...item,
                name: response?.name ?? item.name,
                slugname: response?.slugname ?? item.slugname,
                slug: response?.slugname ?? item.slug,
                is_active:
                  typeof response?.is_active === "boolean"
                    ? response.is_active
                    : item.is_active,
              }
            }),
          }
        })

        if (nextSlug && previousSlug && nextSlug !== previousSlug) {
          navigate(`/session/${nextSlug}`, { replace: true })
        }

        if (sessionSlug) {
          queryClient.invalidateQueries({
            queryKey: SESSION_BY_SLUG_QUERY_KEY(sessionSlug),
          })
        }
        if (response?.slugname) {
          queryClient.invalidateQueries({
            queryKey: SESSION_BY_SLUG_QUERY_KEY(response.slugname),
          })
        }

        queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
      } else {
        queryClient.invalidateQueries({ queryKey: USER_SIDEBAR_QUERY_KEY })
      }

      mutation.reset()
      onOpenChange?.(false)
    },
  })

  const handleOpenChange = (nextOpen) => {
    if (!nextOpen) {
      mutation.reset()
      form.reset()
    }

    onOpenChange?.(nextOpen)
  }

  const mutationError =
    mutation.error?.response?.data?.detail ||
    mutation.error?.message ||
    ""

  const title = isEditMode ? "Edit session" : "Create session"
  const description = isEditMode
    ? "Update session details for the current device."
    : "Create a new session for the current device."
  const submitLabel = mutation.isPending
    ? isEditMode
      ? "Saving..."
      : "Creating..."
    : isEditMode
      ? "Save"
      : "Create"

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>

        <SessionForm
          form={form}
          isSubmitting={mutation.isPending}
          mutationError={mutationError}
          showStart={!isEditMode}
          onCancel={() => handleOpenChange(false)}
          submitLabel={submitLabel}
        />
      </DialogContent>
    </Dialog>
  )
}
