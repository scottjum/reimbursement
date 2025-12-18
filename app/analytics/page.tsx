import { AppSidebar } from "@/components/layout/app-sidebar"
import { AppHeader } from "@/components/layout/app-header"
import { KeyMetrics } from "@/components/analytics/key-metrics"
import { RevenueChart } from "@/components/analytics/revenue-chart"
import { PayerBreakdown } from "@/components/analytics/payer-breakdown"
import { DenialAnalysis } from "@/components/analytics/denial-analysis"
import { analyticsAPI } from "@/lib/mock-api"
import { Button } from "@/components/ui/button"
import { Download, RefreshCw } from "lucide-react"

export default async function AnalyticsPage() {
  const analytics = await analyticsAPI.getDashboard()

  return (
    <div className="flex h-screen bg-background">
      <AppSidebar />

      <div className="flex flex-1 flex-col overflow-hidden">
        <AppHeader />

        <main className="flex-1 overflow-y-auto p-6">
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Analytics Dashboard</h1>
              <p className="text-muted-foreground">Comprehensive insights into your reimbursement performance</p>
            </div>

            <div className="flex gap-2">
              <Button variant="outline">
                <RefreshCw className="mr-2 h-4 w-4" />
                Refresh
              </Button>
              <Button variant="outline">
                <Download className="mr-2 h-4 w-4" />
                Export Report
              </Button>
            </div>
          </div>

          <div className="space-y-6">
            <KeyMetrics analytics={analytics} />

            <div className="grid gap-6 lg:grid-cols-2">
              <RevenueChart data={analytics.monthlyTrend} />
              <PayerBreakdown data={analytics.revenueByPayer} />
            </div>

            <DenialAnalysis data={analytics.topDenialReasons} denialRate={analytics.denialRate} />
          </div>
        </main>
      </div>
    </div>
  )
}
