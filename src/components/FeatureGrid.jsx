import React from 'react'

const FeatureGrid = () => {
  const features = [
    {
      icon: '⚡',
      title: 'Lightning Fast',
      description: 'Built with Vite for instant hot module replacement and optimized builds'
    },
    {
      icon: '🎨',
      title: 'Modern Design',
      description: 'Beautiful glassmorphism UI with smooth animations and responsive design'
    },
    {
      icon: '🔧',
      title: 'Developer Ready',
      description: 'ESLint configured, hot reload enabled, and modern tooling included'
    },
    {
      icon: '📱',
      title: 'Mobile First',
      description: 'Fully responsive design that looks great on all devices and screen sizes'
    },
    {
      icon: '🚀',
      title: 'Production Ready',
      description: 'Optimized build process with code splitting and asset optimization'
    },
    {
      icon: '💡',
      title: 'Best Practices',
      description: 'Following React best practices with hooks, functional components, and more'
    }
  ]

  return (
    <div className="feature-grid">
      {features.map((feature, index) => (
        <div key={index} className="feature-card">
          <div className="feature-icon">{feature.icon}</div>
          <h3 style={{ marginBottom: '0.5rem', color: '#4ecdc4' }}>{feature.title}</h3>
          <p style={{ opacity: 0.8, fontSize: '0.9rem', lineHeight: 1.5 }}>
            {feature.description}
          </p>
        </div>
      ))}
    </div>
  )
}

export default FeatureGrid