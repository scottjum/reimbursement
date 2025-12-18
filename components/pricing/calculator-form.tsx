"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Calculator, Loader2, CheckCircle2, AlertCircle } from "lucide-react"
import { pricingAPI } from "@/lib/mock-api"

const commonProcedures = [
  { code: "99213", name: "Office Visit - Level 3" },
  { code: "99214", name: "Office Visit - Level 4" },
  { code: "99215", name: "Office Visit - Level 5" },
  { code: "80053", name: "Comprehensive Metabolic Panel" },
  { code: "93000", name: "Electrocardiogram" },
  { code: "36415", name: "Venipuncture" },
  { code: "85025", name: "Complete Blood Count" },
]

const payers = ["Blue Cross Blue Shield", "United Healthcare", "Aetna", "Medicare", "Medicaid", "Cigna", "Humana"]

export function CalculatorForm() {
  const [procedureCode, setProcedureCode] = useState("")
  const [customProcedure, setCustomProcedure] = useState("")
  const [payer, setPayer] = useState("")
  const [isCalculating, setIsCalculating] = useState(false)
  const [result, setResult] = useState<{
    procedureCode: string
    procedureName: string
    expectedReimbursement: number
    confidence: number
    contractReference: string
  } | null>(null)

  const handleCalculate = async () => {
    const code = procedureCode === "custom" ? customProcedure : procedureCode

    if (!code || !payer) return

    setIsCalculating(true)
    setResult(null)

    try {
      const calculationResult = await pricingAPI.calculate(code, payer)
      setResult(calculationResult)
    } catch (error) {
      console.error("[v0] Pricing calculation error:", error)
    } finally {
      setIsCalculating(false)
    }
  }

  const resetForm = () => {
    setProcedureCode("")
    setCustomProcedure("")
    setPayer("")
    setResult(null)
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Calculate Expected Reimbursement</CardTitle>
          <CardDescription>
            Enter procedure details to get real-time pricing intelligence based on your contracts
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="procedure">Procedure Code</Label>
            <Select value={procedureCode} onValueChange={setProcedureCode}>
              <SelectTrigger id="procedure">
                <SelectValue placeholder="Select procedure code" />
              </SelectTrigger>
              <SelectContent>
                {commonProcedures.map((proc) => (
                  <SelectItem key={proc.code} value={proc.code}>
                    {proc.code} - {proc.name}
                  </SelectItem>
                ))}
                <SelectItem value="custom">Custom Code</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {procedureCode === "custom" && (
            <div className="space-y-2">
              <Label htmlFor="custom-code">Custom Procedure Code</Label>
              <Input
                id="custom-code"
                placeholder="Enter CPT code"
                value={customProcedure}
                onChange={(e) => setCustomProcedure(e.target.value)}
              />
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="payer">Insurance Payer</Label>
            <Select value={payer} onValueChange={setPayer}>
              <SelectTrigger id="payer">
                <SelectValue placeholder="Select insurance payer" />
              </SelectTrigger>
              <SelectContent>
                {payers.map((p) => (
                  <SelectItem key={p} value={p}>
                    {p}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex gap-2">
            <Button className="flex-1" onClick={handleCalculate} disabled={isCalculating || !procedureCode || !payer}>
              {isCalculating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Calculating...
                </>
              ) : (
                <>
                  <Calculator className="mr-2 h-4 w-4" />
                  Calculate
                </>
              )}
            </Button>
            <Button variant="outline" onClick={resetForm}>
              Reset
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Pricing Intelligence</CardTitle>
          <CardDescription>AI-powered reimbursement prediction with confidence scoring</CardDescription>
        </CardHeader>
        <CardContent>
          {!result && !isCalculating && (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="rounded-full bg-muted p-6">
                <Calculator className="h-12 w-12 text-muted-foreground" />
              </div>
              <p className="mt-4 text-sm text-muted-foreground">
                Enter procedure and payer information to calculate expected reimbursement
              </p>
            </div>
          )}

          {isCalculating && (
            <div className="flex flex-col items-center justify-center py-12">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
              <p className="mt-4 text-sm text-muted-foreground">Analyzing contracts and pricing rules...</p>
            </div>
          )}

          {result && (
            <div className="space-y-6">
              <div className="flex items-start gap-3 rounded-lg bg-accent/10 p-4">
                <CheckCircle2 className="mt-0.5 h-5 w-5 text-accent" />
                <div className="flex-1">
                  <p className="text-sm font-medium">Calculation Complete</p>
                  <p className="text-xs text-muted-foreground">Based on contract {result.contractReference}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <Label className="text-xs text-muted-foreground">Procedure</Label>
                  <div className="mt-1">
                    <span className="font-mono text-sm font-semibold">{result.procedureCode}</span>
                    <span className="ml-2 text-sm text-muted-foreground">{result.procedureName}</span>
                  </div>
                </div>

                <div className="rounded-lg border bg-card p-4">
                  <Label className="text-xs text-muted-foreground">Expected Reimbursement</Label>
                  <div className="mt-2 text-3xl font-bold text-primary">${result.expectedReimbursement.toFixed(2)}</div>
                </div>

                <div>
                  <div className="flex items-center justify-between">
                    <Label className="text-xs text-muted-foreground">Confidence Score</Label>
                    <span className="text-sm font-medium">{(result.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="mt-2 h-2 w-full rounded-full bg-secondary">
                    <div
                      className="h-2 rounded-full bg-accent transition-all"
                      style={{ width: `${result.confidence * 100}%` }}
                    />
                  </div>
                  <p className="mt-2 text-xs text-muted-foreground">
                    {result.confidence >= 0.9
                      ? "Very high confidence based on exact contract match"
                      : result.confidence >= 0.75
                        ? "High confidence based on similar procedures"
                        : "Moderate confidence - consider manual review"}
                  </p>
                </div>

                <div className="rounded-lg bg-muted p-4">
                  <div className="flex items-start gap-2">
                    <AlertCircle className="mt-0.5 h-4 w-4 text-muted-foreground" />
                    <div className="text-xs text-muted-foreground">
                      <p className="font-medium">Note:</p>
                      <p className="mt-1">
                        This calculation is based on your current contracts. Actual reimbursement may vary based on
                        patient eligibility, modifiers, and payer-specific rules.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
