import {
  Pencil,
  RotateCcw,
  Trash2,
  Ellipsis,
} from "lucide-react"
import { FaPlay, FaPause } from "react-icons/fa"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function SessionActions({
  isDeleted,
  isActive,
  isUpdateDeletedPending,
  isSessionActionPending,
  isRestorePending,
  onRestoreFromTrash,
  onToggleStartStop,
  onRestore,
  onEdit,
  onMoveToTrash,
}) {
  return (
    <div className="flex items-center gap-2">
      {isDeleted ? (
        <Button
          variant="outline"
          className="gap-2"
          disabled={isUpdateDeletedPending}
          onClick={onRestoreFromTrash}
        >
          <RotateCcw className="size-4" />
          {isUpdateDeletedPending ? "Restoring from Trash..." : "Restore from Trash"}
        </Button>
      ) : (
        <>
          <Button
            className="gap-2 cursor-pointer"
            disabled={isSessionActionPending}
            onClick={onToggleStartStop}
          >
            {isActive ? (
              <FaPause className="size-3" />
            ) : (
              <FaPlay className="size-3" />
            )}
            {isActive ? "Stop" : "Start"}
          </Button>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" className="gap-2">
                <Ellipsis className="size-4" />
                Actions
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              {!isActive ? (
                <DropdownMenuItem
                  disabled={isRestorePending}
                  onClick={(event) => {
                    event.preventDefault()
                    onRestore?.()
                  }}
                >
                  <RotateCcw />
                  {isRestorePending ? "Restoring..." : "Restore"}
                </DropdownMenuItem>
              ) : null}
              <DropdownMenuItem
                onClick={(event) => {
                  event.preventDefault()
                  onEdit?.()
                }}
              >
                <Pencil />
                Edit
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                variant="destructive"
                disabled={isUpdateDeletedPending}
                onClick={(event) => {
                  event.preventDefault()
                  onMoveToTrash?.()
                }}
              >
                <Trash2 />
                {isUpdateDeletedPending ? "Moving..." : "Move to Trash"}
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </>
      )}
    </div>
  )
}
