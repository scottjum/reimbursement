"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Clock } from "lucide-react"

const recentCalculations = [
  {
    id: 1,
    procedureCode: "99213",
    procedureName: "Office Visit - Level 3",
    payer: "Blue Cross Blue Shield",
    amount: 120.0,
    timestamp: "2 hours ago",
  },
  {
    id: 2,
    procedureCode: "80053",
    procedureName: "Comprehensive Metabolic Panel",
    payer: "United Healthcare",
    amount: 68.0,
    timestamp: "5 hours ago",
  },
  {
    id: 3,
    procedureCode: "93000",
    procedureName: "Electrocardiogram",
    payer: "Aetna",
    amount: 95.0,
    timestamp: "1 day ago",
  },
]

export function RecentCalculations() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Calculations</CardTitle>
        <CardDescription>Your pricing lookup history</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {recentCalculations.map((calc) => (
            <div key={calc.id} className="flex items-start justify-between border-b pb-4 last:border-0 last:pb-0">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-sm font-semibold">{calc.procedureCode}</span>
                  <span className="text-xs text-muted-foreground">{calc.procedureName}</span>
                </div>
                <p className="text-xs text-muted-foreground">{calc.payer}</p>
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold">${calc.amount.toFixed(2)}</div>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Clock className="h-3 w-3" />
                  {calc.timestamp}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
