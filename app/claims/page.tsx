import { AppSidebar } from "@/components/layout/app-sidebar"
import { AppHeader } from "@/components/layout/app-header"
import { ClaimsTable } from "@/components/claims/claims-table"
import { ClaimStats } from "@/components/claims/claim-stats"
import { Button } from "@/components/ui/button"
import { claimsAPI } from "@/lib/mock-api"
import { Plus, Download } from "lucide-react"

export default async function ClaimsPage() {
  const claims = await claimsAPI.getAll()

  return (
    <div className="flex h-screen bg-background">
      <AppSidebar />

      <div className="flex flex-1 flex-col overflow-hidden">
        <AppHeader />

        <main className="flex-1 overflow-y-auto p-6">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Claims Management</h1>
              <p className="text-muted-foreground">
                Track and manage reimbursement claims with real-time variance analysis
              </p>
            </div>

            <div className="flex gap-2">
              <Button variant="outline">
                <Download className="mr-2 h-4 w-4" />
                Export
              </Button>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                New Claim
              </Button>
            </div>
          </div>

          <div className="space-y-6">
            <ClaimStats claims={claims} />
            <ClaimsTable claims={claims} />
          </div>
        </main>
      </div>
    </div>
  )
}
