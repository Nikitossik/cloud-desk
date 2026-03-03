import { useMutation, useQueryClient } from "@tanstack/react-query"
import { updateMeRequest } from "@/features/user/api/user-api"
import { USER_PROFILE_QUERY_KEY } from "@/features/user/lib/query-keys"

export function useUpdateUserProfileMutation(options = {}) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload) => updateMeRequest(payload),
    ...options,
    onSuccess: async (data, variables, context) => {
      queryClient.setQueryData(USER_PROFILE_QUERY_KEY, data)
      await options.onSuccess?.(data, variables, context)
    },
  })
}
