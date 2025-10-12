// Loading screen management
window.addEventListener('load', function() {
  setTimeout(() => {
    const loadingScreen = document.getElementById('loadingScreen');
    loadingScreen.style.opacity = '0';
    setTimeout(() => {
      loadingScreen.style.display = 'none';
    }, 500);
  }, 1000);
});

// Create floating particles
function createParticles() {
  const particlesContainer = document.getElementById('particles');
  const particleCount = window.innerWidth > 768 ? 50 : 25;
  
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 6 + 's';
    particle.style.animationDuration = (3 + Math.random() * 6) + 's';
    particlesContainer.appendChild(particle);
  }
}

// Enhanced card interactions
document.querySelectorAll('.card').forEach((card, index) => {
  card.addEventListener('mouseenter', function() {
    // Add ripple effect on hover
    const ripple = document.createElement('div');
    ripple.style.position = 'absolute';
    ripple.style.borderRadius = '50%';
    ripple.style.background = 'rgba(255, 255, 255, 0.3)';
    ripple.style.transform = 'scale(0)';
    ripple.style.animation = 'ripple 0.6s linear';
    ripple.style.left = '50%';
    ripple.style.top = '50%';
    
    this.appendChild(ripple);
    
    setTimeout(() => {
      ripple.remove();
    }, 600);
  });

  // Add click animation
  card.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const clickRipple = document.createElement('div');
    clickRipple.style.position = 'absolute';
    clickRipple.style.left = x + 'px';
    clickRipple.style.top = y + 'px';
    clickRipple.style.width = '10px';
    clickRipple.style.height = '10px';
    clickRipple.style.borderRadius = '50%';
    clickRipple.style.background = 'rgba(255, 255, 255, 0.5)';
    clickRipple.style.transform = 'scale(0)';
    clickRipple.style.animation = 'clickRipple 0.8s ease-out';
    clickRipple.style.pointerEvents = 'none';
    
    this.appendChild(clickRipple);
    
    setTimeout(() => {
      clickRipple.remove();
    }, 800);
  });
});

// Parallax effect for particles
document.addEventListener('mousemove', (e) => {
  const particles = document.querySelectorAll('.particle');
  const x = e.clientX / window.innerWidth;
  const y = e.clientY / window.innerHeight;
  
  particles.forEach((particle, index) => {
    const speed = (index % 5 + 1) * 0.5;
    const xPos = (x - 0.5) * speed;
    const yPos = (y - 0.5) * speed;
    particle.style.transform += ` translate(${xPos}px, ${yPos}px)`;
  });
});

// Initialize particles after DOM load
document.addEventListener('DOMContentLoaded', createParticles);

// Service Worker registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then((registration) => {
        console.log('Service Worker registered with scope: ', registration.scope);
      })
      .catch((error) => {
        console.log('Service Worker registration failed: ', error);
      });
  });
}

// Performance optimization: Intersection Observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = 'running';
    }
  });
}, observerOptions);

document.querySelectorAll('.card').forEach(card => {
  observer.observe(card);
});