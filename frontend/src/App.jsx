import { useState, useRef } from 'react';
import { 
  Sparkles, 
  Upload, 
  Code, 
  FileText, 
  BookOpen, 
  ChevronRight, 
  ArrowRight, 
  CheckCircle2, 
  AlertTriangle, 
  Lightbulb, 
  RefreshCw, 
  FileCode, 
  Trash2,
  X,
  AlertCircle
} from 'lucide-react';
import './App.css';

// Base backend URL falls back to local FastAPI server
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [page, setPage] = useState('home'); // 'home' | 'analyze' | 'results'
  const [contentType, setContentType] = useState('code'); // 'code' | 'notes' | 'document'
  const [content, setContent] = useState('');
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  
  const fileInputRef = useRef(null);

  // Drag and drop handlers
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    // Only support .docx files
    const filename = selectedFile.name.toLowerCase();
    if (!filename.endsWith('.docx')) {
      setError({
        title: 'Invalid File Type',
        text: 'HackLens currently supports only Microsoft Word (.docx) files.'
      });
      return;
    }
    setError(null);
    setFile(selectedFile);
    setContentType('document'); // Automatically switch to document type
  };

  const removeFile = (e) => {
    e.stopPropagation();
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleAnalyze = async () => {
    if (!content && !file) {
      setError({
        title: 'Input Required',
        text: 'Please enter code/notes or upload a .docx document before analyzing.'
      });
      return;
    }

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('content_type', contentType);
    
    if (file) {
      formData.append('file', file);
    }
    if (content) {
      formData.append('content', content);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorDetail = 'Backend analysis failed.';
        try {
          const errData = await response.json();
          errorDetail = errData.detail || errorDetail;
        } catch (_) {
          // ignore parsing error
        }
        throw new Error(errorDetail);
      }

      const data = await response.json();
      setResults(data);
      setPage('results');
    } catch (err) {
      console.error(err);
      setError({
        title: 'Analysis Error',
        text: err.message || 'Could not connect to the evaluation server. Make sure the backend is running.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFile(null);
    setContent('');
    setError(null);
    setResults(null);
    setPage('analyze');
  };

  // Scores are always 0-10 from backend
  const formatScore = (score) => {
    if (score === undefined || score === null) return '0.0';
    return parseFloat(score).toFixed(1);
  };

  return (
    <div className={`app-container page-${page}`}>
      {/* Header / Navigation */}
      <header className="header">
        <div className="nav-content">
          <div className="logo-container" onClick={() => setPage('home')}>
            <Sparkles className="logo-icon animate-pulse" />
            <span className="logo-text">Hack<span style={{ color: 'var(--accent)' }}>Lens</span></span>
          </div>
          <nav>
            <ul className="nav-links">
              <li>
                <button 
                  className={`nav-button ${page === 'home' ? 'active' : ''}`}
                  onClick={() => setPage('home')}
                >
                  Home
                </button>
              </li>
              <li>
                <button 
                  className={`nav-button ${page === 'analyze' ? 'active' : ''}`}
                  onClick={() => {
                    setError(null);
                    setPage('analyze');
                  }}
                >
                  Analyze
                </button>
              </li>
              {results && (
                <li>
                  <button 
                    className={`nav-button ${page === 'results' ? 'active' : ''}`}
                    onClick={() => setPage('results')}
                  >
                    Results
                  </button>
                </li>
              )}
            </ul>
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="main-content">
        
        {/* 🏠 Page 1: Landing Page (Home) */}
        {page === 'home' && (
          <div className="animated">
            <section className="hero-section">
              <div className="badge">
                <Sparkles size={14} />
                Now Powered by Groq AI
              </div>
              <h1 className="hero-title">
                HackLens<br />
                <span className="gradient-text">AI-Powered Technical Evaluator</span>
              </h1>
              <p className="hero-subtitle">
                Upload code snippets or technical documents and receive structured AI-driven feedback, scores, and improvement suggestions instantly.
              </p>
              <button className="cta-button" onClick={() => setPage('analyze')}>
                Analyze Content
                <ArrowRight size={18} />
              </button>
            </section>

            <section className="features-section">
              <div className="feature-card">
                <div className="feature-icon-container">
                  <Code className="feature-icon" />
                </div>
                <h3>Technical Review</h3>
                <p>Analyze code quality, structure, performance, and adherence to programming best practices.</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon-container">
                  <Sparkles className="feature-icon" />
                </div>
                <h3>Smart Feedback</h3>
                <p>Identify code strengths, highlighting positive aspects, design weaknesses, and logical errors.</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon-container">
                  <FileText className="feature-icon" />
                </div>
                <h3>Document Evaluation</h3>
                <p>Review technical notes, design docs, requirements sheets, or system architecture documents instantly.</p>
              </div>
            </section>
          </div>
        )}

        {/* 📄 Page 2: Analyze Page */}
        {page === 'analyze' && !isLoading && (
          <div className="animated analyze-grid">
            <div className="card">
              <h2 style={{ color: '#fff', fontSize: '1.75rem', fontWeight: 700, marginBottom: '2rem', textAlign: 'center' }}>
                Start AI Evaluation
              </h2>

              {error && (
                <div className="error-message">
                  <AlertCircle className="error-icon" />
                  <div className="error-details">
                    <div className="error-title">{error.title}</div>
                    <div className="error-text">{error.text}</div>
                  </div>
                  <button style={{ background: 'none', border: 'none', color: '#fca5a5', cursor: 'pointer', padding: '0.2rem' }} onClick={() => setError(null)}>
                    <X size={16} />
                  </button>
                </div>
              )}

              <div className="form-group">
                <label className="form-label">Select Content Type</label>
                <div className="select-wrapper">
                  <select 
                    className="select-input" 
                    value={contentType} 
                    onChange={(e) => setContentType(e.target.value)}
                  >
                    <option value="code">Code (Python, JS, C++, Go, etc.)</option>
                    <option value="notes">Technical Notes / Snippets</option>
                    <option value="document">Documentation / System Design (.docx)</option>
                  </select>
                  <ChevronRight size={18} className="select-icon" style={{ transform: 'rotate(90deg)' }} />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Upload Document (.docx)</label>
                <input 
                  type="file" 
                  ref={fileInputRef}
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                  accept=".docx"
                />
                
                <div 
                  className={`upload-zone ${dragging ? 'dragging' : ''}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <Upload className="upload-icon" />
                  {file ? (
                    <div className="file-info-badge">
                      <FileCode size={16} />
                      <span style={{ fontWeight: 500 }}>{file.name}</span>
                      <button className="remove-file-btn" onClick={removeFile}>
                        <Trash2 size={16} />
                      </button>
                    </div>
                  ) : (
                    <>
                      <div className="upload-title">Drag & Drop DOCX here</div>
                      <div className="upload-subtitle">or click to browse from computer (Max 10MB)</div>
                    </>
                  )}
                </div>
              </div>

              <div className="divider">OR</div>

              <div className="form-group">
                <label className="form-label">Paste Content / Code</label>
                <textarea 
                  className="textarea-input"
                  placeholder={
                    contentType === 'code' 
                      ? 'def add(a, b):\n    # paste your code here\n    return a + b' 
                      : contentType === 'notes' 
                      ? 'Paste your technical notes or study snippets here...' 
                      : 'Paste plain text content of your document here...'
                  }
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                />
              </div>

              <button 
                className="submit-button" 
                onClick={handleAnalyze}
                disabled={!content && !file}
              >
                Analyze Content
                <Sparkles size={18} />
              </button>
            </div>
          </div>
        )}

        {/* ⏳ Loading / Spinner state */}
        {isLoading && (
          <div className="animated loading-overlay">
            <div className="spinner"></div>
            <div className="loading-text">Analyzing your content...</div>
            <div className="loading-subtext">Groq LLM is scanning for bugs, structure, and formatting. Please hold.</div>
          </div>
        )}

        {/* 📊 Page 3: Results Page */}
        {page === 'results' && !isLoading && results && (
          <div className="animated results-container">
            <div className="results-header">
              <div className="score-badge">
                <div className="score-number">{formatScore(results.evaluation_score)}</div>
                <div className="score-max">/ 10</div>
              </div>
              <h2 className="score-label">Evaluation Complete</h2>
              <p className="score-meta" style={{ marginBottom: '1.5rem' }}>
                We've evaluated your submitted {contentType} using llama-3.1-8b-instant.
              </p>

              {/* Rating Breakdown & Formula Card */}
              <div className="formula-container">
                <h3 className="formula-title">Rating Breakdown & Formula</h3>
                <div className="formula-grid">
                  <div className="formula-item">
                    <span className="formula-item-label">Technical Quality</span>
                    <span className="formula-item-value">{results.technical_quality?.toFixed(1) || '0.0'}/10</span>
                  </div>
                  <div className="formula-item">
                    <span className="formula-item-label">Structure</span>
                    <span className="formula-item-value">{results.structure?.toFixed(1) || '0.0'}/10</span>
                  </div>
                  <div className="formula-item">
                    <span className="formula-item-label">Clarity</span>
                    <span className="formula-item-value">{results.clarity?.toFixed(1) || '0.0'}/10</span>
                  </div>
                  <div className="formula-item">
                    <span className="formula-item-label">Best Practices</span>
                    <span className="formula-item-value">{results.best_practices?.toFixed(1) || '0.0'}/10</span>
                  </div>
                </div>
                <div className="formula-calculation">
                  <span className="formula-math-label">Formula Used:</span>
                  <code className="formula-math-expression">
                    ({results.technical_quality?.toFixed(1) || '0.0'} + {results.structure?.toFixed(1) || '0.0'} + {results.clarity?.toFixed(1) || '0.0'} + {results.best_practices?.toFixed(1) || '0.0'}) / 4 = {formatScore(results.evaluation_score)} / 10
                  </code>
                </div>
              </div>
            </div>

            <div className="results-grid">
              {/* Strengths Card */}
              <div className="analysis-card">
                <div className="analysis-card-title strengths-title">
                  <CheckCircle2 className="analysis-icon" />
                  <span>Strengths</span>
                </div>
                <ul className="analysis-list">
                  {results.strengths && results.strengths.length > 0 ? (
                    results.strengths.map((str, idx) => (
                      <li key={idx} className="analysis-item strength">
                        <span className="analysis-icon">✓</span>
                        <span className="analysis-item-text">{str}</span>
                      </li>
                    ))
                  ) : (
                    <li className="analysis-item" style={{ color: 'var(--text-dark)' }}>No notable strengths detected.</li>
                  )}
                </ul>
              </div>

              {/* Weaknesses Card */}
              <div className="analysis-card">
                <div className="analysis-card-title weaknesses-title">
                  <AlertTriangle className="analysis-icon" />
                  <span>Weaknesses</span>
                </div>
                <ul className="analysis-list">
                  {results.weaknesses && results.weaknesses.length > 0 ? (
                    results.weaknesses.map((weak, idx) => (
                      <li key={idx} className="analysis-item weakness">
                        <span className="analysis-icon">⚠</span>
                        <span className="analysis-item-text">{weak}</span>
                      </li>
                    ))
                  ) : (
                    <li className="analysis-item" style={{ color: 'var(--text-dark)' }}>No notable weaknesses detected! Great job.</li>
                  )}
                </ul>
              </div>

              {/* Suggestions Card */}
              <div className="analysis-card">
                <div className="analysis-card-title suggestions-title">
                  <Lightbulb className="analysis-icon" />
                  <span>Suggestions</span>
                </div>
                <ul className="analysis-list">
                  {results.suggestions && results.suggestions.length > 0 ? (
                    results.suggestions.map((sug, idx) => (
                      <li key={idx} className="analysis-item suggestion">
                        <span className="analysis-icon">💡</span>
                        <span className="analysis-item-text">{sug}</span>
                      </li>
                    ))
                  ) : (
                    <li className="analysis-item" style={{ color: 'var(--text-dark)' }}>No actionable suggestions. Code looks production ready!</li>
                  )}
                </ul>
              </div>
            </div>

            <div className="back-btn-container">
              <button className="back-button" onClick={resetForm}>
                <RefreshCw size={16} />
                Analyze New Content
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Footer Section */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-text">Built using FastAPI + Groq AI</div>
          <div className="badge-group">
            <span className="tech-badge fastapi">FastAPI Backend</span>
            <span className="tech-badge groq">Groq llama-3.1</span>
            <span className="tech-badge">React SPA</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
