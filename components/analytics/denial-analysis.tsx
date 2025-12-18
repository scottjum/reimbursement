"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { AlertTriangle } from "lucide-react"
import type { Analytics } from "@/lib/types"

interface DenialAnalysisProps {
  data: Analytics["topDenialReasons"]
  denialRate: number
}

export function DenialAnalysis({ data, denialRate }: DenialAnalysisProps) {
  const totalDenials = data.reduce((sum, item) => sum + item.count, 0)

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-destructive" />
          Denial Analysis
        </CardTitle>
        <CardDescription>
          Current denial rate: <span className="font-semibold text-foreground">{denialRate}%</span>
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {data.map((reason) => {
          const percentage = (reason.count / totalDenials) * 100
          return (
            <div key={reason.reason} className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium">{reason.reason}</span>
                <div className="flex items-center gap-2">
                  <span className="text-muted-foreground">{reason.count} claims</span>
                  <span className="font-semibold">{percentage.toFixed(1)}%</span>
                </div>
              </div>
              <Progress value={percentage} className="h-2" />
            </div>
          )
        })}

        <div className="mt-6 rounded-lg bg-muted p-4">
          <h4 className="text-sm font-semibold">Recommendations</h4>
          <ul className="mt-2 space-y-1 text-xs text-muted-foreground">
            <li>• Review documentation requirements for top denial reasons</li>
            <li>• Implement pre-authorization checks for high-risk procedures</li>
            <li>• Train staff on proper claim submission procedures</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  )
}
