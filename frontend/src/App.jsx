import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [jobId, setJobId] = useState(null)
  const [status, setStatus] = useState(null)
  const [progress, setProgress] = useState(0)
  const [videoUrl, setVideoUrl] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const API_URL = 'https://scaling-space-pancake-wrr9qvr5rq5539p7-8000.app.github.dev'

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setError(null)
    setVideoUrl(null)
    setJobId(null)
    setStatus(null)
    setProgress(0)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a video file')
      return
    }
    
    try {
      setIsLoading(true)
      setError(null)
      
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      })
      
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to upload video')
      }
      
      setJobId(data.job_id)
      setStatus('processing')
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    let interval
    
    if (jobId && status === 'processing') {
      interval = setInterval(async () => {
        try {
          const response = await fetch(`${API_URL}/status/${jobId}`)
          const data = await response.json()
          
          setProgress(data.progress || 0)
          setStatus(data.status)
          
          if (data.status === 'completed') {
            setVideoUrl(`${API_URL}${data.output_url}`)
            setIsLoading(false)
            clearInterval(interval)
          } else if (data.status === 'failed') {
            setError(data.error || 'Processing failed')
            setIsLoading(false)
            clearInterval(interval)
          }
        } catch (err) {
          setError('Failed to get status update')
          setIsLoading(false)
          clearInterval(interval)
        }
      }, 1000)
    }
    
    return () => {
      if (interval) {
        clearInterval(interval)
      }
    }
  }, [jobId, status])

  return (
    <div className="container">
      <h1>Cup Tracking App</h1>
      
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="file-input">
          <input 
            type="file" 
            id="videoFile" 
            accept="video/*" 
            onChange={handleFileChange} 
            disabled={isLoading}
          />
          <label htmlFor="videoFile" className={isLoading ? 'disabled' : ''}>
            {file ? file.name : 'Choose Video File'}
          </label>
        </div>
        
        <button type="submit" disabled={!file || isLoading} className="upload-btn">
          {isLoading ? 'Processing...' : 'Upload and Process'}
        </button>
      </form>
      
      {error && <div className="error-message">{error}</div>}
      
      {status === 'processing' && (
        <div className="progress-container">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="progress-text">{progress}% Complete</div>
        </div>
      )}
      
      {videoUrl && (
        <div className="result-container">
          <h2>Processed Video</h2>
          <video controls width="100%" src={videoUrl} />
        </div>
      )}
    </div>
  )
}

export default App
