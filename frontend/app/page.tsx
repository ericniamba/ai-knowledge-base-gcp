'use client'

import { useState, useEffect } from 'react'

export default function Home() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState('')
  const [documents, setDocuments] = useState([])

  useEffect(() => {
    fetchDocuments()
  }, [])

  const fetchDocuments = async () => {
    try {
      const response = await fetch('/api/v1/documents')
      const data = await response.json()
      setDocuments(data.documents || [])
    } catch (error) {
      console.error('Error fetching documents:', error)
    }
  }

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    setUploadStatus('Uploading document...')
    const formData = new FormData()
    formData.append('file', file)
    try {
      const response = await fetch('/api/v1/documents/upload', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      setUploadStatus(`✅ ${file.name} uploaded successfully!`)
      fetchDocuments()
    } catch (error) {
      setUploadStatus('❌ Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  const handleAsk = async () => {
    if (!question.trim()) return
    setLoading(true)
    setAnswer('')
    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })
      const data = await response.json()
      setAnswer(data.answer)
    } catch (error) {
      setAnswer('❌ Error getting answer. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      <div className="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-blue-400">AI Knowledge Base</h1>
            <p className="text-gray-400 text-sm">Powered by Google Vertex AI + GKE</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
            <span className="text-green-400 text-sm">Live on GCP</span>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-10">

        {/* Upload Section */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-6">
          <h2 className="text-lg font-semibold mb-2 text-white">📄 Upload Document</h2>
          <p className="text-gray-400 text-sm mb-4">Upload a PDF or TXT file to add to your knowledge base</p>
          <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-700 rounded-lg cursor-pointer hover:border-blue-500 transition-colors">
            <div className="text-center">
              <p className="text-gray-400 text-sm">{uploading ? 'Uploading...' : 'Click to upload or drag and drop'}</p>
              <p className="text-gray-600 text-xs mt-1">PDF, TXT, DOCX</p>
            </div>
            <input type="file" className="hidden" accept=".pdf,.txt,.docx" onChange={handleUpload} disabled={uploading}/>
          </label>
          {uploadStatus && <p className="mt-3 text-sm text-blue-400">{uploadStatus}</p>}
        </div>

        {/* Documents List */}
        {documents.length > 0 && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4 text-white">📚 Knowledge Base ({documents.length} documents)</h2>
            <div className="space-y-2">
              {documents.map((doc: any, i) => (
                <div key={i} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-3">
                  <div className="flex items-center gap-3">
                    <span className="text-blue-400">📄</span>
                    <span className="text-gray-200 text-sm">{doc.filename}</span>
                  </div>
                  <span className="text-gray-500 text-xs">{doc.chunks} chunks</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Chat Section */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-2 text-white">💬 Ask Your Documents</h2>
          <p className="text-gray-400 text-sm mb-4">Ask any question about your uploaded documents</p>
          <div className="flex gap-3 mb-4">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
              placeholder="Ask a question about your documents..."
              className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleAsk}
              disabled={loading || !question.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {loading ? 'Thinking...' : 'Ask'}
            </button>
          </div>
          {answer && (
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
              <p className="text-xs text-blue-400 font-mono mb-2">AI ANSWER — VERTEX AI + GEMINI 2.5 FLASH</p>
              <p className="text-gray-200 leading-relaxed">{answer}</p>
            </div>
          )}
          {loading && (
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
              <p className="text-gray-400 text-sm animate-pulse">Gemini 2.5 Flash is thinking...</p>
            </div>
          )}
        </div>

        <div className="text-center mt-8 text-gray-600 text-xs font-mono">
          Built by Eric Niamba · GKE + Terraform + Vertex AI + Cloud SQL + pgvector
        </div>
      </div>
    </main>
  )
}
