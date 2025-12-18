// Database types and interfaces for healthcare reimbursement platform

export interface Contract {
  id: string
  payerName: string
  contractNumber: string
  effectiveDate: string
  expirationDate: string
  status: "active" | "pending" | "expired"
  documentUrl: string
  uploadedAt: string
  totalProcedures: number
}

export interface Claim {
  id: string
  patientId: string
  patientName: string
  procedureCode: string
  procedureName: string
  dateOfService: string
  billedAmount: number
  expectedReimbursement: number
  actualReimbursement: number | null
  status: "submitted" | "processing" | "paid" | "denied" | "appealed"
  payerName: string
  variance: number | null
  submittedDate: string
}

export interface PricingRule {
  id: string
  contractId: string
  procedureCode: string
  procedureName: string
  reimbursementRate: number
  unit: "fixed" | "percentage"
  notes?: string
}

export interface Analytics {
  totalRevenue: number
  expectedRevenue: number
  revenueVariance: number
  claimsProcessed: number
  claimsPending: number
  averageReimbursementTime: number
  denialRate: number
  topDenialReasons: Array<{ reason: string; count: number }>
  revenueByPayer: Array<{ payer: string; amount: number }>
  monthlyTrend: Array<{ month: string; revenue: number; claims: number }>
}

export interface UploadResponse {
  success: boolean
  contractId?: string
  message: string
  extractedData?: {
    payerName: string
    contractNumber: string
    proceduresFound: number
  }
}
