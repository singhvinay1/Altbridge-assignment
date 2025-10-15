import React from 'react'

export default function ProgressBar({ progress = 0 }) {
  return (
    <div className="progress">
      <div style={{ width: `${Math.max(0, Math.min(100, progress))}%` }} />
    </div>
  )
}



