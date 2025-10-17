import React from 'react'

export default function DownloadButton({ filename, fileData }) {
  const onDownload = () => {
    if (!filename || !fileData) return
    
    // Convert base64 to blob and download directly
    const byteCharacters = atob(fileData)
    const byteNumbers = new Array(byteCharacters.length)
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], { 
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
    })
    
    // Create download link
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }

  return (
    <div className="row">
      <button className="btn download" onClick={onDownload} disabled={!filename || !fileData}>
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



