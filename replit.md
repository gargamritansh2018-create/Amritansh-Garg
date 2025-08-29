# GARG BANDHU - Business Website

## Overview

GARG BANDHU is a one-page, mobile-responsive business website for a construction materials supplier based in Guna, Madhya Pradesh. The website serves as a digital presence for a business established in 1987, specializing in cement, steel, and paints supply. The site features a modern design with WhatsApp integration for customer bookings and inquiries.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology Stack**: Flask web application serving a single-page website
- **Template Engine**: Jinja2 templates with Flask's built-in templating
- **Static Assets**: CSS and JavaScript files served through Flask's static file handling
- **Responsive Design**: Mobile-first approach using TailwindCSS utility framework

### Design System
- **Styling Framework**: TailwindCSS CDN for utility-first CSS approach
- **Custom Styling**: Additional CSS animations and overrides in separate stylesheet
- **Typography**: Google Fonts (Poppins) for headings, system fonts for body text
- **Color Scheme**: Navy blue (#0F2940) for primary text, bright blue (#2A90E0) for CTAs

### JavaScript Architecture
- **Vanilla JavaScript**: ES6+ features for interactive elements
- **Animation System**: CSS keyframe animations with JavaScript triggers
- **Navigation**: Smooth scrolling implementation with active state management
- **Intersection Observer**: For scroll-based animations and content reveals

### Flask Application Structure
- **Minimal Setup**: Basic Flask app with single route serving the homepage
- **Environment Configuration**: Secret key management through environment variables
- **Development Mode**: Debug mode enabled for development environment
- **Static File Organization**: Separate directories for CSS and JavaScript assets

### User Experience Features
- **Fixed Navigation**: Sticky header with smooth scroll navigation
- **Progressive Enhancement**: Core functionality works without JavaScript
- **Loading Animations**: Fade-in effects for content sections
- **Mobile Optimization**: Responsive breakpoints and touch-friendly interactions

## External Dependencies

### Frontend Libraries
- **TailwindCSS**: Utility-first CSS framework via CDN
- **Google Fonts**: Poppins font family for enhanced typography
- **Font Awesome**: Icon library for UI elements and social media icons

### Python Framework
- **Flask**: Lightweight web framework for serving the application
- **Jinja2**: Template engine (included with Flask)

### Communication Integration
- **WhatsApp Business**: Direct messaging integration for customer inquiries
- **Telephone Links**: Click-to-call functionality for mobile users

### Planned Integrations
- **Google Maps**: Business location embedding
- **Google Business Profile**: Integration with local business listings

The architecture prioritizes simplicity, performance, and mobile accessibility while maintaining professional appearance and functionality suitable for a local construction materials supplier.