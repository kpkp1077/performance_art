import React from 'react'

const Footer = () => {
  return (
    <footer style={{ 
      textAlign: 'center', 
      marginTop: '3rem', 
      padding: '2rem',
      borderTop: '1px solid rgba(255, 255, 255, 0.1)'
    }}>
      <p style={{ opacity: 0.6, fontSize: '0.9rem' }}>
        Built with ❤️ using React + Vite
      </p>
      <div style={{ 
        marginTop: '1rem', 
        display: 'flex', 
        justifyContent: 'center', 
        gap: '2rem',
        flexWrap: 'wrap'
      }}>
        <a 
          href="https://github.com" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ 
            color: '#4ecdc4', 
            textDecoration: 'none',
            fontSize: '0.9rem',
            transition: 'color 0.3s ease'
          }}
          onMouseEnter={(e) => e.target.style.color = '#45b7d1'}
          onMouseLeave={(e) => e.target.style.color = '#4ecdc4'}
        >
          GitHub
        </a>
        <a 
          href="https://vitejs.dev/guide/" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ 
            color: '#4ecdc4', 
            textDecoration: 'none',
            fontSize: '0.9rem',
            transition: 'color 0.3s ease'
          }}
          onMouseEnter={(e) => e.target.style.color = '#45b7d1'}
          onMouseLeave={(e) => e.target.style.color = '#4ecdc4'}
        >
          Vite Docs
        </a>
        <a 
          href="https://react.dev/learn" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ 
            color: '#4ecdc4', 
            textDecoration: 'none',
            fontSize: '0.9rem',
            transition: 'color 0.3s ease'
          }}
          onMouseEnter={(e) => e.target.style.color = '#45b7d1'}
          onMouseLeave={(e) => e.target.style.color = '#4ecdc4'}
        >
          React Docs
        </a>
      </div>
    </footer>
  )
}

export default Footer