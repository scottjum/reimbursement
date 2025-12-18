"use client"
import { MoreVertical, Download, Eye, Trash2, FileText } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"
import type { Contract } from "@/lib/types"

interface ContractListProps {
  contracts: Contract[]
}

export function ContractList({ contracts }: ContractListProps) {
  return (
    <div className="space-y-3">
      {contracts.map((contract) => (
        <Card key={contract.id} className="p-4">
          <div className="flex items-start justify-between">
            <div className="flex gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <FileText className="h-6 w-6 text-primary" />
              </div>

              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold">{contract.payerName}</h3>
                  <Badge
                    variant={
                      contract.status === "active"
                        ? "default"
                        : contract.status === "pending"
                          ? "secondary"
                          : "destructive"
                    }
                  >
                    {contract.status}
                  </Badge>
                </div>

                <p className="mt-1 text-sm text-muted-foreground">Contract #{contract.contractNumber}</p>

                <div className="mt-3 flex gap-6 text-sm">
                  <div>
                    <span className="text-muted-foreground">Effective: </span>
                    <span className="font-medium">{new Date(contract.effectiveDate).toLocaleDateString()}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Expires: </span>
                    <span className="font-medium">{new Date(contract.expirationDate).toLocaleDateString()}</span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Procedures: </span>
                    <span className="font-medium">{contract.totalProcedures}</span>
                  </div>
                </div>
              </div>
            </div>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem>
                  <Eye className="mr-2 h-4 w-4" />
                  View Details
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Download className="mr-2 h-4 w-4" />
                  Download
                </DropdownMenuItem>
                <DropdownMenuItem className="text-destructive">
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </Card>
      ))}
    </div>
  )
}
