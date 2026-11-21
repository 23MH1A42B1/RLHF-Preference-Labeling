import React, { useState, useEffect } from 'react';

export default function ExportModal() {
  const [category, setCategory] = useState('');
  const [preview, setPreview] = useState('Loading export preview...');

  const fetchPreview = async () => {
    let url = '/api/export';
    if (category) url += `?category=${encodeURIComponent(category)}`;
    try {
      const res = await fetch(url);
      if (res.ok) {
        const text = await res.text();
        const lines = text.trim().split('\n').filter((l) => l.trim().length > 0);
        if (lines.length === 0) {
          setPreview('// No preference labels exported yet.\n// Complete pairwise annotations to generate training data.');
        } else {
          const parsed = lines.slice(0, 3).map((l) => JSON.stringify(JSON.parse(l), null, 2));
          setPreview(parsed.join('\n\n') + (lines.length > 3 ? `\n\n... and ${lines.length - 3} more records.` : ''));
        }
      }
    } catch (e) {
      setPreview('Failed to load export preview.');
    }
  };

  useEffect(() => {
    fetchPreview();
  }, [category]);

  const downloadUrl = `/api/export${category ? `?category=${encodeURIComponent(category)}` : ''}`;

  return (
    <div className="export-card">
      <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '0.5rem' }}>
        Export RLHF Reward Model Training Dataset
      </h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.95rem' }}>
        Export labeled prompt-preference pairs formatted according to standard JSONL RLHF specifications
        (<code>prompt</code>, <code>chosen</code>, <code>rejected</code>) ready for model alignment.
      </p>

      <div className="export-controls">
        <label htmlFor="export-cat" style={{ fontWeight: 600, fontSize: '0.9rem' }}>
          Category Filter:
        </label>
        <select
          id="export-cat"
          className="filter-select"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="">All Categories (Complete Dataset)</option>
          <option value="factual_qa">Factual QA</option>
          <option value="code_generation">Code Generation</option>
          <option value="creative_writing">Creative Writing</option>
          <option value="summarization">Summarization</option>
          <option value="reasoning">Reasoning</option>
        </select>

        <a
          href={downloadUrl}
          className="action-btn btn-choose-a"
          style={{ width: 'auto', textDecoration: 'none' }}
          download="labels.jsonl"
        >
          📥 Download labels.jsonl
        </a>
      </div>

      <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem' }}>
        Live JSONL Dataset Preview:
      </h3>
      <pre className="json-preview">{preview}</pre>

      <div style={{ backgroundColor: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)', padding: '1.25rem' }}>
        <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '0.5rem' }}>
          🔬 Downstream Pipeline Validation Stub
        </h4>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
          Simulate downstream consumption with the included validation stub:
        </p>
        <div className="code-snippet">python downstream/validate_data.py labels.jsonl</div>
      </div>
    </div>
  );
}

