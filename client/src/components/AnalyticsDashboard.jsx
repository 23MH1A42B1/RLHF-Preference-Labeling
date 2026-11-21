import React from 'react';

export default function AnalyticsDashboard({ analytics, onRefresh }) {
  if (!analytics) return <div>Loading analytics...</div>;

  const total = analytics.total_labels || 0;
  const dist = analytics.label_distribution || { A: 0, B: 0, tie: 0, skip: 0 };
  const agreement = analytics.agreement_rate !== undefined ? analytics.agreement_rate : 1.0;
  const agreementPct = Math.round(agreement * 100);
  const kappa = analytics.cohens_kappa !== undefined ? analytics.cohens_kappa : 1.0;

  const getPct = (cnt) => (total > 0 ? Math.round((cnt / total) * 100) : 0);
  const catData = analytics.category_breakdown || {};
  const catKeys = Object.keys(catData);

  return (
    <div>
      {/* KPI Cards */}
      <div className="analytics-grid">
        <div className="kpi-card kpi-blue">
          <div className="kpi-label">Total Completed Labels</div>
          <div className="kpi-value">{total}</div>
          <div className="kpi-subtext">Across all annotators</div>
        </div>

        <div className="kpi-card kpi-green">
          <div className="kpi-label">Inter-Rater Agreement</div>
          <div className="kpi-value">{agreementPct}%</div>
          <div className="kpi-subtext">
            {analytics.multi_labeled_pairs_count > 0
              ? `Based on ${analytics.multi_labeled_pairs_count} multi-rated pairs`
              : 'Single annotator baseline'}
          </div>
        </div>

        <div className="kpi-card kpi-purple">
          <div className="kpi-label">Multi-Rated Pairs</div>
          <div className="kpi-value">{analytics.multi_labeled_pairs_count || 0}</div>
          <div className="kpi-subtext">Pairs with &gt; 1 judgment</div>
        </div>

        <div className="kpi-card kpi-orange">
          <div className="kpi-label">Cohen's Kappa (κ)</div>
          <div className="kpi-value">{kappa.toFixed(2)}</div>
          <div className="kpi-subtext">Chance-adjusted agreement</div>
        </div>
      </div>

      {/* Label Distribution */}
      <div className="chart-card">
        <div className="card-title">
          <span>Preference Label Distribution</span>
          <button className="btn-secondary" onClick={onRefresh} style={{ padding: '0.35rem 0.8rem' }}>
            🔄 Refresh Metrics
          </button>
        </div>

        <div className="dist-bar-group">
          <div className="dist-label-row">
            <span>Response A Preferred</span>
            <span>{dist.A || 0} ({getPct(dist.A || 0)}%)</span>
          </div>
          <div className="dist-bar-track">
            <div className="dist-bar-fill fill-a" style={{ width: `${getPct(dist.A || 0)}%` }} />
          </div>
        </div>

        <div className="dist-bar-group">
          <div className="dist-label-row">
            <span>Response B Preferred</span>
            <span>{dist.B || 0} ({getPct(dist.B || 0)}%)</span>
          </div>
          <div className="dist-bar-track">
            <div className="dist-bar-fill fill-b" style={{ width: `${getPct(dist.B || 0)}%` }} />
          </div>
        </div>

        <div className="dist-bar-group">
          <div className="dist-label-row">
            <span>Tie / Indifferent</span>
            <span>{dist.tie || 0} ({getPct(dist.tie || 0)}%)</span>
          </div>
          <div className="dist-bar-track">
            <div className="dist-bar-fill fill-tie" style={{ width: `${getPct(dist.tie || 0)}%` }} />
          </div>
        </div>

        <div className="dist-bar-group">
          <div className="dist-label-row">
            <span>Skipped</span>
            <span>{dist.skip || 0} ({getPct(dist.skip || 0)}%)</span>
          </div>
          <div className="dist-bar-track">
            <div className="dist-bar-fill fill-skip" style={{ width: `${getPct(dist.skip || 0)}%` }} />
          </div>
        </div>
      </div>

      {/* Category Breakdown Table */}
      <div className="chart-card">
        <div className="card-title">Category Breakdown</div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Category</th>
              <th>Total Labels</th>
              <th>Chose A</th>
              <th>Chose B</th>
              <th>Ties</th>
              <th>Skips</th>
            </tr>
          </thead>
          <tbody>
            {catKeys.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                  No labels recorded yet.
                </td>
              </tr>
            ) : (
              catKeys.map((cat) => (
                <tr key={cat}>
                  <td><strong>{cat.replace('_', ' ')}</strong></td>
                  <td>{catData[cat].total || 0}</td>
                  <td style={{ color: '#60a5fa' }}>{catData[cat].A || 0}</td>
                  <td style={{ color: '#c084fc' }}>{catData[cat].B || 0}</td>
                  <td style={{ color: '#fcd34d' }}>{catData[cat].tie || 0}</td>
                  <td style={{ color: '#f87171' }}>{catData[cat].skip || 0}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

