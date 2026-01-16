import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [email, setEmail] = useState('')
  const [courseNumber, setCourseNumber] = useState('')
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ text: '', type: '' })

  useEffect(() => {
    if (email) {
      loadCourses()
    }
  }, [email])

  const showMessage = (text, type = 'success') => {
    setMessage({ text, type })
    setTimeout(() => setMessage({ text: '', type: '' }), 5000)
  }

  const loadCourses = async () => {
    if (!email) {
      showMessage('이메일을 입력해주세요.', 'error')
      return
    }

    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/api/courses`, {
        params: { email }
      })
      setCourses(response.data)
    } catch (error) {
      showMessage('수업 목록을 불러오는 중 오류가 발생했습니다.', 'error')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!courseNumber || !email) {
      showMessage('수업 번호와 이메일을 모두 입력해주세요.', 'error')
      return
    }

    try {
      setLoading(true)
      const response = await axios.post(`${API_URL}/api/courses`, {
        course_number: courseNumber.trim(),
        email: email.trim()
      })
      showMessage(response.data.message, 'success')
      setCourseNumber('')
      loadCourses()
    } catch (error) {
      const errorMsg = error.response?.data?.detail || '수업 등록 중 오류가 발생했습니다.'
      showMessage(errorMsg, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (courseId) => {
    if (!confirm('정말 이 수업 모니터링을 중단하시겠습니까?')) {
      return
    }

    try {
      setLoading(true)
      await axios.delete(`${API_URL}/api/courses/${courseId}`)
      showMessage('수업이 삭제되었습니다.', 'success')
      loadCourses()
    } catch (error) {
      showMessage('삭제 중 오류가 발생했습니다.', 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🎓 USC 수업 크롤러</h1>
          <p>수업 자리를 모니터링하고 알림을 받아보세요</p>
        </header>

        {message.text && (
          <div className={`alert alert-${message.type}`}>
            {message.text}
          </div>
        )}

        <div className="card">
          <h2>새 수업 등록</h2>
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="course-number">수업 번호</label>
              <input
                id="course-number"
                type="text"
                placeholder="예: 535"
                value={courseNumber}
                onChange={(e) => setCourseNumber(e.target.value)}
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">이메일</label>
              <input
                id="email"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
              />
            </div>
            <button type="submit" disabled={loading} className="btn btn-primary">
              {loading ? '처리 중...' : '수업 등록하기'}
            </button>
          </form>
        </div>

        <div className="card">
          <h2>내 수업 목록</h2>
          {email ? (
            <>
              <button 
                onClick={loadCourses} 
                disabled={loading}
                className="btn btn-secondary"
                style={{ marginBottom: '20px' }}
              >
                {loading ? '로딩 중...' : '새로고침'}
              </button>
              
              {courses.length === 0 ? (
                <div className="empty-state">
                  <p>등록된 수업이 없습니다.</p>
                  <p className="hint">위에서 수업 번호와 이메일을 입력하고 등록해주세요.</p>
                </div>
              ) : (
                <div className="courses-grid">
                  {courses.map((course) => (
                    <div key={course.id} className="course-card">
                      <div className="course-header">
                        <h3>{course.course_name || `CSCI ${course.course_number}`}</h3>
                        <span className={`badge ${course.is_available ? 'badge-success' : 'badge-danger'}`}>
                          {course.is_available ? '✅ 자리 있음' : '❌ 만석'}
                        </span>
                      </div>
                      <div className="course-info">
                        <div className="info-item">
                          <span className="label">등록인원:</span>
                          <span className="value">{course.current_registered || '확인 중...'}</span>
                        </div>
                        <div className="info-item">
                          <span className="label">등록일:</span>
                          <span className="value">
                            {new Date(course.created_at).toLocaleString('ko-KR')}
                          </span>
                        </div>
                      </div>
                      <button
                        onClick={() => handleDelete(course.id)}
                        disabled={loading}
                        className="btn btn-danger btn-small"
                      >
                        삭제
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </>
          ) : (
            <div className="empty-state">
              <p>이메일을 입력하면 등록된 수업 목록을 확인할 수 있습니다.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
