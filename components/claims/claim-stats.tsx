import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { DollarSign, FileText, AlertCircle, TrendingUp } from "lucide-react"
import type { Claim } from "@/lib/types"

interface ClaimStatsProps {
  claims: Claim[]
}

export function ClaimStats({ claims }: ClaimStatsProps) {
  const totalBilled = claims.reduce((sum, claim) => sum + claim.billedAmount, 0)
  const totalExpected = claims.reduce((sum, claim) => sum + claim.expectedReimbursement, 0)

  const paidClaims = claims.filter((c) => c.actualReimbursement !== null)
  const totalActual = paidClaims.reduce((sum, claim) => sum + (claim.actualReimbursement || 0), 0)
  const totalVariance = paidClaims.reduce((sum, claim) => sum + (claim.variance || 0), 0)

  const deniedCount = claims.filter((c) => c.status === "denied").length
  const processingCount = claims.filter((c) => c.status === "processing" || c.status === "submitted").length

  const stats = [
    {
      title: "Total Billed",
      value: `$${(totalBilled / 1000).toFixed(1)}K`,
      subtitle: `${claims.length} claims`,
      icon: DollarSign,
      color: "text-primary",
    },
    {
      title: "Expected Reimbursement",
      value: `$${(totalExpected / 1000).toFixed(1)}K`,
      subtitle: totalBilled > 0 ? `${((totalExpected / totalBilled) * 100).toFixed(1)}% of billed` : "—",
      icon: TrendingUp,
      color: "text-accent",
    },
    {
      title: "Actual Received",
      value: `$${(totalActual / 1000).toFixed(1)}K`,
      subtitle: totalVariance < 0 ? `$${Math.abs(totalVariance).toFixed(0)} shortfall` : `On target`,
      icon: FileText,
      color: totalVariance < 0 ? "text-destructive" : "text-accent",
    },
    {
      title: "Action Required",
      value: deniedCount + processingCount,
      subtitle: `${deniedCount} denied, ${processingCount} pending`,
      icon: AlertCircle,
      color: "text-muted-foreground",
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
            <stat.icon className={`h-4 w-4 ${stat.color}`} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="mt-1 text-xs text-muted-foreground">{stat.subtitle}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
