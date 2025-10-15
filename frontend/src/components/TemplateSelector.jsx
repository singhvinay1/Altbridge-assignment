import React from 'react'

export default function TemplateSelector({ value, onChange }) {
  return (
    <div className="row">
      <label htmlFor="template">Template:</label>
      <select id="template" value={value} onChange={e => onChange(e.target.value)}>
        <option value="template1">Template 1</option>
        <option value="template2">Template 2</option>
      </select>
    </div>
  )
}



