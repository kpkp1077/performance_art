import React from 'react'

const Header = () => {
  return (
    <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
      <nav style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        gap: '2rem', 
        marginBottom: '1rem',
        flexWrap: 'wrap'
      }}>
        <a 
          href="https://vitejs.dev" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ textDecoration: 'none' }}
        >
          <div className="logo">
            <svg width="40" height="40" viewBox="0 0 410 404" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="m399.641 59.5246-215.643 388.545c-3.441 6.194-12.314 6.194-15.755 0l-215.643-388.545c-3.44-6.194 0.859-13.937 7.877-13.937h431.286c7.018 0 11.317 7.743 7.878 13.937z" fill="url(#a)"/>
              <path d="m292.965 1.5744-156.731 283.168c-2.209 3.988-0.566 8.981 3.677 11.18l212.236 109.695c1.678 0.867 3.594 0.867 5.272 0l212.236-109.695c4.243-2.199 5.886-7.192 3.677-11.18l-156.731-283.168c-2.209-3.988-7.145-3.988-9.354 0z" fill="url(#b)"/>
              <defs>
                <linearGradient id="a" x1="194.651" y1="8.818" x2="236.076" y2="292.989" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#41d1ff"/>
                  <stop offset="1" stop-color="#bd34fe"/>
                </linearGradient>
                <linearGradient id="b" x1="194.651" y1="8.818" x2="236.076" y2="292.989" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#ffea83"/>
                  <stop offset="0.083" stop-color="#ffdd35"/>
                  <stop offset="1" stop-color="#ffa800"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
        </a>
        <a 
          href="https://react.dev" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ textDecoration: 'none' }}
        >
          <div className="logo react">
            <svg width="40" height="40" viewBox="-11.5 -10.23174 23 20.46348" xmlns="http://www.w3.org/2000/svg">
              <circle cx="0" cy="0" r="2.05" fill="#61dafb"/>
              <g stroke="#61dafb" strokeWidth="1" fill="none">
                <ellipse rx="11" ry="4.2"/>
                <ellipse rx="11" ry="4.2" transform="rotate(60)"/>
                <ellipse rx="11" ry="4.2" transform="rotate(120)"/>
              </g>
            </svg>
          </div>
        </a>
      </nav>
    </header>
  )
}

export default Header