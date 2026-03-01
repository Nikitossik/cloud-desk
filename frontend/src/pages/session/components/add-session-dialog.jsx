import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

export function AddSessionDialog({ open, onOpenChange }) {
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")

  const handleSubmit = (event) => {
    event.preventDefault()
    console.log("[AddSessionDialog] submit", { name, description })
    onOpenChange(false)
    setName("")
    setDescription("")
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add new session</DialogTitle>
          <DialogDescription>
            Create a new session with name and description.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="grid gap-4">
          <div className="grid gap-2">
            <label htmlFor="session-name" className="text-sm font-medium">
              Name
            </label>
            <Input
              id="session-name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="My work session"
            />
          </div>

          <div className="grid gap-2">
            <label htmlFor="session-description" className="text-sm font-medium">
              Description
            </label>
            <Textarea
              id="session-description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Session description"
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit">Add session</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
