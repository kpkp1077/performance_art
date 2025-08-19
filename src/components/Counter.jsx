import React from 'react'

const Counter = ({ count, setCount }) => {
  return (
    <div style={{ margin: '2rem 0' }}>
      <div className="counter-display">{count}</div>
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
        <button 
          className="cta-button" 
          onClick={() => setCount((count) => count + 1)}
          style={{ background: 'linear-gradient(45deg, #4ecdc4, #44a08d)' }}
        >
          Increment (+)
        </button>
        <button 
          className="cta-button" 
          onClick={() => setCount((count) => count - 1)}
          style={{ background: 'linear-gradient(45deg, #ff6b6b, #ee5a6f)' }}
        >
          Decrement (-)
        </button>
        <button 
          className="cta-button" 
          onClick={() => setCount(0)}
          style={{ background: 'linear-gradient(45deg, #667eea, #764ba2)' }}
        >
          Reset
        </button>
      </div>
      <p style={{ marginTop: '1rem', opacity: 0.7 }}>
        Edit <code>src/App.jsx</code> and save to test HMR
      </p>
    </div>
  )
}

export default Counter