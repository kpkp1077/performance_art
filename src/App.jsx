import { useState } from 'react'
import Header from './components/Header'
import Counter from './components/Counter'
import FeatureGrid from './components/FeatureGrid'
import Footer from './components/Footer'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="gradient-bg">
      <div className="app-container">
        <Header />
        
        <main className="glass-card">
          <h1 className="main-title">Welcome to Your Modern React App</h1>
          <p className="subtitle">
            Built with Vite, featuring a beautiful glassmorphism design and modern UI patterns
          </p>
          
          <Counter count={count} setCount={setCount} />
          
          <FeatureGrid />
          
          <div className="cta-section">
            <button 
              className="cta-button"
              onClick={() => window.open('https://vitejs.dev', '_blank')}
            >
              Learn Vite
            </button>
            <button 
              className="cta-button"
              onClick={() => window.open('https://react.dev', '_blank')}
            >
              Learn React
            </button>
          </div>
        </main>

        <Footer />
      </div>
    </div>
  )
}

export default App