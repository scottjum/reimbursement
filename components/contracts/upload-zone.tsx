"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { Upload, File, X, Loader2, CheckCircle2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import type { UploadResponse } from "@/lib/types"

export function UploadZone() {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      setSelectedFile(files[0])
      setUploadResult(null)
    }
  }, [])

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      setSelectedFile(files[0])
      setUploadResult(null)
    }
  }, [])

  const handleUpload = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    try {
      // Create FormData to send the file
      const formData = new FormData()
      formData.append("file", selectedFile)

      // Get API URL from environment variable or use default
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
      const uploadUrl = `${apiUrl}/upload`

      // Make fetch request to backend
      const response = await fetch(uploadUrl, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        let errorMessage = `Upload failed with status ${response.status}`
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorData.message || errorMessage
        } catch {
          // If response is not JSON, use status text
          errorMessage = response.statusText || errorMessage
        }
        throw new Error(errorMessage)
      }

      const data = await response.json()
      
      // Transform backend response to match frontend expected format
      const result: UploadResponse = {
        success: true,
        message: `File "${data.filename}" uploaded and processed successfully`,
        extractedData: {
          payerName: "Processing...", // Backend doesn't extract this yet
          contractNumber: data.filename,
          proceduresFound: 0, // Backend doesn't extract this yet
        },
      }

      setUploadResult(result)
      setTimeout(() => {
        setSelectedFile(null)
        setUploadResult(null)
      }, 3000)
    } catch (error) {
      console.error("Upload error:", error)
      let errorMessage = "Upload failed. Please try again."
      
      if (error instanceof Error) {
        errorMessage = error.message
        // Provide more helpful error messages
        if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError")) {
          errorMessage = "Cannot connect to backend server. Please ensure the backend is running on http://localhost:8000"
        } else if (error.message.includes("CORS")) {
          errorMessage = "CORS error: Please check that FRONTEND_URL is set correctly in your backend .env file"
        }
      }
      
      setUploadResult({
        success: false,
        message: errorMessage,
      })
    } finally {
      setIsUploading(false)
    }
  }

  const clearFile = () => {
    setSelectedFile(null)
    setUploadResult(null)
  }

  return (
    <div className="space-y-4">
      <Card
        className={`relative border-2 border-dashed transition-colors ${
          isDragging ? "border-primary bg-primary/5" : "border-border hover:border-primary/50"
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="flex flex-col items-center justify-center p-12">
          <div className="rounded-full bg-primary/10 p-4">
            <Upload className="h-8 w-8 text-primary" />
          </div>

          <h3 className="mt-4 text-lg font-semibold">Upload Contract Document</h3>
          <p className="mt-2 text-center text-sm text-muted-foreground">
            Drag and drop your payer contract file here, or click to browse
          </p>
          <p className="mt-1 text-xs text-muted-foreground">Supports PDF, DOCX, and TXT files up to 50MB</p>

          <input type="file" id="file-upload" className="hidden" accept=".pdf,.docx,.txt" onChange={handleFileSelect} />
          <Button
            variant="outline"
            className="mt-4 bg-transparent"
            onClick={() => document.getElementById("file-upload")?.click()}
          >
            Browse Files
          </Button>
        </div>
      </Card>

      {selectedFile && (
        <Card className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-lg bg-primary/10 p-2">
                <File className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium">{selectedFile.name}</p>
                <p className="text-xs text-muted-foreground">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {!isUploading && !uploadResult && (
                <>
                  <Button variant="ghost" size="icon" onClick={clearFile}>
                    <X className="h-4 w-4" />
                  </Button>
                  <Button onClick={handleUpload}>Upload & Process</Button>
                </>
              )}

              {isUploading && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Processing contract...
                </div>
              )}

              {uploadResult && uploadResult.success && (
                <div className="flex items-center gap-2 text-sm text-accent">
                  <CheckCircle2 className="h-4 w-4" />
                  Upload successful
                </div>
              )}
            </div>
          </div>

          {uploadResult && uploadResult.extractedData && (
            <div className="mt-4 rounded-lg bg-muted p-4">
              <p className="text-sm font-medium">Extracted Information:</p>
              <div className="mt-2 grid gap-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Payer Name:</span>
                  <span className="font-medium">{uploadResult.extractedData.payerName}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Contract Number:</span>
                  <span className="font-medium">{uploadResult.extractedData.contractNumber}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Procedures Found:</span>
                  <span className="font-medium">{uploadResult.extractedData.proceduresFound}</span>
                </div>
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  )
}
