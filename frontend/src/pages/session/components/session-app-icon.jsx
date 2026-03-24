import { useEffect, useState } from "react"
import { AppWindow } from "lucide-react"
import { http } from "@/shared/api/http-client"

export function SessionAppIcon({ appId, appName, isSessionDeleted = false }) {
  const [iconSrc, setIconSrc] = useState(null)

  useEffect(() => {
    let isMounted = true
    let objectUrl = null

    if (!appId) {
      setIconSrc(null)
      return () => {}
    }

    http
      .get(`/device/apps/${appId}/icon`, { responseType: "blob" })
      .then(({ data }) => {
        objectUrl = URL.createObjectURL(data)
        if (isMounted) {
          setIconSrc(objectUrl)
        }
      })
      .catch(() => {
        if (isMounted) {
          setIconSrc(null)
        }
      })

    return () => {
      isMounted = false
      if (objectUrl) {
        URL.revokeObjectURL(objectUrl)
      }
    }
  }, [appId])

  if (!iconSrc) {
    return (
      <div className={`bg-muted rounded-md p-2 ${isSessionDeleted ? "grayscale" : ""}`}>
        <AppWindow className={`text-muted-foreground size-4 ${isSessionDeleted ? "opacity-75" : ""}`} />
      </div>
    )
  }

  return (
    <img
      src={iconSrc}
      alt={appName}
      className={`size-6 rounded-md object-contain ${isSessionDeleted ? "grayscale opacity-80" : ""}`}
      onError={() => setIconSrc(null)}
    />
  )
}
