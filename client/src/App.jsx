import React, { useState, useEffect, useCallback } from 'react';
import ProgressBar from './components/ProgressBar';
import LabelingCard from './components/LabelingCard';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import ExportModal from './components/ExportModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('labeling');
  const [annotatorId, setAnnotatorId] = useState('annotator_1');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [currentPair, setCurrentPair] = useState(null);
  const [progress, setProgress] = useState({ labeled: 0, total: 0, percentage: 0 });
  const [analytics, setAnalytics] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [toastMessage, setToastMessage] = useState(null);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 2500);
  };

  const fetchNextPair = useCallback(async () => {
    let url = `/api/pairs/next?annotator_id=${encodeURIComponent(annotatorId)}`;
    if (categoryFilter) {
      url += `&category=${encodeURIComponent(categoryFilter)}`;
    }
    try {
      const res = await fetch(url);
      if (res.status === 200) {
        const data = await res.json();
        setCurrentPair(data);
        setIsCompleted(false);
      } else if (res.status === 404) {
        setCurrentPair(null);
        setIsCompleted(true);
      }
    } catch (err) {
      console.error(err);
    }
  }, [annotatorId, categoryFilter]);

  const fetchProgress = useCallback(async () => {
    try {
      const res = await fetch(`/api/pairs/progress?annotator_id=${encodeURIComponent(annotatorId)}`);
      if (res.ok) {
        const data = await res.json();
        setProgress({
          labeled: data.labeled_pairs,
          total: data.total_pairs,
          percentage: data.completion_percentage,
        });
      }
    } catch (err) {
      console.error(err);
    }
  }, [annotatorId]);

  const fetchAnalytics = useCallback(async () => {
    try {
      const res = await fetch('/api/analytics');
      if (res.ok) {
        const data = await res.json();
        setAnalytics(data);
      }
    } catch (err) {
      console.error(err);
    }
  }, []);

  useEffect(() => {
    fetchNextPair();
    fetchProgress();
  }, [fetchNextPair, fetchProgress]);

  useEffect(() => {
    if (activeTab === 'analytics') {
      fetchAnalytics();
    }
  }, [activeTab, fetchAnalytics]);

  const handleChoose = async (choice) => {
    if (!currentPair || isSubmitting) return;
    setIsSubmitting(true);
    try {
      const res = await fetch('/api/labels', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pair_id: currentPair.id,
          annotator_id: annotatorId,
          chosen: choice,
        }),
      });
      if (res.status === 201) {
        showToast(`Recorded choice: ${choice}`);
        await fetchNextPair();
        await fetchProgress();
      }
    } catch (err) {
      showToast('Submission failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Keyboard Shortcuts (A, B, T, S)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;
      const key = e.key.toLowerCase();
      if (key === 'a') {
        e.preventDefault();
        handleChoose('A');
      } else if (key === 'b') {
        e.preventDefault();
        handleChoose('B');
      } else if (key === 't') {
        e.preventDefault();
        handleChoose('tie');
      } else if (key === 's') {
        e.preventDefault();
        handleChoose('skip');
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentPair, isSubmitting, annotatorId]);

  return (
    <div>
      {/* Header */}
      <header className="navbar">
        <div className="nav-brand">
          <span className="brand-badge">RLHF Core</span>
          <h1 className="nav-title">Preference Alignment Studio</h1>
        </div>

        <nav className="nav-tabs">
          <button
            className={`tab-btn ${activeTab === 'labeling' ? 'active' : ''}`}
            onClick={() => setActiveTab('labeling')}
          >
            🏷️ Labeling Studio
          </button>
          <button
            className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setActiveTab('analytics')}
          >
            📊 Analytics &amp; Agreement
          </button>
          <button
            className={`tab-btn ${activeTab === 'export' ? 'active' : ''}`}
            onClick={() => setActiveTab('export')}
          >
            📦 Dataset Export
          </button>
        </nav>

        <div className="nav-user">
          <div className="annotator-select-container">
            <span className="annotator-label">Annotator:</span>
            <input
              type="text"
              className="annotator-input"
              value={annotatorId}
              onChange={(e) => setAnnotatorId(e.target.value.trim() || 'annotator_1')}
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'labeling' && (
          <div>
            <div className="control-bar">
              <ProgressBar
                labeled={progress.labeled}
                total={progress.total}
                percentage={progress.percentage}
              />
              <div className="filter-section">
                <label htmlFor="cat-filter" style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
                  Category:
                </label>
                <select
                  id="cat-filter"
                  className="filter-select"
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                >
                  <option value="">All Categories (50+)</option>
                  <option value="factual_qa">Factual QA</option>
                  <option value="code_generation">Code Generation</option>
                  <option value="creative_writing">Creative Writing</option>
                  <option value="summarization">Summarization</option>
                  <option value="reasoning">Reasoning</option>
                </select>
              </div>
              <div className="shortcut-legend">
                <span>Shortcuts:</span>
                <span><span className="kbd-badge">A</span> Left</span>
                <span><span className="kbd-badge">B</span> Right</span>
                <span><span className="kbd-badge">T</span> Tie</span>
                <span><span className="kbd-badge">S</span> Skip</span>
              </div>
            </div>

            {!isCompleted ? (
              <LabelingCard
                pair={currentPair}
                onChoose={handleChoose}
                isSubmitting={isSubmitting}
              />
            ) : (
              <div className="completed-card">
                <div className="completed-icon">🎉</div>
                <h2 className="completed-title">All Pairs Labeled!</h2>
                <p className="completed-desc">
                  You have completed all available prompt pairs for this annotator.
                  Switch annotator ID in the header to simulate multiple raters or inspect agreement metrics!
                </p>
                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                  <button className="action-btn btn-choose-a" style={{ width: 'auto' }} onClick={() => setActiveTab('analytics')}>
                    📊 View Analytics &amp; Agreement
                  </button>
                  <button className="action-btn btn-choose-b" style={{ width: 'auto' }} onClick={() => setActiveTab('export')}>
                    📦 Export Labeled Dataset
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'analytics' && (
          <AnalyticsDashboard analytics={analytics} onRefresh={fetchAnalytics} />
        )}

        {activeTab === 'export' && <ExportModal />}
      </main>

      {/* Toast Notification */}
      {toastMessage && (
        <div className="toast-container">
          <div className="toast">{toastMessage}</div>
        </div>
      )}
    </div>
  );
}

