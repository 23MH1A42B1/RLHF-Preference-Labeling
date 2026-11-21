import React from 'react';

export default function ProgressBar({ labeled = 0, total = 0, percentage = 0 }) {
  return (
    <div className="progress-section">
      <div className="progress-info">
        <span>Labeled {labeled} of {total} pairs</span>
        <span>{percentage}%</span>
      </div>
      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

