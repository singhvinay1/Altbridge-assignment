import React from 'react'

export default function DownloadButton({ filename }) {
  const onDownload = () => {
    if (!filename) return
    // Create a temporary link element for download
    const url = `/api/download/${encodeURIComponent(filename)}`
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="row">
      <button className="btn download" onClick={onDownload} disabled={!filename}>
        <svg className="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M12 3v12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M7 10l5 5 5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M5 19h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
        </svg>
        <span>Download Excel</span>
      </button>
      <span className="muted">{filename ? `Ready: ${filename}` : 'No file yet'}</span>
    </div>
  )
}



