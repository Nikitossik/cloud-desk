import { useParams } from "react-router"

export function DevicePage() {
  const { device_id } = useParams()

  return (
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <h1 className="text-2xl font-semibold">Device: {device_id}</h1>
    </div>
  )
}
