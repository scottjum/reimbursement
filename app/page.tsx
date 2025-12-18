import { AppSidebar } from "@/components/layout/app-sidebar"
import { AppHeader } from "@/components/layout/app-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowUpRight, ArrowDownRight, TrendingUp, Clock, AlertTriangle, DollarSign } from "lucide-react"
import { analyticsAPI } from "@/lib/mock-api"

export default async function DashboardPage() {
  const analytics = await analyticsAPI.getDashboard()

  const stats = [
    {
      title: "Total Revenue",
      value: `$${(analytics.totalRevenue / 1000000).toFixed(2)}M`,
      change: analytics.revenueVariance,
      changeLabel: `$${Math.abs(analytics.revenueVariance / 1000).toFixed(1)}K variance`,
      icon: DollarSign,
      trend: analytics.revenueVariance >= 0 ? "up" : "down",
    },
    {
      title: "Claims Processed",
      value: analytics.claimsProcessed.toLocaleString(),
      change: analytics.claimsPending,
      changeLabel: `${analytics.claimsPending} pending`,
      icon: TrendingUp,
      trend: "neutral",
    },
    {
      title: "Avg Processing Time",
      value: `${analytics.averageReimbursementTime} days`,
      change: -2.3,
      changeLabel: "2.3 days faster",
      icon: Clock,
      trend: "up",
    },
    {
      title: "Denial Rate",
      value: `${analytics.denialRate}%`,
      change: analytics.denialRate - 9.5,
      changeLabel: "1.3% improvement",
      icon: AlertTriangle,
      trend: analytics.denialRate < 9.5 ? "up" : "down",
    },
  ]

  return (
    <div className="flex h-screen bg-background">
      <AppSidebar />

      <div className="flex flex-1 flex-col overflow-hidden">
        <AppHeader />

        <main className="flex-1 overflow-y-auto p-6">
          <div className="mb-6">
            <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-muted-foreground">Real-time reimbursement intelligence and performance metrics</p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {stats.map((stat) => (
              <Card key={stat.title}>
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
                  <stat.icon className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="mt-1 flex items-center gap-1 text-xs">
                    {stat.trend === "up" && <ArrowUpRight className="h-3 w-3 text-accent" />}
                    {stat.trend === "down" && <ArrowDownRight className="h-3 w-3 text-destructive" />}
                    <span
                      className={
                        stat.trend === "up"
                          ? "text-accent"
                          : stat.trend === "down"
                            ? "text-destructive"
                            : "text-muted-foreground"
                      }
                    >
                      {stat.changeLabel}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Revenue by Payer</CardTitle>
                <CardDescription>Top performing insurance providers</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analytics.revenueByPayer.map((payer, index) => {
                    const percentage = (payer.amount / analytics.totalRevenue) * 100
                    return (
                      <div key={payer.payer}>
                        <div className="flex items-center justify-between text-sm">
                          <span className="font-medium">{payer.payer}</span>
                          <span className="text-muted-foreground">${(payer.amount / 1000).toFixed(1)}K</span>
                        </div>
                        <div className="mt-2 h-2 w-full rounded-full bg-secondary">
                          <div className="h-2 rounded-full bg-primary" style={{ width: `${percentage}%` }} />
                        </div>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Top Denial Reasons</CardTitle>
                <CardDescription>Most common claim denial causes</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {analytics.topDenialReasons.map((reason) => {
                    const maxCount = Math.max(...analytics.topDenialReasons.map((r) => r.count))
                    const percentage = (reason.count / maxCount) * 100
                    return (
                      <div key={reason.reason}>
                        <div className="flex items-center justify-between text-sm">
                          <span className="font-medium">{reason.reason}</span>
                          <span className="text-muted-foreground">{reason.count} claims</span>
                        </div>
                        <div className="mt-2 h-2 w-full rounded-full bg-secondary">
                          <div className="h-2 rounded-full bg-accent" style={{ width: `${percentage}%` }} />
                        </div>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  )
}
