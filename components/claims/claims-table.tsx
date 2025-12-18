"use client"

import { useState } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search, Eye } from "lucide-react"
import type { Claim } from "@/lib/types"

interface ClaimsTableProps {
  claims: Claim[]
}

export function ClaimsTable({ claims: initialClaims }: ClaimsTableProps) {
  const [claims, setClaims] = useState(initialClaims)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState<string>("all")

  const filteredClaims = claims.filter((claim) => {
    const matchesSearch =
      claim.patientName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      claim.procedureCode.toLowerCase().includes(searchQuery.toLowerCase()) ||
      claim.id.toLowerCase().includes(searchQuery.toLowerCase())

    const matchesStatus = statusFilter === "all" || claim.status === statusFilter

    return matchesSearch && matchesStatus
  })

  const getStatusColor = (status: Claim["status"]) => {
    switch (status) {
      case "paid":
        return "default"
      case "processing":
        return "secondary"
      case "submitted":
        return "outline"
      case "denied":
        return "destructive"
      case "appealed":
        return "secondary"
      default:
        return "outline"
    }
  }

  const formatCurrency = (amount: number | null) => {
    if (amount === null) return "-"
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount)
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search by patient name, procedure code, or claim ID..."
            className="pl-10"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="submitted">Submitted</SelectItem>
            <SelectItem value="processing">Processing</SelectItem>
            <SelectItem value="paid">Paid</SelectItem>
            <SelectItem value="denied">Denied</SelectItem>
            <SelectItem value="appealed">Appealed</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="rounded-lg border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Claim ID</TableHead>
              <TableHead>Patient</TableHead>
              <TableHead>Procedure</TableHead>
              <TableHead>Date of Service</TableHead>
              <TableHead>Payer</TableHead>
              <TableHead className="text-right">Billed</TableHead>
              <TableHead className="text-right">Expected</TableHead>
              <TableHead className="text-right">Actual</TableHead>
              <TableHead className="text-right">Variance</TableHead>
              <TableHead>Status</TableHead>
              <TableHead></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredClaims.length === 0 ? (
              <TableRow>
                <TableCell colSpan={11} className="text-center text-muted-foreground">
                  No claims found
                </TableCell>
              </TableRow>
            ) : (
              filteredClaims.map((claim) => (
                <TableRow key={claim.id}>
                  <TableCell className="font-mono text-sm">{claim.id}</TableCell>
                  <TableCell className="font-medium">{claim.patientName}</TableCell>
                  <TableCell>
                    <div>
                      <div className="font-medium">{claim.procedureCode}</div>
                      <div className="text-xs text-muted-foreground">{claim.procedureName}</div>
                    </div>
                  </TableCell>
                  <TableCell>{new Date(claim.dateOfService).toLocaleDateString()}</TableCell>
                  <TableCell className="text-sm">{claim.payerName}</TableCell>
                  <TableCell className="text-right font-medium">{formatCurrency(claim.billedAmount)}</TableCell>
                  <TableCell className="text-right">{formatCurrency(claim.expectedReimbursement)}</TableCell>
                  <TableCell className="text-right font-medium">{formatCurrency(claim.actualReimbursement)}</TableCell>
                  <TableCell className="text-right">
                    {claim.variance !== null ? (
                      <span className={claim.variance < 0 ? "text-destructive" : "text-accent"}>
                        {formatCurrency(claim.variance)}
                      </span>
                    ) : (
                      "-"
                    )}
                  </TableCell>
                  <TableCell>
                    <Badge variant={getStatusColor(claim.status)}>{claim.status}</Badge>
                  </TableCell>
                  <TableCell>
                    <Button variant="ghost" size="icon">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <div>
          Showing {filteredClaims.length} of {claims.length} claims
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" disabled>
            Previous
          </Button>
          <Button variant="outline" size="sm" disabled>
            Next
          </Button>
        </div>
      </div>
    </div>
  )
}
