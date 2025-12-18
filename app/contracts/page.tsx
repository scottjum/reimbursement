import { AppSidebar } from "@/components/layout/app-sidebar"
import { AppHeader } from "@/components/layout/app-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { UploadZone } from "@/components/contracts/upload-zone"
import { ContractList } from "@/components/contracts/contract-list"
import { contractsAPI } from "@/lib/mock-api"
import { FileText, Clock, CheckCircle } from "lucide-react"

export default async function ContractsPage() {
  const contracts = await contractsAPI.getAll()

  const stats = {
    total: contracts.length,
    active: contracts.filter((c) => c.status === "active").length,
    expiringSoon: contracts.filter((c) => {
      const daysUntilExpiration = Math.floor(
        (new Date(c.expirationDate).getTime() - Date.now()) / (1000 * 60 * 60 * 24),
      )
      return daysUntilExpiration <= 90 && daysUntilExpiration > 0
    }).length,
  }

  return (
    <div className="flex h-screen bg-background">
      <AppSidebar />

      <div className="flex flex-1 flex-col overflow-hidden">
        <AppHeader />

        <main className="flex-1 overflow-y-auto p-6">
          <div className="mb-6">
            <h1 className="text-3xl font-bold tracking-tight">Contract Management</h1>
            <p className="text-muted-foreground">Upload and manage payer contracts with automated data extraction</p>
          </div>

          <div className="mb-6 grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Total Contracts</CardTitle>
                <FileText className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total}</div>
                <p className="text-xs text-muted-foreground">{stats.active} currently active</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Active Contracts</CardTitle>
                <CheckCircle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.active}</div>
                <p className="text-xs text-muted-foreground">Fully processed and active</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Expiring Soon</CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.expiringSoon}</div>
                <p className="text-xs text-muted-foreground">Within 90 days</p>
              </CardContent>
            </Card>
          </div>

          <Tabs defaultValue="upload" className="space-y-6">
            <TabsList>
              <TabsTrigger value="upload">Upload New Contract</TabsTrigger>
              <TabsTrigger value="active">Active Contracts</TabsTrigger>
              <TabsTrigger value="all">All Contracts</TabsTrigger>
            </TabsList>

            <TabsContent value="upload" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Upload Contract Document</CardTitle>
                  <CardDescription>
                    Our AI will automatically extract payer information, pricing rules, and procedure codes
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <UploadZone />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="active" className="space-y-4">
              <ContractList contracts={contracts.filter((c) => c.status === "active")} />
            </TabsContent>

            <TabsContent value="all" className="space-y-4">
              <ContractList contracts={contracts} />
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  )
}
