import { AppSidebar } from "@/components/layout/app-sidebar"
import { AppHeader } from "@/components/layout/app-header"
import { CalculatorForm } from "@/components/pricing/calculator-form"
import { RecentCalculations } from "@/components/pricing/recent-calculations"
import { Card, CardContent } from "@/components/ui/card"
import { Lightbulb } from "lucide-react"

export default function PricingPage() {
  return (
    <div className="flex h-screen bg-background">
      <AppSidebar />

      <div className="flex flex-1 flex-col overflow-hidden">
        <AppHeader />

        <main className="flex-1 overflow-y-auto p-6">
          <div className="mb-6">
            <h1 className="text-3xl font-bold tracking-tight">Pricing Calculator</h1>
            <p className="text-muted-foreground">Get instant reimbursement estimates based on your payer contracts</p>
          </div>

          <div className="mb-6">
            <Card className="border-accent/50 bg-accent/5">
              <CardContent className="flex items-start gap-3 pt-6">
                <div className="rounded-full bg-accent/20 p-2">
                  <Lightbulb className="h-5 w-5 text-accent" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold">AI-Powered Intelligence</h3>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Our system analyzes your uploaded contracts in real-time to provide accurate reimbursement
                    predictions. The confidence score indicates how closely the procedure matches your contract terms.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-6">
            <CalculatorForm />
            <RecentCalculations />
          </div>
        </main>
      </div>
    </div>
  )
}
