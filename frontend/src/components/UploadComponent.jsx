import React from 'react'

export default function UploadComponent({ files = [], onFilesSelected, onRemoveFile }) {
  const onPick = e => {
    const picked = Array.from(e.target.files || [])
    onFilesSelected(picked)
  }

  return (
    <div>
      <div className="upload-box">
        <input
          type="file"
          accept="application/pdf"
          multiple
          onChange={onPick}
        />
      </div>
      {!!files.length && (
        <div className="file-list">
          {files.map((f, idx) => (
            <span key={idx} className="file-chip">
              <span className="name">{f.name}</span>
              <button aria-label={`Remove ${f.name}`} onClick={() => onRemoveFile(idx)}>×</button>
            </span>
          ))}
        </div>
      )}
    </div>
  )
}



