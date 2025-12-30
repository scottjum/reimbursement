import { AppSidebar } from "@/components/layout/app-sidebar"
import { AppHeader } from "@/components/layout/app-header"
import { ClaimsTable } from "@/components/claims/claims-table"
import { ClaimStats } from "@/components/claims/claim-stats"
import { Button } from "@/components/ui/button"
import { Plus, Download } from "lucide-react"
import type { Claim } from "@/lib/types"

type SupabaseListResponse<T> = {
  data?: T[]
}

function pickFirst<T>(...values: T[]): T | undefined {
  for (const v of values) {
    if (v !== undefined && v !== null) return v
  }
  return undefined
}

function toNumberOrZero(value: unknown): number {
  if (typeof value === "number" && Number.isFinite(value)) return value
  const n = Number(value)
  return Number.isFinite(n) ? n : 0
}

function toNumberOrNull(value: unknown): number | null {
  if (value === null || value === undefined) return null
  if (typeof value === "number" && Number.isFinite(value)) return value
  const n = Number(value)
  return Number.isFinite(n) ? n : null
}

function mapBackendClaimToFrontend(row: any): Claim {
  const billed = toNumberOrZero(pickFirst(row?.billed_amount, row?.billedAmount, row?.billed))
  const expected = toNumberOrZero(
    pickFirst(row?.expected, row?.expected_reimbursement, row?.expectedReimbursement, row?.expected_reimbursement_amount),
  )
  const actual = toNumberOrNull(pickFirst(row?.actual, row?.actual_reimbursement, row?.actualReimbursement))

  return {
    id: String(row?.claim_id ?? row?.id ?? ""),
    patientId: row?.patient_id === null || row?.patient_id === undefined ? "" : String(row.patient_id),
    patientName: String(row?.patient ?? row?.patient_name ?? ""),
    procedureCode: String(pickFirst(row?.procedure_code, row?.procedureCode, row?.cpt_code, row?.cptCode) ?? ""),
    procedureName: String(pickFirst(row?.procedure_name, row?.procedureName) ?? ""),
    dateOfService: String(pickFirst(row?.date_of_service, row?.dateOfService) ?? ""),
    billedAmount: billed,
    expectedReimbursement: expected,
    actualReimbursement: actual,
    status: row?.status as Claim["status"],
    payerName: String(pickFirst(row?.payer, row?.payer_name, row?.payerName) ?? ""),
    variance: actual === null ? null : actual - expected,
    submittedDate: String(row?.submitted_date ?? row?.created_at ?? row?.date_of_service ?? new Date().toISOString()),
  }
}

async function getClaimsFromBackend(): Promise<Claim[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
  const base = apiUrl.replace(/\/$/, "")

  const res = await fetch(`${base}/claims`, { cache: "no-store" })
  if (!res.ok) {
    throw new Error(`Failed to fetch claims: ${res.status} ${res.statusText}`)
  }

  const json = (await res.json()) as unknown
  const rows =
    Array.isArray(json) ? json : (json as SupabaseListResponse<any>)?.data ?? []

  return rows.map(mapBackendClaimToFrontend)
}

export default async function ClaimsPage() {
  const claims = await getClaimsFromBackend()

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
