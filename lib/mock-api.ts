// Mock API layer matching FastAPI backend structure
import type { Contract, Claim, PricingRule, Analytics, UploadResponse } from "./types"

// Simulated delay to mimic API calls
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

// Mock data
const mockContracts: Contract[] = [
  {
    id: "ct-001",
    payerName: "Blue Cross Blue Shield",
    contractNumber: "BCBS-2024-001",
    effectiveDate: "2024-01-01",
    expirationDate: "2024-12-31",
    status: "active",
    documentUrl: "/contracts/bcbs-001.pdf",
    uploadedAt: "2024-01-15T10:00:00Z",
    totalProcedures: 247,
  },
  {
    id: "ct-002",
    payerName: "United Healthcare",
    contractNumber: "UHC-2024-003",
    effectiveDate: "2024-02-01",
    expirationDate: "2024-12-31",
    status: "active",
    documentUrl: "/contracts/uhc-003.pdf",
    uploadedAt: "2024-02-10T14:30:00Z",
    totalProcedures: 189,
  },
  {
    id: "ct-003",
    payerName: "Aetna",
    contractNumber: "AET-2024-007",
    effectiveDate: "2024-01-15",
    expirationDate: "2024-12-31",
    status: "active",
    documentUrl: "/contracts/aetna-007.pdf",
    uploadedAt: "2024-01-20T09:15:00Z",
    totalProcedures: 312,
  },
]

const mockClaims: Claim[] = [
  {
    id: "cl-001",
    patientId: "pt-1234",
    patientName: "John Smith",
    procedureCode: "99213",
    procedureName: "Office Visit - Level 3",
    dateOfService: "2024-11-15",
    billedAmount: 150.0,
    expectedReimbursement: 120.0,
    actualReimbursement: 115.0,
    status: "paid",
    payerName: "Blue Cross Blue Shield",
    variance: -5.0,
    submittedDate: "2024-11-16T08:00:00Z",
  },
  {
    id: "cl-002",
    patientId: "pt-5678",
    patientName: "Sarah Johnson",
    procedureCode: "80053",
    procedureName: "Comprehensive Metabolic Panel",
    dateOfService: "2024-11-18",
    billedAmount: 85.0,
    expectedReimbursement: 68.0,
    actualReimbursement: null,
    status: "processing",
    payerName: "United Healthcare",
    variance: null,
    submittedDate: "2024-11-19T10:30:00Z",
  },
  {
    id: "cl-003",
    patientId: "pt-9012",
    patientName: "Michael Chen",
    procedureCode: "93000",
    procedureName: "Electrocardiogram",
    dateOfService: "2024-11-20",
    billedAmount: 120.0,
    expectedReimbursement: 95.0,
    actualReimbursement: 85.0,
    status: "paid",
    payerName: "Aetna",
    variance: -10.0,
    submittedDate: "2024-11-21T09:00:00Z",
  },
  {
    id: "cl-004",
    patientId: "pt-3456",
    patientName: "Emily Davis",
    procedureCode: "99214",
    procedureName: "Office Visit - Level 4",
    dateOfService: "2024-11-22",
    billedAmount: 200.0,
    expectedReimbursement: 160.0,
    actualReimbursement: null,
    status: "denied",
    payerName: "Blue Cross Blue Shield",
    variance: null,
    submittedDate: "2024-11-23T11:00:00Z",
  },
]

const mockPricingRules: PricingRule[] = [
  {
    id: "pr-001",
    contractId: "ct-001",
    procedureCode: "99213",
    procedureName: "Office Visit - Level 3",
    reimbursementRate: 120.0,
    unit: "fixed",
  },
  {
    id: "pr-002",
    contractId: "ct-001",
    procedureCode: "99214",
    procedureName: "Office Visit - Level 4",
    reimbursementRate: 160.0,
    unit: "fixed",
  },
]

const mockAnalytics: Analytics = {
  totalRevenue: 3245678.5,
  expectedRevenue: 3456789.0,
  revenueVariance: -211110.5,
  claimsProcessed: 1847,
  claimsPending: 234,
  averageReimbursementTime: 18.5,
  denialRate: 8.2,
  topDenialReasons: [
    { reason: "Missing documentation", count: 45 },
    { reason: "Prior authorization required", count: 38 },
    { reason: "Procedure not covered", count: 22 },
    { reason: "Duplicate claim", count: 15 },
  ],
  revenueByPayer: [
    { payer: "Blue Cross Blue Shield", amount: 1234567.89 },
    { payer: "United Healthcare", amount: 987654.32 },
    { payer: "Aetna", amount: 765432.1 },
    { payer: "Medicare", amount: 258024.19 },
  ],
  monthlyTrend: [
    { month: "Jul", revenue: 287654, claims: 156 },
    { month: "Aug", revenue: 312456, claims: 178 },
    { month: "Sep", revenue: 298765, claims: 164 },
    { month: "Oct", revenue: 334567, claims: 189 },
    { month: "Nov", revenue: 356789, claims: 201 },
    { month: "Dec", revenue: 289456, claims: 142 },
  ],
}

// API functions
export const contractsAPI = {
  async getAll(): Promise<Contract[]> {
    await delay(500)
    return mockContracts
  },

  async getById(id: string): Promise<Contract | null> {
    await delay(300)
    return mockContracts.find((c) => c.id === id) || null
  },

  async upload(file: File): Promise<UploadResponse> {
    await delay(2000) // Simulate processing time
    return {
      success: true,
      contractId: `ct-${Date.now()}`,
      message: "Contract uploaded and processed successfully",
      extractedData: {
        payerName: "Sample Payer",
        contractNumber: `SMPL-${Date.now()}`,
        proceduresFound: Math.floor(Math.random() * 200) + 50,
      },
    }
  },
}

export const claimsAPI = {
  async getAll(): Promise<Claim[]> {
    await delay(600)
    return mockClaims
  },

  async getById(id: string): Promise<Claim | null> {
    await delay(300)
    return mockClaims.find((c) => c.id === id) || null
  },

  async create(claim: Omit<Claim, "id" | "submittedDate">): Promise<Claim> {
    await delay(500)
    return {
      ...claim,
      id: `cl-${Date.now()}`,
      submittedDate: new Date().toISOString(),
    }
  },
}

export const pricingAPI = {
  async calculate(
    procedureCode: string,
    payerName: string,
  ): Promise<{
    procedureCode: string
    procedureName: string
    expectedReimbursement: number
    confidence: number
    contractReference: string
  }> {
    await delay(400)
    return {
      procedureCode,
      procedureName: "Sample Procedure",
      expectedReimbursement: Math.floor(Math.random() * 300) + 50,
      confidence: 0.85 + Math.random() * 0.15,
      contractReference: "ct-001",
    }
  },

  async getRules(contractId: string): Promise<PricingRule[]> {
    await delay(400)
    return mockPricingRules.filter((r) => r.contractId === contractId)
  },
}

export const analyticsAPI = {
  async getDashboard(): Promise<Analytics> {
    await delay(700)
    return mockAnalytics
  },
}
