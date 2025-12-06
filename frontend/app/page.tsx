"use client";
import { useState } from "react";
import { Upload, CheckCircle, XCircle, Loader2, FileText, Calendar, DollarSign } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
      setError("");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to connect to the backend.");
      }

      const data = await response.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center py-12 px-4">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight mb-2">
          Invoice QC System
        </h1>
        <p className="text-slate-500">Upload a PDF Receipt to validate it.</p>
      </div>

      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8 border border-slate-100">
        <div className="border-2 border-dashed border-slate-300 rounded-lg p-8 flex flex-col items-center justify-center bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer relative">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          <Upload className="w-10 h-10 text-slate-400 mb-3" />
          <p className="text-sm text-slate-600 font-medium">
            {file ? file.name : "Click to select a PDF"}
          </p>
        </div>

        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className={`w-full mt-6 py-3 px-4 rounded-lg font-bold text-white transition-all
            ${!file || loading 
              ? "bg-slate-300 cursor-not-allowed" 
              : "bg-blue-600 hover:bg-blue-700 shadow-md hover:shadow-lg"}`}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <Loader2 className="animate-spin w-5 h-5" /> Processing...
            </span>
          ) : (
            "Validate Invoice"
          )}
        </button>

        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-600 text-sm rounded-md border border-red-100 font-bold">
            Server Error: {error}
          </div>
        )}
      </div>

      {result && (
        <div className="w-full max-w-lg mt-8 animate-fade-in-up">
          <div className={`p-6 rounded-xl border shadow-sm ${result.is_valid ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"}`}>
            
            {/* Header: Status */}
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold text-slate-800">
                  Invoice #{result.invoice_id || "Unknown"}
                </h3>
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${result.is_valid ? "bg-green-200 text-green-800" : "bg-red-200 text-red-800"}`}>
                  {result.is_valid ? "Approved" : "Rejected"}
                </span>
              </div>
              {result.is_valid ? (
                <CheckCircle className="w-10 h-10 text-green-500" />
              ) : (
                <XCircle className="w-10 h-10 text-red-500" />
              )}
            </div>

            {/* Error List (If any) */}
            {!result.is_valid && result.errors && result.errors.length > 0 && (
              <div className="bg-white/60 rounded-lg p-3 mb-4 border border-red-100">
                <p className="text-xs font-bold text-red-800 mb-2 uppercase">Issues Found:</p>
                <ul className="space-y-1">
                  {result.errors.map((err: string, idx: number) => (
                    <li key={idx} className="text-sm text-red-700 flex items-start gap-2">
                      <span className="mt-1.5 w-1.5 h-1.5 bg-red-500 rounded-full flex-shrink-0" />
                      {err}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* NEW: Extracted Data Table */}
            {result.invoice_data && (
              <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
                <div className="px-4 py-2 bg-slate-100 border-b border-slate-200 font-semibold text-xs text-slate-500 uppercase">
                  Extracted Data
                </div>
                <div className="divide-y divide-slate-100">
                  
                  <div className="flex justify-between px-4 py-3">
                    <span className="text-sm text-slate-500 flex items-center gap-2">
                      <Calendar className="w-4 h-4" /> Date
                    </span>
                    <span className="text-sm font-medium text-slate-900">
                      {result.invoice_data.invoice_date || "N/A"}
                    </span>
                  </div>

                  <div className="flex justify-between px-4 py-3">
                    <span className="text-sm text-slate-500 flex items-center gap-2">
                      <DollarSign className="w-4 h-4" /> Net Total
                    </span>
                    <span className="text-sm font-medium text-slate-900">
                      {result.invoice_data.net_total?.toFixed(2)} {result.invoice_data.currency}
                    </span>
                  </div>

                  <div className="flex justify-between px-4 py-3">
                    <span className="text-sm text-slate-500 flex items-center gap-2">
                      <DollarSign className="w-4 h-4" /> Tax
                    </span>
                    <span className="text-sm font-medium text-slate-900">
                      {result.invoice_data.tax_amount?.toFixed(2)} {result.invoice_data.currency}
                    </span>
                  </div>

                  <div className="flex justify-between px-4 py-3 bg-slate-50">
                    <span className="text-sm font-bold text-slate-700 flex items-center gap-2">
                      <DollarSign className="w-4 h-4" /> Gross Total
                    </span>
                    <span className="text-sm font-bold text-slate-900">
                      {result.invoice_data.gross_total?.toFixed(2)} {result.invoice_data.currency}
                    </span>
                  </div>

                </div>
              </div>
            )}

          </div>
        </div>
      )}
    </div>
  );
}