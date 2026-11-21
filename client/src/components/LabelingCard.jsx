import React from 'react';

export default function LabelingCard({ pair, onChoose, isSubmitting }) {
  if (!pair) return null;

  return (
    <div id="pair-container">
      {/* Prompt Card */}
      <div className="prompt-card">
        <div className="prompt-meta">
          <span className="category-tag">
            {(pair.category || 'General').replace('_', ' ')}
          </span>
          <span className="pair-id-tag">Pair #{pair.id}</span>
        </div>
        <h2 className="prompt-text">{pair.prompt}</h2>
      </div>

      {/* Side-by-side Response Comparison */}
      <div className="comparison-grid">
        {/* Response A */}
        <div className="response-card" id="card-response-a">
          <div className="response-header">
            <span className="response-title">
              <span className="response-badge-a">A</span> Response A
            </span>
            <span className="kbd-badge">Key [A]</span>
          </div>
          <div className="response-content">{pair.response_a}</div>
          <button
            className="action-btn btn-choose-a"
            onClick={() => onChoose('A')}
            disabled={isSubmitting}
          >
            👍 Response A is Better
          </button>
        </div>

        {/* Response B */}
        <div className="response-card" id="card-response-b">
          <div className="response-header">
            <span className="response-title">
              <span className="response-badge-b">B</span> Response B
            </span>
            <span className="kbd-badge">Key [B]</span>
          </div>
          <div className="response-content">{pair.response_b}</div>
          <button
            className="action-btn btn-choose-b"
            onClick={() => onChoose('B')}
            disabled={isSubmitting}
          >
            👍 Response B is Better
          </button>
        </div>
      </div>

      {/* Secondary Actions */}
      <div className="secondary-actions">
        <button
          className="btn-secondary btn-tie"
          onClick={() => onChoose('tie')}
          disabled={isSubmitting}
        >
          🤝 Equal Quality / Tie <span className="kbd-badge">T</span>
        </button>
        <button
          className="btn-secondary btn-skip"
          onClick={() => onChoose('skip')}
          disabled={isSubmitting}
        >
          ⏭️ Skip Pair <span className="kbd-badge">S</span>
        </button>
      </div>
    </div>
  );
}

