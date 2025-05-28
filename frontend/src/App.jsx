// src/App.jsx
import { useState } from 'react'
import './App.css'

function App() {
  const [keywords, setKeywords] = useState('')
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!keywords.trim()) {
      alert("请输入关键词")
      return
    }

    setLoading(true)

    try {
      // 1. 设置关键词
      await fetch('http://localhost:8000/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keywords: keywords.split(',') })
      })

      // 2. 触发后端手动任务
      await fetch('http://localhost:8000/run-task', { method: 'POST' })

      // 3. 获取摘要
      const res = await fetch('http://localhost:8000/summary')
      const data = await res.json()
      setSummary(data.summary)
    } catch (err) {
      console.error('请求失败:', err)
      setSummary('获取摘要失败，请检查后端是否运行')
    }

    setLoading(false)
  }

  return (
    <div className="app">
      <h1>新闻智能摘要</h1>
      <input
        type="text"
        placeholder="请输入关键词，例如：AI,芯片"
        value={keywords}
        onChange={e => setKeywords(e.target.value)}
      />
      <button onClick={handleSubmit}>生成摘要</button>

      {loading ? (
        <p>正在加载摘要...</p>
      ) : (
        <div className="summary-box">
          <h2>摘要结果：</h2>
          <p>{summary || '暂无摘要，请先输入关键词并生成'}</p>
        </div>
      )}
    </div>
  )
}

export default App
