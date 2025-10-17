import React, { useState } from 'react'
import UploadComponent from './components/UploadComponent'
import TemplateSelector from './components/TemplateSelector'
import ProgressBar from './components/ProgressBar'
import DownloadButton from './components/DownloadButton'
import api from './api.js'

export default function App() {
  const [files, setFiles] = useState([])
  const [templateId, setTemplateId] = useState('template1')
  const [progress, setProgress] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [resultFilename, setResultFilename] = useState('')
  const [message, setMessage] = useState('')

  const onExtract = async () => {
    if (!files.length) return
    setIsLoading(true)
    setProgress(10)
    setMessage('Uploading and extracting...')
    setResultFilename('')
    try {
      const form = new FormData()
      files.forEach(f => form.append('files', f))
      form.append('template_id', templateId)

      const res = await api.post('/api/extract', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: evt => {
          if (evt.total) {
            const p = Math.round((evt.loaded / evt.total) * 40)
            setProgress(10 + p)
          }
        }
      })
      setProgress(80)
      setResultFilename(res.data.filename)
      setMessage('Extraction complete. Ready to download.')
      setProgress(100)
    } catch (e) {
      setMessage('Extraction failed. Please try again.')
      setProgress(0)
    } finally {
      setIsLoading(false)
    }
  }

  const onFilesSelected = (picked) => {
    // Merge newly picked files with existing, avoiding duplicates by name+size
    const existing = new Map(files.map(f => [f.name + ':' + f.size, f]))
    picked.forEach(f => existing.set(f.name + ':' + f.size, f))
    setFiles(Array.from(existing.values()))
  }

  const onRemoveFile = (idx) => {
    setFiles(prev => prev.filter((_, i) => i !== idx))
  }

  return (
    <div className="container">
      <h1 className="center">PDF Extraction Tool</h1>
      <div className="card">
        <UploadComponent files={files} onFilesSelected={onFilesSelected} onRemoveFile={onRemoveFile} />
      </div>
      <div className="card">
        <TemplateSelector value={templateId} onChange={setTemplateId} />
      </div>
      <div className="card row">
        <button className="btn extract" onClick={onExtract} disabled={isLoading || !files.length}>
          {isLoading ? (
            <>
              <span className="spinner" aria-hidden="true"></span>
              <span>Extracting…</span>
            </>
          ) : (
            <>
              <svg className="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path d="M12 3v12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <path d="M7 10l5 5 5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M5 19h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
              <span>Run Extraction</span>
            </>
          )}
        </button>
        <span className="muted">{message}</span>
      </div>
      <div className="card">
        <ProgressBar progress={progress} />
      </div>
      <div className="card">
        <DownloadButton filename={resultFilename} />
      </div>
    </div>
  )
}





