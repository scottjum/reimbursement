import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown, DollarSign, Clock, AlertCircle, CheckCircle } from "lucide-react"
import type { Analytics } from "@/lib/types"

interface KeyMetricsProps {
  analytics: Analytics
}

export function KeyMetrics({ analytics }: KeyMetricsProps) {
  const variancePercentage = ((analytics.revenueVariance / analytics.expectedRevenue) * 100).toFixed(1)
  const collectionRate = ((analytics.totalRevenue / analytics.expectedRevenue) * 100).toFixed(1)

  const metrics = [
    {
      title: "Total Revenue",
      value: `$${(analytics.totalRevenue / 1000000).toFixed(2)}M`,
      subtitle: `${collectionRate}% collection rate`,
      icon: DollarSign,
      trend: Number.parseFloat(variancePercentage) >= 0 ? "up" : "down",
      color: "text-primary",
    },
    {
      title: "Revenue Variance",
      value: `$${Math.abs(analytics.revenueVariance / 1000).toFixed(1)}K`,
      subtitle: `${Math.abs(Number.parseFloat(variancePercentage))}% ${Number.parseFloat(variancePercentage) >= 0 ? "above" : "below"} expected`,
      icon: Number.parseFloat(variancePercentage) >= 0 ? TrendingUp : TrendingDown,
      trend: Number.parseFloat(variancePercentage) >= 0 ? "up" : "down",
      color: Number.parseFloat(variancePercentage) >= 0 ? "text-accent" : "text-destructive",
    },
    {
      title: "Avg Processing Time",
      value: `${analytics.averageReimbursementTime} days`,
      subtitle: "From submission to payment",
      icon: Clock,
      trend: "neutral",
      color: "text-muted-foreground",
    },
    {
      title: "Denial Rate",
      value: `${analytics.denialRate}%`,
      subtitle: `${Math.floor((analytics.denialRate / 100) * (analytics.claimsProcessed + analytics.claimsPending))} claims denied`,
      icon: analytics.denialRate < 10 ? CheckCircle : AlertCircle,
      trend: analytics.denialRate < 10 ? "up" : "down",
      color: analytics.denialRate < 10 ? "text-accent" : "text-destructive",
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric) => (
        <Card key={metric.title}>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">{metric.title}</CardTitle>
            <metric.icon className={`h-4 w-4 ${metric.color}`} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metric.value}</div>
            <p className="mt-1 text-xs text-muted-foreground">{metric.subtitle}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
